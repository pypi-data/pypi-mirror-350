#include "validator/validator.h"

static PyObject* _unicode_literal;

static PyObject*
validator_literal_repr(TypeAdapter* self)
{
    _PyUnicodeWriter writer;
    _PyUnicodeWriter_Init(&writer);
    writer.overallocate = 1;
    writer.min_length = 16;
    PyObject* iter = PyObject_GetIter(self->args);
    if (!iter) {
        return NULL;
    }

    PyObject* item;
    Py_ssize_t cnt = 0;
    _UNICODE_WRITE_STRING(&writer, "Literal[", 8);
    for (;;) {
        int r = _PyIter_GetNext(iter, &item);
        if (r < 0) {
            goto error;
        }
        if (!r) {
            break;
        }

        if (cnt) {
            if (_PyUnicodeWriter_WriteASCIIString(&writer, ", ", 2) < 0) {
                Py_DECREF(item);
                goto error;
            }
        }

        r = _UnicodeWriter_Write(&writer, item, PyObject_Repr);
        cnt++;
        Py_DECREF(item);
        if (r < 0) {
            goto error;
        }
    }

    _UNICODE_WRITE_CHAR(&writer, ']');
    Py_DECREF(iter);
    return _PyUnicodeWriter_Finish(&writer);

error:
    Py_DECREF(iter);
    _PyUnicodeWriter_Dealloc(&writer);
    return NULL;
}

static int
inspector_literal(TypeAdapter* self, PyObject* val)
{
    return PySet_Contains(self->args, val) == 1;
}

inline TypeAdapter*
TypeAdapter_Create_Literal(PyObject* hint)
{
    PyObject* args = PyTyping_Get_Args(hint);
    if (args == NULL) {
        return NULL;
    }
    PyObject* values = PyFrozenSet_New(args);
    Py_DECREF(args);

    if (values == NULL) {
        return NULL;
    }
    TypeAdapter* res = TypeAdapter_Create(hint,
                                          values,
                                          _unicode_literal,
                                          validator_literal_repr,
                                          Not_Converter,
                                          inspector_literal);
    Py_DECREF(values);
    return res;
}

int
validator_literal_setup(void)
{
    _unicode_literal = PyUnicode_InternFromString("Literal");
    return _unicode_literal ? 0 : -1;
}

void
validator_literal_free(void)
{
    Py_DECREF(_unicode_literal);
}