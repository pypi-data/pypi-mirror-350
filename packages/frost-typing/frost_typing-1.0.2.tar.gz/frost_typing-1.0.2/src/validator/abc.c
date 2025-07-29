#include "field.h"
#include "validator/validator.h"

#define ASYNC ((uint32_t)1 << 31)

static PyObject *__send, *__throw, *__close;

TypeAdapter *TypeAdapter_AbcHashable, *TypeAdapter_AbcCallable,
  *TypeAdapter_AbcByteString;

static void
validator_iterable_dealloc(ValidatorIterable* self)
{
    Py_DECREF(self->ctx);
    Py_DECREF(self->iterator);
    Py_DECREF(self->validator);
    Py_TYPE(self)->tp_free(self);
}

static PyObject*
validator_iterable_repr(ValidatorIterable* self)
{
    return PyUnicode_FromFormat(
      "%s[%.100S]", Py_TYPE(self)->tp_name, self->validator);
}

static PyObject*
validator_iterable_validate(ValidatorIterable* self, PyObject* val)
{
    ValidateContext vctx =
      ValidateContext_Create(self->ctx, self, Py_TYPE(self), self->flags);
    PyObject* res = TypeAdapter_Conversion(self->validator, &vctx, val);
    if (!res) {
        ValidationError_Raise(
          NULL, self->validator, val, (PyObject*)Py_TYPE(self));
    }
    return res;
}

static PyObject*
validator_iterable_next_no_validator(ValidatorIterable* self)
{
    iternextfunc tp_iternext = Py_TYPE(self->iterator)->tp_iternext;
    if (!tp_iternext) {
        PyErr_BadArgument();
        return NULL;
    }

    PyObject* item = tp_iternext(self->iterator);
    if (item) {
        return item;
    }

    PyObject *exc_type, *exc_val, *exc_tb;
    PyErr_Fetch(&exc_type, &exc_val, &exc_tb);
    if (!exc_type) {
        return NULL;
    }

    if (!PyErr_GivenExceptionMatches(exc_type, PyExc_StopIteration)) {
        PyErr_Restore(exc_type, exc_val, exc_tb);
        return NULL;
    }

    PyObject* res = validator_iterable_validate(self, exc_val);
    Py_DECREF(exc_val);
    if (!res) {
        Py_DECREF(exc_type);
        Py_XDECREF(exc_tb);
        return NULL;
    }
    PyErr_Restore(exc_type, res, exc_tb);
    return NULL;
}

static PyObject*
validator_iterable_next_iter(ValidatorIterable* self)
{
    PyObject* item;
    int r = _PyIter_GetNext(self->iterator, &item);
    if (r != 1) {
        return NULL;
    }

    PyObject* res = validator_iterable_validate(self, item);
    Py_DECREF(item);
    return res;
}

static PyObject*
validator_iterable_next(ValidatorIterable* self)
{
    if (self->flags | ASYNC) {
        return validator_iterable_next_no_validator(self);
    }
    return validator_iterable_next_iter(self);
}

static PyObject*
validator_iterable_send(ValidatorIterable* self, PyObject* args)
{
    return PyObject_CallMethodOneArg(self->iterator, __send, args);
};

static PyObject*
validator_iterable_throw(ValidatorIterable* self,
                         PyObject* const* args,
                         Py_ssize_t nargs,
                         PyObject* kwnames)
{
    PyObject* func = PyObject_GetAttr(self->iterator, __throw);
    if (!func) {
        return NULL;
    }
    PyObject* res = PyObject_Vectorcall(func, args, nargs, kwnames);
    Py_DECREF(func);
    return res;
};

static PyObject*
validator_iterable_close(ValidatorIterable* self)
{
    return PyObject_CallMethodNoArgs(self->iterator, __close);
};

static PyAsyncMethods validator_iterable_async_methods = {
    .am_await = PyObject_SelfIter,
};

static PyMethodDef validator_iterable_methods[] = {
    { "send", (PyCFunction)validator_iterable_send, METH_O, NULL },
    { "close", (PyCFunction)validator_iterable_close, METH_NOARGS, NULL },
    { "throw",
      (PyCFunction)validator_iterable_throw,
      METH_FASTCALL | METH_KEYWORDS,
      NULL },
    { NULL },
};

PyTypeObject ValidatorIterableType = {
    .tp_iternext = (iternextfunc)validator_iterable_next,
    .tp_dealloc = (destructor)validator_iterable_dealloc,
    .tp_as_async = &validator_iterable_async_methods,
    .tp_repr = (reprfunc)validator_iterable_repr,
    .tp_name = "frost_typing.ValidatorIterable",
    .tp_methods = validator_iterable_methods,
    .tp_basicsize = sizeof(ValidatorIterable),
    .tp_iter = PyObject_SelfIter,
};

static PyObject*
validator_iterable_create(PyObject* iterator,
                          ContextManager* ctx,
                          TypeAdapter* validator,
                          uint32_t flags)
{
    ValidatorIterable* self =
      (ValidatorIterable*)ValidatorIterableType.tp_alloc(&ValidatorIterableType,
                                                         0);
    if (!self) {
        Py_DECREF(iterator);
        return NULL;
    }

    self->validator = (TypeAdapter*)Py_NewRef(validator);
    self->ctx = (ContextManager*)Py_NewRef(ctx);
    self->iterator = Py_NewRef(iterator);
    self->flags = flags;
    return (PyObject*)self;
};

