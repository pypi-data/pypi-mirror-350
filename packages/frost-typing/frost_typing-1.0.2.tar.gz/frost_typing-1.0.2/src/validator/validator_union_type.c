#include "validator/validator.h"

static PyObject*
validator_union_type_repr(TypeAdapter* self)
{
    return PyUnicode_FromFormat(
      "Type[%s]", _CAST(PyTypeObject*, self->cls)->tp_name, NULL);
}

TypeAdapter*
TypeAdapter_Create_UnionType(PyObject* hint, PyObject* tp)
{
    PyObject* type_args = PyTyping_Get_Args(hint);
    if (type_args == NULL) {
        return NULL;
    }

    if (PyTuple_GET_SIZE(type_args) != 1) {
        PyErr_Format(PyExc_TypeError,
                     "Too many arguments for typing.Type "
                     "actual %zu, expected 1",
                     PyTuple_GET_SIZE(type_args));
        Py_DECREF(type_args);
        return NULL;
    }

    PyObject* cls =
      PyEvaluateIfNeeded(PyTuple_GET_ITEM(type_args, 0), (PyTypeObject*)tp);
    if (!cls) {
        Py_DECREF(type_args);
        return NULL;
    }

    if (PyType_Check(cls)) {
        TypeAdapter* res = TypeAdapter_Create(cls,
                                            NULL,
                                            NULL,
                                            validator_union_type_repr,
                                            Not_Converter,
                                            Inspector_IsSubclass);
        Py_DECREF(type_args);
        Py_DECREF(cls);
        return res;
    }

    _RaiseInvalidType("Type[...]", "type", Py_TYPE(cls)->tp_name);
    Py_DECREF(cls);
    Py_DECREF(type_args);
    return NULL;
}