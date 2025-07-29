#include "valid_model.h"
#include "data_model.h"
#include "field.h"
#include "hash_table.h"
#include "meta_valid_model.h"
#include "validator/validator.h"
#include "vector_dict.h"
#include "json/json.h"

static void
valid_model_dealloc(ValidModel* self)
{
    Py_XDECREF(self->ctx);
    DataModelType.head.ht_type.tp_dealloc((PyObject*)self);
}

static inline int
valida_model_init_val(PyObject** restrict slots,
                      Schema* restrict sc,
                      ValidationError** restrict err,
                      ValidateContext* restrict ctx,
                      InitGetter getter,
                      PyObject* arg)
{
    if (!IS_FIELD_INIT(sc->field->flags)) {
        return _DataModel_SetDefault(_CAST(Schema*, sc)->field, slots);
    }

    PyObject *val, *name = SCHEMA_GET_NAME(sc);
    if (!arg || !(val = getter(arg, name))) {
        int r = _DataModel_SetDefault(_CAST(Schema*, sc)->field, slots);
        if (r) {
            return r;
        }

        PyObject* input_val;
        if (!arg || !VectorDict_Check(arg)) {
            input_val = arg;
        } else {
            input_val = _VectorDict_GetDict((_VectorDict*)arg);
            if (!input_val) {
                return -1;
            }
        }
        return ValidationError_CreateMissing(name, input_val, ctx->model, err);
    }

    TypeAdapter* validator = _Schema_GET_VALIDATOR(sc);
    PyObject* tmp = TypeAdapter_Conversion(validator, ctx, val);
    if (!tmp) {
        int r = ValidationError_Create(name, validator, val, ctx->model, err);
        Py_DECREF(val);
        return r;
    }

    Py_DECREF(val);
    Py_XDECREF(*slots);
    *slots = tmp;
    return 0;
}

static int
valid_model_universal_init(PyObject* self, InitGetter getter, PyObject* kwargs)
{
    ValidationError* err = NULL;
    PyTypeObject* tp = Py_TYPE(self);
    ValidateContext ctx = _VALID_MODEL_GET_CTX(self);
    PyObject** restrict slots = DATA_MODEL_GET_SLOTS(self);
    SchemaForeach(sc, tp, slots++)
    {
        if (valida_model_init_val(slots, sc, &err, &ctx, getter, kwargs) < 0) {
            Py_XDECREF(err);
            return -1;
        }
    }

    if (err) {
        ValidationError_RaiseWithModel(err, ctx.model);
        return -1;
    }
    return 0;
}

static inline int
valid_model_init_from_attributes(PyObject* self, PyObject* obj)
{
    if (PyDict_Check(obj)) {
        return valid_model_universal_init(self, _Dict_GetAscii, obj);
    }
    return valid_model_universal_init(self, _Object_Gettr, obj);
}

static int
valid_model_init(PyObject* self, PyObject* args, PyObject* kwargs)
{
    Py_ssize_t size = PyTuple_GET_SIZE(args);
    if (!kwargs && size == 1) {
        kwargs = PyTuple_GET_ITEM(args, 0);
        return valid_model_init_from_attributes(self, kwargs);
    }

    if (!PyCheck_MaxArgs("__init__", size, 0)) {
        return -1;
    }

    if (valid_model_universal_init(self, _Dict_GetAscii, kwargs) < 0) {
        return -1;
    }

    MetaModel* meta = _CAST_META(Py_TYPE(self));
    if (IS_FAIL_ON_EXTRA_INIT(meta->config->flags)) {
        return HashTable_CheckExtraDict(meta->lookup_table,
                                        kwargs,
                                        _CAST(PyTypeObject*, meta)->tp_name,
                                        "__init__");
    }
    return 0;
}

static int
valid_model_vec_init(PyObject* self,
                     PyObject* const* args,
                     size_t nargsf,
                     PyObject* kwnames)
{
    Py_ssize_t size = PyVectorcall_NARGS(nargsf);
    if (!kwnames && size == 1) {
        return valid_model_init_from_attributes(self, (PyObject*)*args);
    }

    if (!PyCheck_ArgsCnt("__init__", size, 0)) {
        return -1;
    }

    if (!VectorCall_CheckKwStrOnly(kwnames)) {
        return -1;
    }

    _VectorDict vd = _VectorDict_Create(args, nargsf, kwnames);
    int r = valid_model_universal_init(self, _VectorDict_Get, (PyObject*)&vd);
    Py_DECREF(&vd);
    if (r < 0) {
        return -1;
    }

    MetaModel* meta = _CAST_META(Py_TYPE(self));
    if (IS_FAIL_ON_EXTRA_INIT(meta->config->flags)) {
        return HashTable_CheckExtraKwnames(meta->lookup_table,
                                           kwnames,
                                           _CAST(PyTypeObject*, meta)->tp_name,
                                           "__init__");
    }
    return 0;
}

