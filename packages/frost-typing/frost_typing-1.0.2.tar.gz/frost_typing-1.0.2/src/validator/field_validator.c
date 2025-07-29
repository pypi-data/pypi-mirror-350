#include "meta_valid_model.h"
#include "stddef.h"
#include "validator/validator.h"

PyObject* registered_field_validator;
static PyObject *__before, *__after, *__wrap;

static inline PyObject*
registered_field_validator_get_dict(PyObject* type)
{
    PyObject* dict = PyDict_GetItem(registered_field_validator, type);
    if (!dict) {
        dict = PyDict_New();
        if (!dict) {
            return NULL;
        }
        if (PyDict_SetItemDecrefVal(registered_field_validator, type, dict)) {
            return NULL;
        }
    }
    return dict;
}

static inline PyObject*
registered_field_validator_get_list(PyObject* dict, PyObject* name)
{
    PyObject* list = PyDict_GetItem(dict, name);
    if (!list) {
        list = PyList_New(0);
        if (!list) {
            return NULL;
        }
        if (PyDict_SetItemDecrefVal(dict, name, list) < 0) {
            return NULL;
        }
    }
    return list;
}

static int
registration_field_validator(FieldValidator* self, PyObject* type)
{
    if (!PyType_IsSubtype(Py_TYPE(type), &MetaValidModelType)) {
        _RaiseInvalidType(
          "owner", "subtype of the ValidModel", Py_TYPE(type)->tp_name);
        return -1;
    }

    if (MetaValid_IS_SUBCLASS(type)) {
        PyErr_SetString(PyExc_TypeError,
                        "Cannot register after type is created");
        return -1;
    }

    PyObject* dict = registered_field_validator_get_dict(type);
    if (!dict) {
        return -1;
    }

    for (Py_ssize_t i = 0; i < PyTuple_GET_SIZE(self->fields_name); i++) {
        PyObject* name = PyTuple_GET_ITEM(self->fields_name, i);
        PyObject* list = registered_field_validator_get_list(dict, name);
        if (!list) {
            goto error;
        }

        if (PyList_Append(list, (PyObject*)self) < 0) {
            goto error;
        }
    }

    return 0;

error:
    PyDict_DelItem(registered_field_validator, type);
    return -1;
}

static inline PyObject*
field_validator_registered_pop_list(PyObject* type, PyObject* name)
{
    PyObject* dict = PyDict_GetItem(registered_field_validator, type);
    if (!dict) {
        return NULL;
    }

    PyObject* list = PyDict_GetItem(dict, name);
    if (!list) {
        return NULL;
    }

    Py_INCREF(list);
    PyDict_DelItem(dict, name);
    if (!PyDict_GET_SIZE(dict)) {
        PyDict_DelItem(registered_field_validator, type);
    }
    return list;
}

