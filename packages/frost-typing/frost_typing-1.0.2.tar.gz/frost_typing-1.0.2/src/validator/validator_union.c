#include "field.h"
#include "validator/validator.h"

static PyObject*
validator_union_repr(TypeAdapter* self)
{
    PyObject* tmp;
    _PyUnicodeWriter writer;
    _PyUnicodeWriter_Init(&writer);
    writer.overallocate = 1;
    writer.min_length = 16;

    _UNICODE_WRITE_STRING(&writer, "Union[", 6);
    Py_ssize_t size = PyTuple_GET_SIZE(self->cls);
    for (Py_ssize_t i = 0; i < size; i++) {
        tmp = PyTuple_GET_ITEM(self->cls, i);
        _UNICODE_WRITE(&writer, tmp, PyObject_Repr);
        if (i < size - 1) {
            _UNICODE_WRITE_STRING(&writer, ", ", 2);
        }
    }

    _UNICODE_WRITE_CHAR(&writer, ']');
    return _PyUnicodeWriter_Finish(&writer);

error:
    _PyUnicodeWriter_Dealloc(&writer);
    return NULL;
}

static PyObject*
converter_union(TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    if (ctx->flags & FIELD_STRICT) {
        return NULL;
    }

    Py_ssize_t size = PyTuple_GET_SIZE(self->args);
    TypeAdapter* validator;
    PyObject* tmp;
    for (Py_ssize_t i = 0; i < size; i++) {
        validator = (TypeAdapter*)PyTuple_GET_ITEM(self->args, i);
        tmp = TypeAdapter_Conversion(validator, ctx, val);
        if (!tmp) {
            PyErr_Clear();
            continue;
        }
        return tmp;
    }
    return NULL;
}

TypeAdapter*
TypeAdapter_Create_Union(PyObject* hint, PyObject* tp)
{
    PyObject* type_args = PyTyping_Get_Args(hint);
    if (type_args == NULL) {
        return NULL;
    }
    PyObject *args, *cls;
    args = cls = TypeAdapter_MapParseHintTuple(type_args, tp);
    Py_DECREF(type_args);
    if (cls == NULL) {
        return NULL;
    }
    return TypeAdapter_Create(cls,
                            args,
                            NULL,
                            validator_union_repr,
                            converter_union,
                            Inspector_IsInstanceTypeAdapter);
}