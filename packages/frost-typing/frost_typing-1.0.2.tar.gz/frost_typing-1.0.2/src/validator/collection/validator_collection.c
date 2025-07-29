#include "validator/validator.h"

int
_TypeAdapter_CollectionConverterArr(TypeAdapter* self,
                                    ValidateContext* ctx,
                                    PyObject** arr,
                                    Py_ssize_t size,
                                    PyObject** res)
{
    ValidationError* err = NULL;
    TypeAdapter* vd = (TypeAdapter*)self->args;
    for (Py_ssize_t i = 0; i != size; i++) {
        Py_XDECREF(res[i]);
        res[i] = TypeAdapter_Conversion(vd, ctx, arr[i]);
        if (res[i]) {
            continue;
        }

        if (ValidationError_IndexCreate(i, vd, arr[i], ctx->model, &err) < 0) {
            Py_XDECREF(err);
            return -1;
        }
    }

    if (err) {
        ValidationError_RaiseWithModel(err, ctx->model);
        return -1;
    }
    return 0;
}

int
_TypeAdapter_CollectionConverterSet(TypeAdapter* self,
                                    ValidateContext* ctx,
                                    PyObject* set,
                                    PyObject** res)
{
    ValidationError* err = NULL;
    TypeAdapter* vd = (TypeAdapter*)self->args;
    Py_ssize_t pos = 0;
    PyObject* val;

    for (Py_ssize_t i = 0; _PySet_Next(set, &pos, &val); i++) {
        Py_XDECREF(res[i]);
        res[i] = TypeAdapter_Conversion(vd, ctx, val);
        if (res[i]) {
            continue;
        }

        if (ValidationError_IndexCreate(i, vd, val, ctx->model, &err) < 0) {
            Py_XDECREF(err);
            return -1;
        }
    }

    if (err) {
        ValidationError_RaiseWithModel(err, ctx->model);
        return -1;
    }
    return 0;
}

PyObject*
_TypeAdapter_CollectionRepr(TypeAdapter* self)
{
    _PyUnicodeWriter writer;
    _PyUnicodeWriter_Init(&writer);
    writer.overallocate = 1;
    writer.min_length = 12;

    if (!self->ob_str) {
        self->ob_str = self->ob_repr(self);
        if (!self->ob_str) {
            return NULL;
        }
    }
    _UNICODE_WRITE_STR(&writer, self->ob_str);
    _UNICODE_WRITE_CHAR(&writer, '[');
    if (PyTuple_Check(self->args)) {
        Py_ssize_t size = PyTuple_GET_SIZE(self->args);
        for (Py_ssize_t i = 0; i < size; i++) {
            PyObject* val = PyTuple_GET_ITEM(self->args, i);
            _UNICODE_WRITE(&writer, val, PyObject_Repr);
            if (size > 1 && (i + 1) < size) {
                _UNICODE_WRITE_STRING(&writer, ", ", 2);
            }
        }
    } else {
        _UNICODE_WRITE(&writer, self->args, PyObject_Repr);
    }
    _UNICODE_WRITE_CHAR(&writer, ']');
    return _PyUnicodeWriter_Finish(&writer);

error:
    _PyUnicodeWriter_Dealloc(&writer);
    return NULL;
}

int
TypeAdapter_CollectionCheckArgs(PyObject* type_args,
                                PyTypeObject* tp,
                                Py_ssize_t args_cnt)
{
    if (PyTuple_GET_SIZE(type_args) != args_cnt) {
        PyErr_Format(FrostUserError,
                     "Expected %s to have exactly %zu generic parameters",
                     tp->tp_name,
                     args_cnt);
        return 0;
    }
    return 1;
}

TypeAdapter*
_TypeAdapter_NewCollection(PyObject* cls, PyObject* args, Converter conv)
{
    PyObject* str =
      PyUnicode_InternFromString(_CAST(PyTypeObject*, cls)->tp_name);
    if (!str) {
        return NULL;
    }

    TypeAdapter* res = TypeAdapter_Create(
      cls, args, str, _TypeAdapter_CollectionRepr, conv, Inspector_No);
    Py_DECREF(str);
    return res;
}

TypeAdapter*
TypeAdapter_CreateCollection(PyObject* hint, PyObject* tp, PyObject* origin)
{
    PyObject* type_args = PyTyping_Get_Args(hint);
    if (!type_args) {
        return NULL;
    }

    TypeAdapter* res = NULL;
    if (origin == (PyObject*)&PyDict_Type) {
        res = _TypeAdapter_Create_Dict(origin, type_args, tp);
    } else if (origin == (PyObject*)&PyTuple_Type) {
        res = _TypeAdapter_Create_Tuple(origin, type_args, tp);
    } else if (origin == (PyObject*)&PyList_Type) {
        res = _TypeAdapter_Create_List(origin, type_args, tp);
    } else if (origin == (PyObject*)&PySet_Type ||
               origin == (PyObject*)&PyFrozenSet_Type) {
        res = _TypeAdapter_Create_Set(origin, type_args, tp);
    } else if (origin == AbcIterable) {
        res = _TypeAdapter_CreateIterable(AbcIterable, tp, type_args);
    } else if (origin == AbcGenerator) {
        res = _TypeAdapter_CreateGenerator(tp, type_args);
    } else if (origin == AbcSequence) {
        res = _TypeAdapter_CreateSequence(tp, type_args);
    } else {
        PyErr_Format(FrostUserError, "Unsupported annotation: '%S'", hint);
    }

    Py_DECREF(type_args);
    return res;
}

int
validator_collection_setup(void)
{
    return validator_tuple_setup();
}

void
validator_collection_free(void)
{
    validator_tuple_free();
}