static PyObject*
valid_model_from_attributes(PyTypeObject* cls, PyObject* obj)
{
    PyObject* self = cls->tp_new(cls, VoidTuple, NULL);
    if (!self || !PyObject_TypeCheck(self, cls)) {
        return self;
    }

    if (valid_model_init_from_attributes(self, obj) < 0 ||
        _MetaModel_CallPostInit(self) < 0) {
        Py_DECREF(self);
        return NULL;
    }
    return self;
}

static inline void
valid_model_set_ctx(PyObject* self, ContextManager* ctx)
{
    PyObject* tp = (PyObject*)Py_TYPE(self);
    if (ctx->model != tp) {
        ctx = _CAST(MetaValidModel*, tp)->ctx;
    }
    _CAST(ValidModel*, self)->ctx = (ContextManager*)Py_NewRef(ctx);
}

PyObject*
_ValidModel_FrostValidate(PyTypeObject* cls, PyObject* val, ContextManager* ctx)
{
    if (Py_IS_TYPE(val, cls) && !_CAST(MetaValidModel*, cls)->gtypes) {
        return Py_NewRef(val);
    }

    PyObject* self = cls->tp_new(cls, VoidTuple, NULL);
    if (!self || !PyObject_TypeCheck(self, cls)) {
        return self;
    }

    valid_model_set_ctx(self, ctx);
    if (valid_model_init_from_attributes(self, val) < 0 ||
        _MetaModel_CallPostInit(self) < 0) {
        Py_DECREF(self);
        return NULL;
    }
    return self;
}

static PyObject*
valid_model_frost_validate(PyTypeObject* cls,
                           PyObject* const* args,
                           Py_ssize_t nargs)
{
    PyObject* val;
    ContextManager* ctx;
    if (_ParseFrostValidate(args, nargs, &val, &ctx) < 0) {
        return NULL;
    }
    return _ValidModel_FrostValidate(cls, val, ctx);
}

static PyObject*
valid_model_from_json(PyTypeObject* cls,
                      PyObject* const* args,
                      size_t nargs,
                      PyObject* kwnames)
{
    Py_ssize_t cnt = PyVectorcall_NARGS(nargs);
    if (!PyCheck_ArgsCnt(".from_json", cnt, 1)) {
        return NULL;
    }

    PyObject* obj = (PyObject*)*args;
    PyObject* dict = JsonParse(obj);
    if (!dict) {
        ValidationError_RaiseInvalidJson(obj, (PyObject*)cls);
        return NULL;
    }

    if (!PyDict_Check(dict)) {
        ValidationError_RaiseModelType((PyObject*)cls, dict);
        Py_DECREF(dict);
        return NULL;
    }

    if (_Dict_MergeKwnames(dict, args + cnt, kwnames) < 0) {
        Py_DECREF(dict);
        return NULL;
    }

    PyObject* res = valid_model_from_attributes(cls, dict);
    Py_DECREF(dict);
    return res;
}

PyObject*
_ValidModel_Construct(PyTypeObject* cls,
                      PyObject* const* args,
                      Py_ssize_t nargs,
                      PyObject* kwnames)
{
    PyObject* self = cls->tp_new(cls, VoidTuple, NULL);
    if (!self || !PyObject_TypeCheck(self, cls)) {
        return self;
    }

    if (DataModelType.vec_init(self, args, nargs, kwnames) < 0 ||
        _MetaModel_CallPostInit(self) < 0) {
        Py_DECREF(self);
        return NULL;
    }
    return self;
}

int
_ValidModel_Setattro(PyObject* self, PyObject* name, PyObject* val)
{
    MetaModel* meta = _CAST_META(Py_TYPE(self));
    if (!Meta_IS_SUBCLASS(meta)) {
        return PyObject_GenericSetAttr(self, name, val);
    }

    const Py_ssize_t offset = HashTable_Get(meta->lookup_table, name);
    if (offset < 0) {
        return PyObject_GenericSetAttr(self, name, val);
    }

    Schema* schema = META_GET_SCHEMA_BY_OFFSET(meta, offset);
    if (IS_FIELD_FROZEN(schema->field->flags)) {
        PyErr_Format(PyExc_AttributeError,
                     "'%.100s' object attribute '%U' is read-only",
                     _CAST(PyTypeObject*, meta)->tp_name,
                     schema->name);
        return -1;
    }

    PyObject** addr = GET_ADDR(self, meta->slot_offset + offset);
    PyObject* old = *addr;
    if (val) {
        PyObject* tmp;
        ValidateContext ctx = _VALID_MODEL_GET_CTX(self);
        tmp = TypeAdapter_Conversion(_Schema_GET_VALIDATOR(schema), &ctx, val);
        if (!tmp) {
            ValidationError_Raise(schema->name,
                                  _Schema_GET_VALIDATOR(schema),
                                  val,
                                  (PyObject*)meta);
            return -1;
        }

        Py_XDECREF(old);
        *addr = tmp;
        return 0;
    }

    if (!old) {
        RETURN_ATTRIBUT_ERROR(self, schema->name, -1);
    }

    Py_DECREF(old);
    *addr = NULL;
    return 0;
}