static int
field_validator_registered_pop(PyObject* type,
                               PyObject* name,
                               PyObject** args,
                               PyObject** wrap)
{
    PyObject* list = field_validator_registered_pop_list(type, name);
    if (!list) {
        *args = NULL;
        return 0;
    }

    PyObject* res = PyTuple_New(2);
    if (!res) {
        Py_DECREF(list);
        return -1;
    }

    Py_ssize_t wrap_cnt = 0;
    Py_ssize_t after_cnt = 0;
    Py_ssize_t before_cnt = 0;
    Py_ssize_t size = PyList_GET_SIZE(list);
    for (Py_ssize_t i = 0; i < size; i++) {
        FieldValidator* fv = (FieldValidator*)PyList_GET_ITEM(list, i);
        wrap_cnt += (fv->flags & FIELD_VALIDATOR_WRAP) != 0;
        after_cnt += (fv->flags & FIELD_VALIDATOR_AFRET) != 0;
        before_cnt += (fv->flags & FIELD_VALIDATOR_BEFORE) != 0;
    }

    PyObject* before = NULL;
    PyObject* after = NULL;
    PyObject* wrap_ = NULL;
    if (after_cnt > 1) {
        after = PyTuple_New(after_cnt);
        if (!after) {
            goto error;
        }
    }

    if (before_cnt > 1) {
        before = PyTuple_New(before_cnt);
        if (!before) {
            goto error;
        }
    }

    if (wrap_cnt > 1) {
        wrap_ = PyTuple_New(wrap_cnt);
        if (!wrap_) {
            goto error;
        }
    }

    Py_ssize_t wrap_ind = 0;
    Py_ssize_t after_ind = 0;
    Py_ssize_t before_ind = 0;
    for (Py_ssize_t i = 0; i < size; i++) {
        FieldValidator* fv = (FieldValidator*)PyList_GET_ITEM(list, i);
        if (fv->flags & FIELD_VALIDATOR_AFRET) {
            if (after_cnt == 1) {
                after = Py_NewRef(fv->func);
            } else {
                PyTuple_SET_ITEM(after, after_ind++, Py_NewRef(fv->func));
            }
        } else if ((fv->flags & FIELD_VALIDATOR_BEFORE)) {
            if (before_cnt == 1) {
                before = Py_NewRef(fv->func);
            } else {
                PyTuple_SET_ITEM(before, before_ind++, Py_NewRef(fv->func));
            }
        } else if ((fv->flags & FIELD_VALIDATOR_WRAP)) {
            if (wrap_cnt == 1) {
                wrap_ = Py_NewRef(fv->func);
            } else {
                PyTuple_SET_ITEM(wrap_, wrap_ind++, Py_NewRef(fv->func));
            }
        }
    }

    Py_DECREF(list);
    PyTuple_SET_ITEM(res, 0, before);
    PyTuple_SET_ITEM(res, 1, after);
    *args = res;
    *wrap = wrap_;
    return 1;

error:
    *args = NULL;
    *wrap = NULL;
    Py_XDECREF(wrap_);
    Py_XDECREF(after);
    Py_XDECREF(before);
    Py_DECREF(list);
    return -1;
}

static void
field_validator_dealloc(FieldValidator* self)
{
    Py_XDECREF(self->func);
    Py_DECREF(self->fields_name);
    Py_TYPE(self)->tp_free(self);
}

static PyObject*
field_validator_proxy_call(FieldValidator* self,
                           PyObject* const* args,
                           size_t nargsf,
                           PyObject* kwnames)
{
    return PyObject_Vectorcall(self->func, args, nargsf, kwnames);
}

static PyObject*
field_validator_set_func(FieldValidator* self,
                         PyObject* const* args,
                         size_t nargs,
                         PyObject* kwn)
{
    self->func = _VectorCall_GetFuncArg("field_validator", args, nargs, kwn);
    if (!self->func) {
        return NULL;
    }
    self->vectorcall = (vectorcallfunc)field_validator_proxy_call;
    return Py_NewRef(self);
}

static PyObject*
field_validator_new(PyTypeObject* type, PyObject* args, PyObject* kwargs)
{
    FieldValidator* self;
    Py_ssize_t args_size = PyTuple_GET_SIZE(args);
    if (args_size == 0) {
        return PyErr_Format(PyExc_TypeError,
                            "%.100s() missing 1 required "
                            "positional argument: 'field'",
                            type->tp_name);
    }

    for (Py_ssize_t i = 0; i < args_size; i++) {
        PyObject* field = PyTuple_GET_ITEM(args, i);
        if (!PyUnicode_Check(field)) {
            return PyErr_Format(
              PyExc_TypeError,
              "attribute fields.%zu must be string, not '%.100s'",
              i,
              Py_TYPE(field)->tp_name);
        }
    }

    PyObject* mode = __after;
    char* kwlist[] = { "mode", NULL };
    int r = PyArg_ParseTupleAndKeywords(
      VoidTuple, kwargs, "|U:field_validator.__new__", kwlist, &mode);
    if (!r) {
        return NULL;
    }

    uint8_t flags;
    if (PyObject_RichCompareBool(__after, mode, Py_EQ)) {
        flags = FIELD_VALIDATOR_AFRET;
    } else if (PyObject_RichCompareBool(__before, mode, Py_EQ)) {
        flags = FIELD_VALIDATOR_BEFORE;
    } else if (PyObject_RichCompareBool(__wrap, mode, Py_EQ)) {
        flags = FIELD_VALIDATOR_WRAP;
    } else {
        return PyErr_Format(PyExc_ValueError,
                            "Argument 'mode' must be a valid value of "
                            "'before' or 'after' or 'wrap', not '%.100U'",
                            mode);
    }

    self = (FieldValidator*)type->tp_alloc(type, 0);
    if (!self) {
        return NULL;
    }

    self->flags = flags;
    self->fields_name = Py_NewRef(args);
    self->vectorcall = (vectorcallfunc)field_validator_set_func;
    return (PyObject*)self;
}

