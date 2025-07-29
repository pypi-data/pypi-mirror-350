#include "meta_valid_model.h"
#include "field.h"
#include "stddef.h"
#include "valid_model.h"
#include "validator/validator.h"

static void
meta_valid_model_dealloc(MetaValidModel* self)
{
    Py_XDECREF(self->ctx);
    Py_XDECREF(self->gtypes);
    Py_XDECREF(self->__frost_validate__);
    MetaModelType.tp_dealloc((PyObject*)self);
}

static int
meta_model_set_field(MetaValidModel* self)
{
    PyObject* par = PyObject_GetAttrString((PyObject*)self, "__parameters__");
    if (par) {
        if (!PyTuple_Check(par)) {
            _RaiseInvalidType("__parameters__", "tuple", Py_TYPE(par)->tp_name);
            Py_DECREF(par);
            return -1;
        }

        if (!PyTuple_GET_SIZE(par)) {
            Py_CLEAR(par);
        }
    } else {
        PyErr_Clear();
    }

    self->gtypes = par;
    self->ctx = _ContextManager_New((PyObject*)self,
                                    (ContextManagerCall)_ValidModel_CtxCall);
    if (!self->ctx) {
        return -1;
    }
    return _MetaModel_SetFunc((MetaModel*)self,
                              __frost_validate__,
                              (PyObject*)_CAST(PyTypeObject*, self)->tp_base,
                              offsetof(MetaValidModel, __frost_validate__));
}

static PyObject*
meta_valid_model_new(PyTypeObject* type, PyObject* args, PyObject* kwargs)
{
    if (PyTuple_GET_SIZE(args) == 1) {
        return _CAST(PyObject*, Py_TYPE(PyTuple_GET_ITEM(args, 0)));
    }

    MetaModel* self =
      MetaModel_New(type, args, kwargs, (SchemaCreate)ValidSchema_Create);
    if (!self) {
        return NULL;
    }

    if (!PyType_IsSubtype((PyTypeObject*)self,
                          (PyTypeObject*)&ValidModelType)) {
        Py_DECREF(self);
        PyErr_SetString(PyExc_TypeError,
                        "The MetaValidModel can only create instances "
                        "of the ValidModel subtype.");
        return NULL;
    }

    _CAST(PyTypeObject*, self)->tp_flags |= TPFLAGS_META_VALID_SUBCLASS;
    if (meta_model_set_field((MetaValidModel*)self) < 0 ||
        FieldValidator_CheckRegistered((PyObject*)self)) {
        Py_DECREF(self);
        return NULL;
    }

    _CAST(PyTypeObject*, self)->tp_setattro = _ValidModel_Setattro;
    return (PyObject*)self;
}

static int
meta_valid_model_traverse(MetaValidModel* self, visitproc visit, void* arg)
{
    if (!(_CAST(PyTypeObject*, self)->tp_flags & Py_TPFLAGS_HEAPTYPE)) {
        return 0;
    }
    Py_VISIT(self->ctx);
    Py_VISIT(self->gtypes);
    return MetaModelType.tp_traverse((PyObject*)self, visit, arg);
}

static int
meta_valid_model_clear(MetaValidModel* self)
{
    if (!(_CAST(PyTypeObject*, self)->tp_flags & Py_TPFLAGS_HEAPTYPE)) {
        return 0;
    }
    Py_CLEAR(self->ctx);
    Py_CLEAR(self->gtypes);
    return MetaModelType.tp_clear((PyObject*)self);
}

static PyObject*
valid_model_subscript(MetaValidModel* cls, PyObject* key)
{
    if (!_MetaModel_IsInit((PyTypeObject*)cls)) {
        return NULL;
    }

    return _ContextManager_CreateGetItem(
      (PyObject*)cls,
      cls->gtypes,
      key,
      (ContextManagerCall)_ValidModel_CtxCall);
}

PyMappingMethods meta_valid_model_as_mapping = {
    .mp_subscript = (binaryfunc)valid_model_subscript
};

PyTypeObject MetaValidModelType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_flags =
      Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_TYPE_SUBCLASS |
      Py_TPFLAGS_HAVE_GC,
    .tp_traverse = (traverseproc)meta_valid_model_traverse,
    .tp_dealloc = (destructor)meta_valid_model_dealloc,
    .tp_as_mapping = &meta_valid_model_as_mapping,
    .tp_clear = (inquiry)meta_valid_model_clear,
    .tp_name = "frost_typing.MetaValidModel",
    .tp_basicsize = sizeof(MetaValidModel),
    .tp_new = meta_valid_model_new,
};

void
meta_valid_model_free()
{
    Py_DECREF(&MetaValidModelType);
}

int
meta_valid_model_setup()
{
    MetaValidModelType.tp_base = &MetaModelType;
    return PyType_Ready(&MetaValidModelType);
}