static PyMethodDef valid_model_methods[] = {
    { "__frost_validate__",
      (PyCFunction)valid_model_frost_validate,
      METH_CLASS | METH_FASTCALL,
      NULL },
    { "from_attributes",
      (PyCFunction)valid_model_from_attributes,
      METH_CLASS | METH_O,
      NULL },
    { "from_json",
      (PyCFunction)valid_model_from_json,
      METH_CLASS | METH_FASTCALL | METH_KEYWORDS,
      NULL },
    { "construct",
      (PyCFunction)_ValidModel_Construct,
      METH_CLASS | METH_FASTCALL | METH_KEYWORDS,
      NULL },
    { NULL }
};

MetaValidModel ValidModelType = {
    .gtypes = NULL,
    .ctx = NULL,
    .head= {
        .slot_offset = (Py_ssize_t)sizeof(ValidModel),
        .vec_init = valid_model_vec_init,
        .head = {
            .ht_type = {
            PyVarObject_HEAD_INIT(&MetaValidModelType, 0)
            .tp_flags =
            Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | TPFLAGS_META_SUBCLASS |
            TPFLAGS_META_VALID_SUBCLASS | Py_TPFLAGS_HAVE_VECTORCALL,
            .tp_vectorcall = (vectorcallfunc)_MetaModel_Vectorcall,
            .tp_dealloc = (destructor)valid_model_dealloc,
            .tp_base = (PyTypeObject *)&DataModelType,
            .tp_name = "frost_typing.ValidModel",
            .tp_setattro = _ValidModel_Setattro,
            .tp_basicsize = sizeof(ValidModel),
            .tp_methods = valid_model_methods,
            .tp_init = valid_model_init,
            }
        },
    },
};

PyObject*
_ValidModel_CtxCall(PyTypeObject* cls,
                    ContextManager* ctx,
                    PyObject* args,
                    PyObject* kwargs,
                    PyObject* obj)
{
    if (obj) {
        PyObject* frost_validate =
          _CAST(MetaValidModel*, cls)->__frost_validate__;
        if (frost_validate == ValidModelType.__frost_validate__) {
            return _ValidModel_FrostValidate(cls, obj, ctx);
        }
        PyObject* const f_args[3] = { (PyObject*)cls, obj, (PyObject*)ctx };
        PyObject* res = PyObject_Vectorcall(frost_validate, f_args, 3, NULL);
        if (!res) {
            ValidationError_ExceptionHandling((PyObject*)ctx, obj);
        }
        return res;
    }

    PyObject* self = cls->tp_new(cls, VoidTuple, NULL);
    if (!self || !PyObject_TypeCheck(self, cls)) {
        return self;
    }

    valid_model_set_ctx(self, ctx);
    if (valid_model_init(self, args, kwargs) < 0 ||
        _MetaModel_CallPostInit(self) < 0) {
        Py_DECREF(self);
        return NULL;
    }
    return self;
}

ValidateContext
_ValidModel_GetCtx(ValidModel* self)
{
    ContextManager* ctx = _CAST(ValidModel*, self)->ctx;
    if (!ctx) {
        ctx = _CAST(MetaValidModel*, Py_TYPE(self))->ctx;
        Py_INCREF(ctx);
        _CAST(ValidModel*, self)->ctx = ctx;
    }
    return ValidateContext_Create(
      ctx, self, ctx, _CTX_CONFIG_GET_FLAGS(_CAST_META(Py_TYPE(self))->config));
}

int
valid_model_setup(void)
{
    Py_SET_TYPE(&ValidModelType, &MetaValidModelType);
    Py_INCREF(DefaultConfigValid);

    ValidModelType.head.config = DefaultConfigValid;
    ValidModelType.head.vec_new = DataModelType.vec_new;
    ValidModelType.head.schemas = Py_NewRef(VoidTuple);
    if (ValidModelType.head.schemas == NULL) {
        return -1;
    }

    if (PyType_Ready((PyTypeObject*)&ValidModelType) < 0) {
        return -1;
    }
    Py_INCREF(&MetaValidModelType);
    Py_SET_TYPE(&ValidModelType, &MetaValidModelType);

    ValidModelType.ctx = ContextManager_CREATE(&ValidModelType);
    if (!ValidModelType.ctx) {
        return -1;
    }

    ValidModelType.head.__copy__ = Py_NewRef(DataModelType.__copy__);
    ValidModelType.head.__as_dict__ = Py_NewRef(DataModelType.__as_dict__);
    ValidModelType.head.__as_json__ = Py_NewRef(DataModelType.__as_json__);
    ValidModelType.__frost_validate__ = _Dict_GetAscii(
      ValidModelType.head.head.ht_type.tp_dict, __frost_validate__);
    if (!ValidModelType.__frost_validate__) {
        return -1;
    }
    return 0;
}

void
valid_model_free(void)
{
    Py_DECREF(&ValidModelType);
}