static PyObject*
field_validator_set_name(FieldValidator* self,
                         PyObject* const* args,
                         Py_ssize_t nargs)
{
    Py_ssize_t cnt = PyVectorcall_NARGS(nargs);
    if (!PyCheck_ArgsCnt("__set_name__", cnt, 2)) {
        return NULL;
    }

    PyObject* owner = (PyObject*)args[0];
    if (registration_field_validator(self, owner) < 0) {
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyObject*
field_validator_get(FieldValidator* self,
                    UNUSED PyObject* instance,
                    PyObject* owner)
{
    return PyMethod_New(self->func, owner);
}

static PyMethodDef field_validator_methods[] = {
    { "__set_name__",
      (PyCFunction)field_validator_set_name,
      METH_FASTCALL,
      NULL },
    { NULL }
};

PyTypeObject FieldValidatorType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_dealloc =
      (destructor)field_validator_dealloc,
    .tp_vectorcall_offset = offsetof(FieldValidator, vectorcall),
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_VECTORCALL,
    .tp_descr_get = (descrgetfunc)field_validator_get,
    .tp_name = "frost_typing.field_validator",
    .tp_basicsize = sizeof(FieldValidator),
    .tp_methods = field_validator_methods,
    .tp_new = field_validator_new,
    .tp_call = PyVectorcall_Call,
};

int
field_validator_setup(void)
{
    CREATE_VAR_INTERN___STING(before);
    CREATE_VAR_INTERN___STING(after);
    CREATE_VAR_INTERN___STING(wrap);
    registered_field_validator = PyDict_New();
    if (!registered_field_validator) {
        return -1;
    }
    return PyType_Ready(&FieldValidatorType);
}

void
field_validator_free(void)
{
    Py_DECREF(__wrap);
    Py_DECREF(__after);
    Py_DECREF(__before);
    Py_DECREF(&FieldValidatorType);
    Py_DECREF(registered_field_validator);
}

int
FieldValidator_CheckRegistered(PyObject* type)
{
    PyObject* dict = PyDict_GetItem(registered_field_validator, type);
    if (!dict) {
        return 0;
    }

    if (!PyDict_GET_SIZE(dict)) {
        PyDict_DelItem(registered_field_validator, type);
        return 1;
    }

    PyObject* join = PyUnicode_Join(__sep_and__, dict);
    PyDict_DelItem(registered_field_validator, type);
    if (join == NULL) {
        return -1;
    }

    PyErr_Format(
      PyExc_ValueError, "Decorators defined with incorrect fields: '%S'", join);
    Py_DECREF(join);
    return -1;
}

static PyObject*
field_validator_validate(PyObject* validators,
                         ValidateContext* ctx,
                         PyObject* val)
{
    PyObject** vd;
    Py_ssize_t size;
    PyObject* args[2] = { (PyObject*)Py_TYPE(ctx->cur_obj), NULL };
    if (PyTuple_Check(validators)) {
        vd = TUPLE_ITEMS(validators);
        size = PyTuple_GET_SIZE(validators);
    } else {
        vd = &validators;
        size = 1;
    }

    Py_INCREF(val);
    for (Py_ssize_t i = 0; i != size; i++) {
        args[1] = val;
        PyObject* tmp = PyObject_Vectorcall(vd[i], args, 2, NULL);
        Py_DECREF(val);
        if (!tmp) {
            ValidationError_ExceptionHandling(ctx->model, val);
            return NULL;
        }
        val = tmp;
    }
    return val;
}

static PyObject*
converter_field_validator(TypeAdapter* self,
                          ValidateContext* ctx,
                          PyObject* val)
{
    PyObject* tmp;
    PyObject* before = PyTuple_GET_ITEM(self->args, 0);
    PyObject* after = PyTuple_GET_ITEM(self->args, 1);

    if (before) {
        tmp = field_validator_validate(before, ctx, val);
        Py_DECREF(val);
        val = tmp;
        if (!val) {
            return NULL;
        }
    } else {
        Py_INCREF(val);
    }

    tmp = TypeAdapter_Conversion((TypeAdapter*)self->cls, ctx, val);
    Py_DECREF(val);
    if (!tmp) {
        return NULL;
    }
    val = tmp;

    if (after) {
        tmp = field_validator_validate(after, ctx, val);
        Py_DECREF(val);
        return tmp;
    }
    return val;
}

static PyObject*
converter_field_validator_wrap(TypeAdapter* self,
                               ValidateContext* ctx,
                               PyObject* val)
{
    PyObject* handler = Handler_Create(ctx, (TypeAdapter*)self->cls);
    if (!handler) {
        return NULL;
    }

    PyObject* const args[4] = {
        NULL, (PyObject*)Py_TYPE(ctx->cur_obj), val, handler
    };
    PyObject* res = PyObject_Vectorcall(
      self->args, args + 1, 3 | PY_VECTORCALL_ARGUMENTS_OFFSET, NULL);
    Py_DECREF(handler);

    if (!res) {
        ValidationError_ExceptionHandling(ctx->model, res);
    }
    return res;
}

static inline TypeAdapter*
set_field_validator_wrap(TypeAdapter* validator, PyObject* wrap)
{
    if (!PyTuple_Check(wrap)) {
        return TypeAdapter_Create((PyObject*)validator,
                                  wrap,
                                  NULL,
                                  TypeAdapter_Base_Repr,
                                  converter_field_validator_wrap,
                                  Inspector_No);
    }

    Py_INCREF(validator);
    for (Py_ssize_t i = 0; i != PyTuple_GET_SIZE(wrap); i++) {
        PyObject* func = PyTuple_GET_ITEM(wrap, i);
        TypeAdapter* tmp = set_field_validator_wrap(validator, func);
        Py_DECREF(validator);
        if (!tmp) {
            return NULL;
        }
        validator = tmp;
    }
    return validator;
}

TypeAdapter*
_TypeAdapter_Create_FieldValidator(TypeAdapter* validator,
                                   PyObject* type,
                                   PyObject* name)
{
    PyObject *args, *wrap;
    int r = field_validator_registered_pop(type, name, &args, &wrap);
    if (r < 0) {
        return NULL;
    }
    if (!r) {
        Py_INCREF(validator);
        return validator;
    }

    TypeAdapter* res = TypeAdapter_Create((PyObject*)validator,
                                          args,
                                          NULL,
                                          TypeAdapter_Base_Repr,
                                          converter_field_validator,
                                          Inspector_No);
    Py_DECREF(args);
    if (!res) {
        Py_XDECREF(wrap);
        return NULL;
    }

    if (wrap) {
        TypeAdapter* tmp = set_field_validator_wrap(res, wrap);
        Py_DECREF(wrap);
        Py_DECREF(res);
        return tmp;
    }
    return res;
}

TypeAdapter*
TypeAdapter_Create_FieldValidator(PyObject* hint,
                                  PyObject* type,
                                  PyObject* name)
{
    TypeAdapter* validator = ParseHint(hint, type);
    if (validator == NULL) {
        return NULL;
    }

    TypeAdapter* res =
      _TypeAdapter_Create_FieldValidator(validator, type, name);
    Py_DECREF(validator);
    return res;
}