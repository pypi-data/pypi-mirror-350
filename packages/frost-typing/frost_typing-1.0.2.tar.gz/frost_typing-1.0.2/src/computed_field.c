#include "computed_field.h"
#include "field.h"
#include "stddef.h"
#include "structmember.h"
#include "utils_common.h"
#include "validator/py_typing.h"

#define REQUIRED_FIELDS                                                        \
    (FIELD_FROZEN | FIELD_FROZEN_TYPE | _FIELD_COMPUTED_FIELD)
#define SUPPORT_FIELD_FLAGS                                                    \
    (FIELD_JSON_SCHEMA_EXTRA | FIELD_REPR | FIELD_HASH | FIELD_DICT |          \
     FIELD_JSON | _FIELD_COMPUTED_FIELD)
#define SUPPORT_FIELD_FLAGS_FULL                                               \
    (SUPPORT_FIELD_FLAGS | FIELD_EXAMPLES | FIELD_TITLE |                      \
     FIELD_SERIALIZATION_ALIAS)

static Field* default_field;

static void
computed_field_dealloc(ComputedField* self)
{
    Py_XDECREF(self->func);
    Py_XDECREF(self->field);
    Py_TYPE(self)->tp_free(self);
}

static PyObject*
computed_field_proxy_call(ComputedField* self,
                          PyObject* const* args,
                          size_t nargsf,
                          PyObject* kwnames)
{
    return PyObject_Vectorcall(self->func, args, nargsf, kwnames);
}

static PyObject*
computed_field_set_func(ComputedField* self,
                        PyObject* const* args,
                        size_t nargs,
                        PyObject* kwn)
{
    self->func = _VectorCall_GetFuncArg("computed_field", args, nargs, kwn);
    if (!self->func) {
        return NULL;
    }

    self->vectorcall = (vectorcallfunc)computed_field_proxy_call;
    return Py_NewRef(self);
}

static PyObject*
computed_field_new(PyTypeObject* cls, PyObject* args, PyObject* kw)
{
    PyObject* func = NULL;
    Field* field = NULL;

    char* kwlist[] = { "field", NULL };
    if (!PyArg_ParseTupleAndKeywords(
          args, kw, "O!:computed_field.__new__", kwlist, &FieldType, &field)) {
        return NULL;
    }

    ComputedField* self = (ComputedField*)cls->tp_alloc(cls, 0);
    if (!self) {
        return NULL;
    }

    self->vectorcall = (vectorcallfunc)computed_field_set_func;
    self->field = (Field*)Py_XNewRef(field);
    self->func = Py_XNewRef(func);
    return (PyObject*)self;
}

static PyObject*
computed_field_repr(ComputedField* self)
{
    if (self->func) {
        return PyObject_Repr(self->func);
    }
    return PyUnicode_FromFormat("computed_field(field=%R)",
                                self->field ? self->field : default_field);
}

static PyMemberDef computed_field_members[] = {
    { "__func__", T_OBJECT, offsetof(ComputedField, func), READONLY },
    { "field", T_OBJECT, offsetof(ComputedField, field), READONLY },
    { NULL }
};

PyTypeObject ComputedFieldType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_flags =
      Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_VECTORCALL,
    .tp_vectorcall_offset = offsetof(ComputedField, vectorcall),
    .tp_dealloc = (destructor)computed_field_dealloc,
    .tp_repr = (reprfunc)computed_field_repr,
    .tp_name = "frost_typing.computed_field",
    .tp_basicsize = sizeof(ComputedField),
    .tp_members = computed_field_members,
    .tp_call = PyVectorcall_Call,
    .tp_new = computed_field_new,
};

int
computed_field_setup(void)
{
    default_field =
      Field_Create(SUPPORT_FIELD_FLAGS, FIELD_FULL & ~FIELD_VALUES);
    if (!default_field) {
        return -1;
    }
    return PyType_Ready(&ComputedFieldType);
}

void
computed_field_free(void)
{
    Py_DECREF(default_field);
}

static inline PyObject*
computed_field_get_return_type(ComputedField* self)
{
    PyObject* annot = PyFunction_GetAnnotations(self->func);
    if (!annot) {
        return Py_NewRef(PyAny);
    }
    PyObject* res = _PyDict_GetItem_Ascii(annot, __return);
    return Py_NewRef(res ? res : PyAny);
}

PyObject*
ComputedField_GetAnnotated(ComputedField* self)
{
    if (!self->func) {
        PyErr_SetString(PyExc_ValueError,
                        "There is no function for computed_field");
        return NULL;
    }

    PyObject* type = computed_field_get_return_type(self);
    if (!type) {
        return NULL;
    }

    Field* field = self->field ? self->field : default_field;
    uint32_t falgs = field->flags & SUPPORT_FIELD_FLAGS_FULL;
    Field* new_field =
      _Field_CreateComputed((falgs | REQUIRED_FIELDS), field, (PyObject*)self);
    if (!new_field) {
        Py_DECREF(type);
        return NULL;
    }

    PyObject* key = PyTuple_Pack(2, type, new_field);
    Py_DECREF(new_field);
    Py_DECREF(type);
    if (key == NULL) {
        return NULL;
    }

    PyObject* res = PyObject_GetItem(PyAnnotated, key);
    Py_DECREF(key);
    return res;
}
