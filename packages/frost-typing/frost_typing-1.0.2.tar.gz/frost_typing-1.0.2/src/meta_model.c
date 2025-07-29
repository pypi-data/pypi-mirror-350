#include "alias_generator.h"
#include "computed_field.h"
#include "data_model.h"
#include "field.h"
#include "field_serializer.h"
#include "hash_table.h"
#include "json_schema.h"
#include "meta_valid_model.h"
#include "structmember.h"
#include "utils_common.h"
#include "validator/py_typing.h"
#include "validator/validation_error.h"

static void
meta_model_dealloc(MetaModel* self)
{
    HashTable_Dealloc(self->lookup_table);
    Py_XDECREF(self->config);
    Py_XDECREF(self->schemas);
    Py_XDECREF(self->__copy__);
    Py_XDECREF(self->__as_json__);
    Py_XDECREF(self->__post_init__);
    PyType_Type.tp_dealloc((PyObject*)self);
}

static int
meta_model_set__slots__(PyObject* dict)
{
    PyObject* slots = _PyDict_GetItem_Ascii(dict, __slots__);
    if (!slots) {
        return PyDict_SetItem(dict, __slots__, VoidTuple);
    }

    if (PyObject_RichCompareBool(__dict__, slots, Py_EQ) ||
        PyObject_RichCompareBool(__weakref__, slots, Py_EQ)) {
        return 0;
    }

    if (!PyTuple_Check(slots)) {
        goto error;
    }

    for (Py_ssize_t i = 0; i < PyTuple_GET_SIZE(slots); i++) {
        PyObject* val = PyTuple_GET_ITEM(slots, i);
        if (!PyObject_RichCompareBool(val, __dict__, Py_EQ) &&
            !PyObject_RichCompareBool(val, __weakref__, Py_EQ)) {
            goto error;
        }
    }
    return 0;

error:
    PyErr_SetString(PyExc_ValueError,
                    "The MetaModel supports __slots__ of the "
                    "tuple type with '__dict__' or '__weakref__'");
    return -1;
}

PyObject*
get_root(PyTypeObject* self)
{
    Py_ssize_t i;
    PyObject *base, *mro = self->tp_mro;
    for (i = 1; i < PyTuple_GET_SIZE(mro); i++) {
        base = PyTuple_GET_ITEM(mro, i);
        if (Meta_IS_SUBCLASS(base)) {
            return base;
        }
    }
    return NULL;
}

static Field*
get_config(MetaModel* root, PyObject* dict)
{
    Field* config = _CAST_FIELD(_PyDict_GetItem_Ascii(dict, __config__));
    if (!config) {
        config = root ? root->config : DefaultConfig;
        Py_INCREF(config);
        return config;
    }

    if (!Config_Check(config)) {
        _RaiseInvalidType("__config__", "Config", Py_TYPE(config)->tp_name);
        return NULL;
    }

    if (root) {
        return Config_Inheritance(config, root->config);
    }

    Py_INCREF(config);
    return config;
}

static inline Field*
copy_config(Field* config)
{
    return Field_Create(config->flags & ~FIELD_VALUES,
                        config->def_flags & ~FIELD_VALUES);
}

int
_MetaModel_SetFunc(MetaModel* self,
                   PyObject* name,
                   PyObject* root,
                   Py_ssize_t offset)
{
    PyObject* func =
      _PyDict_GetItem_Ascii(_CAST(PyTypeObject*, self)->tp_dict, name);
    if (!func) {
        if (!root) {
            return 0;
        }
        func = Py_XNewRef(GET_OBJ(root, offset));
    } else {
        func = _PyObject_Get_Func(func, (const char*)PyUnicode_DATA(name));
        if (!func) {
            return -1;
        }
    }

    SET_OBJ(self, offset, func);
    return 0;
}