PyObject*
ValidatorIterable_Create(PyObject* iterable,
                         ValidateContext* ctx,
                         TypeAdapter* validator)
{
    PyObject* iterator = PyObject_GetIter(iterable);
    if (!iterator) {
        return NULL;
    }

    PyObject* self =
      validator_iterable_create(iterator, ctx->ctx, validator, ctx->flags);
    Py_DECREF(iterator);
    return self;
};

PyObject*
ValidatorIterable_CreateAsync(PyObject* coroutine,
                              ValidateContext* ctx,
                              TypeAdapter* validator)
{
    PyTypeObject* tp = Py_TYPE(coroutine);
    if (!tp->tp_as_async || !tp->tp_as_async->am_await) {
        return PyErr_Format(PyExc_TypeError,
                            "object %.100s can't be used in 'await' expression",
                            tp->tp_name);
    }

    PyObject* iterator = tp->tp_as_async->am_await(coroutine);
    if (!iterator) {
        return NULL;
    }

    PyObject* self = validator_iterable_create(
      iterator, ctx->ctx, validator, ctx->flags | ASYNC);
    Py_DECREF(iterator);
    return self;
};

static int
hashable_inspector(UNUSED TypeAdapter* self, PyObject* val)
{
    return PyObject_CheckHashable(val);
}

static int
callable_inspector(UNUSED TypeAdapter* self, PyObject* val)
{
    return PyCallable_Check(val);
}

static int
iterable_inspector(UNUSED TypeAdapter* self, PyObject* val)
{
    return PyObject_CheckIter(val);
}

static PyObject*
iterable_convector(TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    return ValidatorIterable_Create(val, ctx, (TypeAdapter*)self->args);
}

static int
sequence_inspector(UNUSED TypeAdapter* self, PyObject* val)
{
    PySequenceMethods* tp_as_sequence = Py_TYPE(val)->tp_as_sequence;
    return tp_as_sequence && tp_as_sequence->sq_length &&
           tp_as_sequence->sq_item;
}

static int
byte_string_inspector(UNUSED TypeAdapter* self, PyObject* val)
{
    return PyBytes_Check(val) || PyByteArray_Check(val);
}

static PyObject*
byte_string_converter(UNUSED TypeAdapter* self,
                      ValidateContext* ctx,
                      PyObject* val)
{
    if ((ctx->flags & FIELD_STRICT) || !PyUnicode_Check(val)) {
        return NULL;
    }
    return PyUnicode_AsUTF8String(val);
}

static TypeAdapter*
type_adapter_create_iterable(PyObject* hint, PyObject* tp, PyObject* args)
{
    if (!args) {
        return TypeAdapter_Create(hint,
                                  NULL,
                                  NULL,
                                  TypeAdapter_Base_Repr,
                                  Not_Converter,
                                  iterable_inspector);
    }

    PyObject* vd = (PyObject*)ParseHint(PyTuple_GET_ITEM(args, 0), tp);
    if (!vd) {
        return NULL;
    }

    TypeAdapter* res = _TypeAdapter_NewCollection(hint, vd, iterable_convector);
    Py_DECREF(vd);
    return res;
}

TypeAdapter*
_TypeAdapter_CreateIterable(PyObject* cls, PyObject* tp, PyObject* args)
{
    if (args && !TypeAdapter_CollectionCheckArgs(args, (PyTypeObject*)cls, 1)) {
        return NULL;
    }
    return type_adapter_create_iterable(cls, tp, args);
}

TypeAdapter*
_TypeAdapter_CreateGenerator(PyObject* tp, PyObject* args)
{
    if (args && !TypeAdapter_CollectionCheckArgs(
                  args, (PyTypeObject*)AbcGenerator, 3)) {
        return NULL;
    }
    return type_adapter_create_iterable(AbcGenerator, tp, args);
}

TypeAdapter*
_TypeAdapter_CreateSequence(PyObject* tp, PyObject* args)
{
    if (!args) {
        return TypeAdapter_Create(AbcSequence,
                                  NULL,
                                  NULL,
                                  TypeAdapter_Base_Repr,
                                  Not_Converter,
                                  sequence_inspector);
    }
    return _TypeAdapter_Create_List(AbcSequence, args, tp);
}

int
abc_setup(void)
{
#define TYPE_ADAPTER_ABC(h, conv, ins)                                         \
    TypeAdapter_##h =                                                          \
      TypeAdapter_Create(h, NULL, NULL, TypeAdapter_Base_Repr, conv, ins);     \
    if (!TypeAdapter_##h) {                                                    \
        return -1;                                                             \
    }

    if (PyType_Ready(&ValidatorIterableType) < 0) {
        return -1;
    }

    CREATE_VAR_INTERN___STING(send);
    CREATE_VAR_INTERN___STING(throw);
    CREATE_VAR_INTERN___STING(close);

    TYPE_ADAPTER_ABC(AbcCallable, Not_Converter, callable_inspector);
    TYPE_ADAPTER_ABC(AbcHashable, Not_Converter, hashable_inspector);
    TYPE_ADAPTER_ABC(
      AbcByteString, byte_string_converter, byte_string_inspector);

#undef TYPE_ADAPTER_ABC
    return 0;
}

void
abc_free(void)
{
    Py_DECREF(__send);
    Py_DECREF(__throw);
    Py_DECREF(__close);
    Py_DECREF(TypeAdapter_AbcCallable);
    Py_DECREF(TypeAdapter_AbcHashable);
    Py_DECREF(TypeAdapter_AbcByteString);
}