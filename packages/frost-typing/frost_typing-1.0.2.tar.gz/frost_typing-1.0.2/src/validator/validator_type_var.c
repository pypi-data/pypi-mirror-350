#include "validator/validator.h"

static PyObject*
validator_type_var_repr(TypeAdapter* self)
{
    _PyUnicodeWriter writer;
    PyObject *bound, *constraints;
    _PyUnicodeWriter_Init(&writer);
    writer.overallocate = 1;
    writer.min_length = 32;

    bound = PyTuple_GET_ITEM(self->args, 0);
    constraints = PyTuple_GET_ITEM(self->args, 1);

    _UNICODE_WRITE_STRING(&writer, "TypeVar[", 8);
    _UNICODE_WRITE(&writer, self->cls, PyObject_Repr);
    _UNICODE_WRITE_STRING(&writer, "](bound=", 8);
    _UNICODE_WRITE_STRING(
      &writer, bound != Py_None ? ((PyTypeObject*)bound)->tp_name : "None", -1);
    _UNICODE_WRITE_STRING(&writer, ", constraints=(", 15);

    Py_ssize_t size = PyTuple_GET_SIZE(constraints);
    for (Py_ssize_t i = 0; i < size; i++) {
        if (i) {
            _UNICODE_WRITE_STRING(&writer, ", ", 2);
        }
        PyTypeObject* tp = (PyTypeObject*)PyTuple_GET_ITEM(constraints, i);
        _UNICODE_WRITE_STRING(&writer, tp->tp_name, -1);
    }
    _UNICODE_WRITE_STRING(&writer, "))", 2);
    return _PyUnicodeWriter_Finish(&writer);

error:
    _PyUnicodeWriter_Dealloc(&writer);
    return NULL;
}

static PyObject*
converter_type_var(TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    TypeAdapter* validator;
    if (_ContextManager_Get_TTypeAdapter(self->cls, ctx->ctx, &validator)) {
        PyObject* res = TypeAdapter_Conversion(validator, ctx, val);
        if (!res) {
            ValidationError_Raise(NULL, validator, val, ctx->model);
        }
        return res;
    }

    PyObject *type, *bound, *constraints;
    type = (PyObject*)Py_TYPE(val);
    bound = PyTuple_GET_ITEM(self->args, 0);
    constraints = PyTuple_GET_ITEM(self->args, 1);

    if (bound != Py_None) {
        if (PyObject_IsSubclass(type, bound) != 1) {
            return NULL;
        }
    }

    if (PyTuple_GET_SIZE(constraints)) {
        if (PyObject_IsSubclass(type, constraints) != 1) {
            return NULL;
        }
    }
    return Py_NewRef(val);
}

TypeAdapter*
TypeAdapter_Create_TypeVar(PyObject* hint)
{
    PyObject *constraints, *bound;
    bound = PyTyping_Get_Bound(hint);
    if (bound == NULL) {
        return NULL;
    }
    constraints = PyTyping_Get_Constraints(hint);
    if (constraints == NULL) {
        Py_DECREF(bound);
        return NULL;
    }

    for (Py_ssize_t i = 0; i < PyTuple_GET_SIZE(constraints); i++) {
        PyObject* tmp = PyTuple_GET_ITEM(constraints, i);
        if (!PyType_Check(tmp)) {
            Py_DECREF(bound);
            Py_DECREF(constraints);
            _RaiseInvalidType("__constraints__", "type", Py_TYPE(tmp)->tp_name);
            return NULL;
        }
    }

    PyObject* args = PyTuple_Pack(2, bound, constraints);
    Py_DECREF(constraints);
    Py_DECREF(bound);
    if (args == NULL) {
        return NULL;
    }
    PyObject* ob_str = PyObject_Str(hint);
    if (ob_str == NULL) {
        Py_DECREF(args);
        return NULL;
    }
    TypeAdapter* res = TypeAdapter_Create(hint,
                                          args,
                                          ob_str,
                                          validator_type_var_repr,
                                          converter_type_var,
                                          Inspector_No);
    Py_DECREF(ob_str);
    Py_DECREF(args);
    return res;
}