static PyObject*
slot_meta_new(PyTypeObject* cls,
              PyObject* const* args,
              size_t nargsf,
              PyObject* kwnames)
{
    PyObject *func, *res;
    func = PyObject_GetAttr((PyObject*)cls, __new__);
    if (!func) {
        return NULL;
    }

    res = _Object_Call_Prepend(func, (PyObject*)cls, args, nargsf, kwnames);
    Py_DECREF(func);
    return res;
}

static int
slot_meta_init(PyObject* self,
               PyObject* const* args,
               size_t nargsf,
               PyObject* kwnames)
{
    PyObject* func = _Object_Gettr((PyObject*)Py_TYPE(self), __init__);
    if (!func) {
        return 0;
    }

    PyObject* res = _Object_Call_Prepend(func, self, args, nargsf, kwnames);
    Py_DECREF(func);
    if (!res) {
        return -1;
    }

    if (res != Py_None) {
        PyErr_Format(PyExc_TypeError,
                     "__init__() should return None, not '%.200s'",
                     Py_TYPE(res)->tp_name);
        Py_DECREF(res);
        return -1;
    }

    Py_DECREF(res);
    return 0;
}

static void
meta_model_set_call(MetaModel* self, PyObject* root)
{
    PyTypeObject* tp = (PyTypeObject*)self;
    tp->tp_flags |= Py_TPFLAGS_HAVE_VECTORCALL;

    if (root && META_GET_SIZE(self) < 14) {
        tp->tp_vectorcall = _CAST(PyTypeObject*, root)->tp_vectorcall;
        self->vec_new = PyDict_Contains(tp->tp_dict, __new__)
                          ? slot_meta_new
                          : _CAST_META(root)->vec_new;
        self->vec_init = PyDict_Contains(tp->tp_dict, __init__)
                           ? slot_meta_init
                           : _CAST_META(root)->vec_init;
    } else {
        tp->tp_vectorcall = PyType_Type.tp_vectorcall;
    }
}

static int
meta_model_set_field(MetaModel* self, PyObject* root)
{
    PyObject* dict = _CAST(PyTypeObject*, self)->tp_dict;
    self->config = get_config((MetaModel*)root, dict);
    if (!self->config) {
        return -1;
    }

    if (_MetaModel_SetFunc(
          self, __as_dict__, root, offsetof(MetaModel, __as_dict__)) < 0) {
        return -1;
    }
    if (_MetaModel_SetFunc(
          self, __post_init__, root, offsetof(MetaModel, __post_init__)) < 0) {
        return -1;
    }
    if (_MetaModel_SetFunc(
          self, __as_json__, root, offsetof(MetaModel, __as_json__)) < 0) {
        return -1;
    }
    if (_MetaModel_SetFunc(
          self, __copy__, root, offsetof(MetaModel, __copy__)) < 0) {
        return -1;
    }
    return 0;
}

static int
meta_model_sub_new(MetaModel* self,
                   MetaModel* root,
                   PyObject* annot,
                   PyObject* dict,
                   SchemaCreate schema_create)
{
    PyTypeObject* tp = (PyTypeObject*)self;
    PyTypeObject* base = tp->tp_base;
    int has_dict_slot = TYPE_DICT_OFFSET(tp) != TYPE_DICT_OFFSET(base) &&
                        TYPE_DICT_OFFSET(tp) > 0;
    int has_weakref_slot = TYPE_WEAK_OFFSET(tp) != TYPE_WEAK_OFFSET(base) &&
                           TYPE_WEAK_OFFSET(tp) > 0;

    Field* default_field = copy_config(self->config);
    if (!default_field) {
        return -1;
    }

    PyObject* base_schemas = root ? _CAST_META(root)->schemas : VoidTuple;
    self->schemas = Schema_CreateTuple(base_schemas,
                                       schema_create,
                                       annot,
                                       tp,
                                       default_field,
                                       self->config,
                                       dict);
    Py_DECREF(default_field);
    if (!self->schemas) {
        return -1;
    }

    self->args_only = Schema_GetArgsCnt(self->schemas);
    /* If the parent is a MetaModel, then it has already calculated offset */
    if (Meta_IS_SUBCLASS(tp->tp_base)) {
        self->slot_offset = META_MODEL_GET_OFFSET(tp->tp_base);
    } else {
        self->slot_offset = tp->tp_basicsize;
    }

    tp->tp_flags |= TPFLAGS_META_SUBCLASS;

    Py_ssize_t total_scs = PyTuple_GET_SIZE(self->schemas);
    Py_ssize_t base_cnt = PyTuple_GET_SIZE(base_schemas);
    Py_ssize_t extra = total_scs - base_cnt - has_weakref_slot - has_dict_slot;

    tp->tp_basicsize += BASE_SIZE * extra;
    self->lookup_table = HashTable_Create(self->schemas);
    return self->lookup_table ? 0 : -1;
}

