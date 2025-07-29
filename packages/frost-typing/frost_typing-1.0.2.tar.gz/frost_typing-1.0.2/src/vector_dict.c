#include "vector_dict.h"
#include "utils_common.h"

void
vector_dict_dealloc(_VectorDict* self)
{
    Py_XDECREF(self->_dict);
}

PyTypeObject _VectorDictType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_dealloc = (destructor)vector_dict_dealloc,
    .tp_name = "frost_typing.VectorDict",
    .tp_basicsize = sizeof(_VectorDict),

};

inline _VectorDict
_VectorDict_Create(PyObject* const* args, size_t nargsf, PyObject* kwnames)
{
    Py_INCREF(&_VectorDictType);
    return (_VectorDict){ .ob_base.ob_refcnt = 1,
                          .ob_base.ob_type = &_VectorDictType,
                          .args = args + PyVectorcall_NARGS(nargsf),
                          .kwnames = kwnames,
                          ._dict = NULL };
}

PyObject*
_VectorDict_Get(PyObject* self, PyObject* string)
{
    _VectorDict* this = (_VectorDict*)self;
    if (!this->kwnames) {
        return NULL;
    }

    Py_hash_t hash = _Hash_String(string);
    PyObject** names = TUPLE_ITEMS(this->kwnames);
    Py_ssize_t key_len = PyUnicode_GetLength(string);
    Py_ssize_t size = PyTuple_GET_SIZE(this->kwnames);

    for (Py_ssize_t i = 0; i != size; i++) {
        PyObject* name = names[i];
        if (name == string ||
            (key_len == PyUnicode_GetLength(name) &&
             _Hash_String(name) == hash &&
             !memcmp(PyUnicode_DATA(name), PyUnicode_DATA(string), key_len))) {
            return Py_NewRef(this->args[i]);
        }
    }
    return NULL;
}

PyObject*
_VectorDict_GetDict(_VectorDict* self)
{
    if (self->_dict) {
        return self->_dict;
    }

    PyObject* dict = PyDict_New();
    if (!dict) {
        return NULL;
    }

    if (self->kwnames) {
        Py_ssize_t size = PyTuple_GET_SIZE(self->kwnames);
        for (Py_ssize_t i = 0; i != size; i++) {
            PyObject* name = PyTuple_GET_ITEM(self->kwnames, i);
            if (Dict_SetItem_String(dict, name, self->args[i]) < 0) {
                Py_DECREF(dict);
                return NULL;
            }
        }
    }

    self->_dict = dict;
    return dict;
}

int
vector_dict_setup(void)
{
    return PyType_Ready(&_VectorDictType);
}

void
vector_dict_free(void)
{
}