static PyObject*
meta_model_get_annotations(PyObject* self)
{
    PyObject *annot, *new_annot, *name, *hint;
#if PY_VERSION_HEX < 0x030A0000
    annot = Py_XNewRef(_PyDict_GetItem_Ascii(
      _CAST(PyTypeObject*, self)->tp_dict, __annotations__));
#else
    annot = _Object_Gettr(self, __annotations__);
#endif

    new_annot = PyDict_New();
    if (!new_annot) {
        Py_XDECREF(annot);
        return NULL;
    }

    if (!annot) {
        return new_annot;
    }

    if (!PyDict_Check(annot)) {
        _RaiseInvalidType("__annotations__", "dict", Py_TYPE(annot)->tp_name);
        goto error;
    }

    Py_ssize_t pos = 0;
    while (PyDict_Next(annot, &pos, &name, &hint)) {
        if (PyTyping_Is_Origin(hint, PyClassVar)) {
            continue;
        }

        if (PyDict_SetItem(new_annot, name, hint) < 0) {
            goto error;
        }
    }

    PyObject* dict = _CAST(PyTypeObject*, self)->tp_dict;
    pos = 0;
    while (PyDict_Next(dict, &pos, &name, &hint)) {
        if (!ComputedField_Check(hint)) {
            continue;
        }

        PyObject* annotated = ComputedField_GetAnnotated((ComputedField*)hint);
        if (!annotated) {
            goto error;
        }

        if (PyDict_SetItemDecrefVal(new_annot, name, annotated) < 0) {
            goto error;
        }
    }

    Py_DECREF(annot);
    return new_annot;

error:
    Py_DECREF(new_annot);
    Py_DECREF(annot);
    return NULL;
}

static int
check_bases(PyObject* bases)
{
    Py_ssize_t size = PyTuple_GET_SIZE(bases);
    for (Py_ssize_t i = 0; i != size; i++) {
        PyTypeObject* tp = _CAST(PyTypeObject*, PyTuple_GET_ITEM(bases, 0));
        if (PyType_Check(tp) && !Meta_IS_SUBCLASS(tp) && tp->tp_itemsize) {
            PyErr_Format(PyExc_TypeError,
                         "Not supported for subtype of '%s'",
                         tp->tp_name);
            return -1;
        }
    }
    return 0;
}

MetaModel*
MetaModel_New(PyTypeObject* type,
              PyObject* args,
              PyObject* kwargs,
              SchemaCreate schema_create)
{
    PyObject *name, *bases, *dict, *annot;
    MetaModel* self;
    if (!PyArg_ParseTuple(args,
                          "UO!O!:MetaModel.__new__",
                          &name,
                          &PyTuple_Type,
                          &bases,
                          &PyDict_Type,
                          &dict)) {
        return NULL;
    }

    if (check_bases(bases) < 0) {
        return NULL;
    }

    if (meta_model_set__slots__(dict) < 0) {
        return NULL;
    }

    self = _CAST_META(PyType_Type.tp_new(type, args, kwargs));
    if (!self) {
        return NULL;
    }

    PyObject* root = get_root((PyTypeObject*)self);
    if (meta_model_set_field(self, root) < 0) {
        Py_DECREF(self);
        return NULL;
    }

    annot = meta_model_get_annotations((PyObject*)self);
    if (!annot) {
        Py_DECREF(self);
        return NULL;
    }

    int r =
      meta_model_sub_new(self, (MetaModel*)root, annot, dict, schema_create);
    Py_DECREF(annot);
    if (r < 0) {
        Py_DECREF(self);
        return NULL;
    }

    meta_model_set_call(self, root);
    _CAST(PyTypeObject*, self)->tp_getattro = _DataModel_Getattro;
    _CAST(PyTypeObject*, self)->tp_setattro = _DataModel_Setattro;

    if (FieldSerializer_CheckRegistered((PyObject*)self) < 0) {
        Py_DECREF(self);
        return NULL;
    }
    return self;
}

static PyObject*
meta_model_new(PyTypeObject* type, PyObject* args, PyObject* kwargs)
{
    return (PyObject*)MetaModel_New(type, args, kwargs, Schema_Create);
}

int
_MetaModel_CallPostInit(PyObject* self)
{
    PyTypeObject* tp = Py_TYPE(self);
    PyObject* call = _CAST_META(tp)->__post_init__;
    if (!call) {
        return 0;
    }

    PyObject* res = PyObject_CallOneArg(call, self);
    if (res) {
        Py_DECREF(res);
        return 0;
    }

    if (MetaValid_IS_SUBCLASS(tp)) {
        ValidationError_RaiseModelType((PyObject*)tp, self);
    }
    return -1;
}

static PyObject*
meta_mode_call(PyTypeObject* cls, PyObject* args, PyObject* kwds)
{
    if (!cls->tp_new) {
        return PyErr_Format(
          PyExc_TypeError, "cannot create '%s' instances", cls->tp_name);
    }

    PyObject* self = cls->tp_new(cls, args, kwds);
    if (!self || !PyObject_TypeCheck(self, cls)) {
        return self;
    }

    cls = Py_TYPE(self);
    if ((cls->tp_init && cls->tp_init(self, args, kwds) < 0) ||
        _MetaModel_CallPostInit(self) < 0) {
        Py_DECREF(self);
        return NULL;
    }
    return self;
}

PyObject*
_MetaModel_Vectorcall(MetaModel* cls,
                      PyObject* const* args,
                      size_t nargsf,
                      PyObject* kwnames)
{
    if (!cls->vec_new) {
        return PyErr_Format(PyExc_TypeError,
                            "cannot create '%s' instances",
                            _CAST(PyTypeObject*, cls)->tp_name);
    }

    PyObject* self = cls->vec_new((PyTypeObject*)cls, args, nargsf, kwnames);
    if (!self || !PyObject_TypeCheck(self, (PyTypeObject*)cls)) {
        return self;
    }

    cls = _CAST_META(Py_TYPE(self));
    if ((cls->vec_init && cls->vec_init(self, args, nargsf, kwnames) < 0) ||
        _MetaModel_CallPostInit(self) < 0) {
        Py_DECREF(self);
        return NULL;
    }
    return self;
}

static PyObject*
meta_model_getattro(MetaModel* self, PyObject* name)
{
    if (!Meta_IS_SUBCLASS(self)) {
        return PyType_Type.tp_getattro((PyObject*)self, name);
    }

    const Py_ssize_t offset = HashTable_Get(self->lookup_table, name);
    if (offset < 0) {
        return PyType_Type.tp_getattro((PyObject*)self, name);
    }

    Schema* schema = META_GET_SCHEMA_BY_OFFSET(self, offset);
    if (schema->value) {
        return Py_NewRef(schema->value);
    }

    return PyErr_Format(PyExc_AttributeError,
                        "type object '%.100s' has no attribute '%.100U'",
                        _CAST(PyTypeObject*, self)->tp_name,
                        schema->name);
}

static int
meta_model_setattro(MetaModel* self, PyObject* name, PyObject* val)
{
    if (!Meta_IS_SUBCLASS(self)) {
        return PyType_Type.tp_setattro((PyObject*)self, name, val);
    }

    const Py_ssize_t offset = HashTable_Get(self->lookup_table, name);
    if (offset < 0) {
        return PyType_Type.tp_setattro((PyObject*)self, name, val);
    }

    Schema* schema = META_GET_SCHEMA_BY_OFFSET(self, offset);
    if (IS_FIELD_FROZEN_TYPE(schema->field->flags)) {
        PyErr_Format(PyExc_AttributeError,
                     "'%.100s' type object attribute '%U' is read-only",
                     _CAST(PyTypeObject*, self)->tp_name,
                     schema->name);
        return -1;
    }

    if (val) {
        Py_XDECREF(schema->value);
        schema->value = Py_NewRef(val);
        return 0;
    }

    if (schema->value) {
        Py_DECREF(schema->value);
        schema->value = NULL;
        return 0;
    }

    PyErr_Format(PyExc_AttributeError,
                 "type object '%.100s' has no attribute '%.100U'",
                 _CAST(PyTypeObject*, self)->tp_name,
                 schema->name);
    return -1;
}

static int
meta_model_traverse(MetaModel* self, visitproc visit, void* arg)
{
    if (!(_CAST(PyTypeObject*, self)->tp_flags & Py_TPFLAGS_HEAPTYPE)) {
        return 0;
    }
    Py_VISIT(self->config);
    Py_VISIT(self->schemas);
    return PyType_Type.tp_traverse((PyObject*)self, visit, arg);
}

static int
meta_model_clear(MetaModel* self)
{
    if (!(_CAST(PyTypeObject*, self)->tp_flags & Py_TPFLAGS_HEAPTYPE)) {
        return 0;
    }
    Py_CLEAR(self->config);
    Py_CLEAR(self->schemas);
    return PyType_Type.tp_clear((PyObject*)self);
}

static PyMethodDef meta_model_methods[] = {
    { "json_schema", (PyCFunction)Schema_JsonSchema, METH_NOARGS, NULL },
    { NULL }
};

static PyMemberDef meta_members[] = {
    { "__config__", T_OBJECT, offsetof(MetaModel, config), READONLY },
    { "__schemas__", T_OBJECT, offsetof(MetaModel, schemas), READONLY },
    { "__post_init__", T_OBJECT, offsetof(MetaModel, __post_init__), READONLY },
    { "__as_dict__", T_OBJECT, offsetof(MetaModel, __as_dict__), READONLY },
    { "__as_json__", T_OBJECT, offsetof(MetaModel, __as_json__), READONLY },
    { "__copy__", T_OBJECT, offsetof(MetaModel, __copy__), READONLY },
    { NULL }
};

PyTypeObject MetaModelType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_flags =
      Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_TYPE_SUBCLASS |
      Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_HAVE_VECTORCALL,
    .tp_traverse = (traverseproc)meta_model_traverse,
    .tp_getattro = (getattrofunc)meta_model_getattro,
    .tp_setattro = (setattrofunc)meta_model_setattro,
    .tp_dealloc = (destructor)meta_model_dealloc,
    .tp_call = (ternaryfunc)meta_mode_call,
    .tp_clear = (inquiry)meta_model_clear,
    .tp_name = "frost_typing.MetaModel",
    .tp_basicsize = sizeof(MetaModel),
    .tp_methods = meta_model_methods,
    .tp_members = meta_members,
    .tp_new = meta_model_new,
};

inline int
_MetaModel_IsInit(PyTypeObject* tp)
{
    if (!Meta_IS_SUBCLASS(tp)) {
        PyErr_SetString(PyExc_TypeError,
                        "The model must be created using a MetaModel");
        return 0;
    }
    return 1;
}

int
meta_model_setup()
{
    MetaModelType.tp_base = &PyType_Type;
    Py_INCREF(&PyType_Type);
    return PyType_Ready(&MetaModelType);
}

void
meta_model_free()
{
    Py_DECREF(&MetaModelType);
}
