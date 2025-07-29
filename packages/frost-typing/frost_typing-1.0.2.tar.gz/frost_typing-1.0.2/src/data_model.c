#include "data_model.h"
#include "context_manager.h"
#include "convector.h"
#include "field.h"
#include "hash_table.h"
#include "json_schema.h"
#include "meta_valid_model.h"
#include "utils_common.h"
#include "valid_model.h"
#include "vector_dict.h"
#include "json/json.h"

static PyObject*
data_model_new(PyTypeObject* cls,
               UNUSED PyObject* args,
               UNUSED PyObject* kwargs)
{
    return _MetaModel_IsInit(cls) ? cls->tp_alloc(cls, 0) : NULL;
}

static PyObject*
data_model_vec_new(PyTypeObject* cls,
                   UNUSED PyObject* const* args,
                   UNUSED size_t nargsf,
                   UNUSED PyObject* kwnames)
{
    return _MetaModel_IsInit(cls) ? cls->tp_alloc(cls, 0) : NULL;
}

static inline void
data_model_raise_missing(const char* func_name, PyObject* names)
{
    _PyUnicodeWriter writer;
    _PyUnicodeWriter_Init(&writer);
    writer.overallocate = 1;
    writer.min_length = 32;

    Py_ssize_t cnt = PyTuple_GET_SIZE(names);
    _UNICODE_WRITE_STRING(&writer, func_name, -1);
    _UNICODE_WRITE_STRING(&writer, "() missing ", 11);

    _UNICODE_WRITE_SSIZE(&writer, PyList_GET_SIZE(names));
    _UNICODE_WRITE_STRING(&writer, " required positional arguments: ", 32);

    for (Py_ssize_t i = 0; i != cnt; i++) {
        if (i && _PyUnicodeWriter_WriteASCIIString(&writer, " and ", 5) < 0) {
            goto error;
        }

        _UNICODE_WRITE_CHAR(&writer, '\'');
        if (_PyUnicodeWriter_WriteStr(&writer, PyList_GET_ITEM(names, i)) < 0) {
            goto error;
        }
        _UNICODE_WRITE_CHAR(&writer, '\'');
    }

    PyObject* res = _PyUnicodeWriter_Finish(&writer);
    if (res) {
        PyErr_SetObject(PyExc_TypeError, res);
        Py_DECREF(res);
    }
    return;

error:
    _PyUnicodeWriter_Dealloc(&writer);
}

static inline void
data_model_missing(Schema** schemas,
                   Schema** end_schemas,
                   InitGetter getter,
                   PyObject* arg,
                   const char* func_name)
{
    PyObject* names = PyList_New(0);
    if (!names) {
        return;
    }

    for (Schema* sc = *schemas; schemas != end_schemas; sc = *++schemas) {
        if (!IS_FIELD_INIT(sc->field->flags) ||
            IF_FIELD_CHECK(sc->field, FIELD_DEFAULT) ||
            IF_FIELD_CHECK(sc->field, FIELD_DEFAULT_FACTORY)) {
            continue;
        }

        PyObject* name = SCHEMA_GET_NAME(sc);
        PyObject* val = arg ? getter(arg, name) : NULL;
        Py_XDECREF(val);
        if (val) {
            continue;
        }

        if (PyList_Append(names, name) < 0) {
            Py_DECREF(names);
            return;
        }
    };

    data_model_raise_missing(func_name, names);
    Py_DECREF(names);
}

static int
valid_model_universal_init(PyObject* self,
                           InitGetter getter,
                           PyObject* const* args,
                           Py_ssize_t args_cnt,
                           PyObject* kw,
                           const char* f_name)
{
    PyTypeObject* tp = Py_TYPE(self);
    if (!PyCheck_MaxArgs(f_name, args_cnt, _CAST_META(tp)->args_only)) {
        return -1;
    }

    PyObject *name, *val, *const *args_end, **slots;

    args_end = args + args_cnt;
    slots = DATA_MODEL_GET_SLOTS(self);
    SchemaForeach(schema, tp, slots++)
    {
        const uint32_t flags = schema->field->flags;
        if (!IS_FIELD_INIT(flags)) {
            if (_DataModel_SetDefault(schema->field, slots) < 0) {
                return -1;
            }
            continue;
        }

        name = SCHEMA_GET_NAME(schema);
        val = kw ? getter(kw, name) : NULL;
        if ((args != args_end) && !IS_FIELD_KW_ONLY(flags)) {
            if (val) {
                Py_DECREF(val);
                PyErr_Format(
                  PyExc_TypeError,
                  "%.100s.%.100s() got multiple values for argument '%U'",
                  tp->tp_name,
                  f_name,
                  name);
                return -1;
            }
            val = Py_NewRef(*args++);
        }

        if (val) {
            Py_XDECREF(*slots);
            *slots = val;
            continue;
        }

        int r = _DataModel_SetDefault(schema->field, slots);
        if (r == -1) {
            return -1;
        } else if (!r) {
            data_model_missing(__schema, __end_schema, getter, kw, f_name);
            return -1;
        }
    }
    return 0;
}

static int
data_model_init(PyObject* self, PyObject* args, PyObject* kwargs)
{
    if (valid_model_universal_init(self,
                                   _Dict_GetAscii,
                                   TUPLE_ITEMS(args),
                                   PyTuple_GET_SIZE(args),
                                   kwargs,
                                   "__init__") < 0) {
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
data_model_vec_init(PyObject* self,
                    PyObject* const* args,
                    size_t nargsf,
                    PyObject* kwnames)
{
    if (!VectorCall_CheckKwStrOnly(kwnames)) {
        return -1;
    }

    _VectorDict vd = _VectorDict_Create(args, nargsf, kwnames);
    if (valid_model_universal_init(self,
                                   _VectorDict_Get,
                                   args,
                                   PyVectorcall_NARGS(nargsf),
                                   (PyObject*)&vd,
                                   "__init__") < 0) {
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

static int
data_model_init_from_attributes(PyObject* self, PyObject* obj)
{
    if (PyDict_Check(obj)) {
        return valid_model_universal_init(
          self, _Dict_GetAscii, NULL, 0, obj, "from_attributes");
    }

    if (Py_TYPE(obj)->tp_dictoffset) {
        PyObject** addr_dict = _PyObject_GetDictPtr(obj);
        if (addr_dict) {
            return valid_model_universal_init(
              self, _Dict_GetAscii, NULL, 0, *addr_dict, "from_attributes");
        }
    }
    return valid_model_universal_init(
      self, _Object_Gettr, NULL, 0, obj, "from_attributes");
}

static PyObject*
data_model_repr(PyObject* self)
{
    _PyUnicodeWriter writer;
    PyTypeObject* tp = Py_TYPE(self);
    int r = Py_ReprEnter(self);
    if (r) {
        return r > 0 ? PyUnicode_FromFormat("%.100s(...)", tp->tp_name) : NULL;
    }

    _PyUnicodeWriter_Init(&writer);
    writer.overallocate = 1;
    writer.min_length = 64;

    if (MetaValid_IS_SUBCLASS(tp) && _CAST(ValidModel*, self)->ctx) {
        if (_ContextManager_ReprModel(
              &writer, (PyObject*)_CAST(ValidModel*, self)->ctx) < 0) {
            goto error;
        }
    } else {
        _UNICODE_WRITE_STRING(&writer, tp->tp_name, -1);
    }

    Py_ssize_t cnt = 0;
    PyObject** slots = DATA_MODEL_GET_SLOTS(self);
    _UNICODE_WRITE_CHAR(&writer, '(');
    SchemaForeach(schema, tp, slots++)
    {
        if (!IS_FIELD_REPR(schema->field->flags)) {
            continue;
        }
        if (cnt) {
            _UNICODE_WRITE_STRING(&writer, ", ", 2);
        }

        PyObject* val = *slots;
        if (!val) {
            if (SCHEMA_GET_VALUE(schema, self, slots) < 0) {
                goto error;
            }
            val = *slots;
        }
        cnt++;
        _UNICODE_WRITE_STR(&writer, schema->name);
        _UNICODE_WRITE_CHAR(&writer, '=');
        _UNICODE_WRITE(&writer, val, PyObject_Repr);
    }

    _UNICODE_WRITE_CHAR(&writer, ')');

    Py_ReprLeave(self);
    return _PyUnicodeWriter_Finish(&writer);

error:
    _PyUnicodeWriter_Dealloc(&writer);
    Py_ReprLeave(self);
    return NULL;
}

static Py_hash_t
data_model_hash(PyObject* self)
{
    PyObject *val, **slots;
    PyTypeObject* tp = Py_TYPE(self);
    Py_hash_t acc = _PyHASH_XXPRIME_5;

    slots = DATA_MODEL_GET_SLOTS(self);
    SchemaForeach(schema, tp, slots++)
    {
        if (!IS_FIELD_HASH(schema->field->flags)) {
            continue;
        }
        val = *slots;
        if (!val) {
            if (SCHEMA_GET_VALUE(schema, self, slots) < 0) {
                return -1;
            }
            val = *slots;
        }
        Py_hash_t lane = PyObject_Hash(val);
        if (lane == -1 && PyErr_Occurred()) {
            return -1;
        }
        acc += lane * _PyHASH_XXPRIME_2;
        acc = _PyHASH_XXROTATE(acc);
        acc *= _PyHASH_XXPRIME_1;
    }
    acc += META_GET_SIZE(tp) ^ (_PyHASH_XXPRIME_5 ^ 3527539UL);
    if (acc == (Py_hash_t)-1) {
        return 1546275797;
    }
    return acc;
}

static PyObject*
data_model_richcompare(PyObject* self, PyObject* other, int op)
{
    MetaModel *meta, *o_meta;
    PyObject **slots, **o_slots;
    PyObject *val, *o_val;

    meta = _CAST_META(Py_TYPE(self));
    o_meta = _CAST_META(Py_TYPE(other));
    if (o_meta != meta) {
        if (op == Py_NE) {
            Py_RETURN_TRUE;
        }
        Py_RETURN_FALSE;
    }

    o_slots = DATA_MODEL_GET_SLOTS(other);
    slots = DATA_MODEL_GET_SLOTS(self);
    SchemaForeach(schema, meta, slots++, o_slots++)
    {
        if (!IS_FIELD_COMPARISON(schema->field->flags)) {
            continue;
        }

        val = *slots;
        if (!val) {
            if (SCHEMA_GET_VALUE(schema, self, slots) < 0) {
                return NULL;
            }
            val = *slots;
        }
        o_val = *o_slots;
        if (!o_val) {
            if (SCHEMA_GET_VALUE(schema, other, o_slots) < 0) {
                return NULL;
            }
            o_val = *o_slots;
        }

        int r = PyObject_RichCompareBool(val, o_val, op);
        if (r < 0) {
            return NULL;
        }
        if (r == 0) {
            Py_RETURN_FALSE;
        }
    }
    Py_RETURN_TRUE;
}

static PyObject*
data_model__as_dict__nested(PyObject* self,
                            ConvParams* params,
                            PyObject* include,
                            PyObject* exclude,
                            uint32_t exclude_flag)
{
    if (!ConvecotrEnterRecCall(params)) {
        return NULL;
    }

    PyObject* dict = PyDict_New();
    if (!dict) {
        return NULL;
    }

    PyTypeObject* tp = Py_TYPE(self);
    PyObject** slots = DATA_MODEL_GET_SLOTS(self);
    SchemaForeach(sc, tp, slots++)
    {
        if (!IF_FIELD_CHECK(sc->field, exclude_flag)) {
            continue;
        }

        if (exclude && exclude != Py_None) {
            int r = PySet_Contains(exclude, sc->name);
            if (r < 0) {
                goto error;
            }
            if (r) {
                continue;
            }
        }

        if (include && include != Py_None) {
            int r = PySet_Contains(include, sc->name);
            if (r < 0) {
                goto error;
            }
            if (!r) {
                continue;
            }
        }

        PyObject* val = *slots;
        if (!val) {
            int r = _Schema_GetValue(sc, self, slots, params->exclude_unset);
            if (r < 0) {
                goto error;
            } else if (!r) {
                continue;
            }
            val = *slots;
        }

        if (params->exclude_none && val == Py_None) {
            continue;
        }

        PyObject* serializer = Field_GET_SERIALIZER(sc->field);
        if (!serializer) {
            val = params->conv(val, params);
        } else {
            PyObject* const args[2] = { self, val };
            PyObject* tmp = PyObject_Vectorcall(serializer, args, 2, NULL);
            if (!tmp) {
                goto error;
            }

            val = params->conv(tmp, params);
            Py_DECREF(tmp);
        }

        if (!val) {
            goto error;
        }

        PyObject* name = SCHEMA_GET_SNAME(params->by_alias, sc);
        if (PyDict_SetItemStringDecrefVal(dict, name, val) < 0) {
            goto error;
        }
    }

    return dict;

error:
    Py_DECREF(dict);
    return NULL;
}

static PyObject*
data_model__as_dict__(PyObject* self)
{
    ConvParams conv_params = ConvParams_Create(AsDict);
    return data_model__as_dict__nested(
      self, &conv_params, NULL, NULL, FIELD_DICT);
}

static PyObject*
data_model_as_dict(PyObject* self, PyObject* args, PyObject* kwargs)
{
    if (!_PyArg_NoPositional("as_dict", args)) {
        return NULL;
    }

    char* kwlist[] = { "as_json",       "include",      "exclude", "by_alias",
                       "exclude_unset", "exclude_none", NULL };
    ConvParams params = ConvParams_Create(AsDict);
    PyObject *include = NULL, *exclude = NULL;
    char as_json = 0;

    if (kwargs && !PyArg_ParseTupleAndKeywords(VoidTuple,
                                               kwargs,
                                               "|pOOppp:as_dict",
                                               kwlist,
                                               &as_json,
                                               &include,
                                               &exclude,
                                               &params.by_alias,
                                               &params.exclude_unset,
                                               &params.exclude_none)) {
        return NULL;
    }

    if (as_json) {
        params.conv = AsDictJson;
    }

    if (Convector_ValidateInclue(include, exclude) < 0) {
        return NULL;
    }
    return _DataModel_AsDict(self, &params, include, exclude);
}

PyObject*
_DataModel_AsDict(PyObject* self,
                  ConvParams* params,
                  PyObject* include,
                  PyObject* exclude)
{
    PyTypeObject* tp = Py_TYPE(self);
    PyObject* as_dict = _CAST_META(tp)->__as_dict__;
    if (as_dict == DataModelType.__as_dict__) {
        return data_model__as_dict__nested(
          self, params, include, exclude, FIELD_DICT);
    }

    if (!as_dict) {
        return PyErr_Format(
          PyExc_TypeError,
          "The '__as_dict__' method is not defined for '%.100s'",
          tp->tp_name);
    }

    PyObject* res = PyObject_CallOneArg(as_dict, self);
    if (res && !PyDict_Check(res)) {
        PyErr_Format(PyExc_TypeError,
                     "The '__as_dict__' method of the should "
                     "return dict, but returned '%.100S'",
                     Py_TYPE(res)->tp_name);
        Py_DECREF(res);
        return NULL;
    }
    return res;
}

static PyObject*
data_model__copy__(PyObject* self)
{
    PyTypeObject* tp = Py_TYPE(self);
    PyObject *duplicate, **c_slots;
    ConvParams conv_params = ConvParams_Create(Copy);
    duplicate = tp->tp_alloc(tp, 0);
    if (!duplicate) {
        return NULL;
    }

    if (MetaValid_IS_SUBCLASS(tp)) {
        Py_XINCREF(_CAST(ValidModel*, self)->ctx);
        _CAST(ValidModel*, duplicate)->ctx = _CAST(ValidModel*, self)->ctx;
    }

    c_slots = DATA_MODEL_GET_SLOTS(duplicate);
    DataModelForeach(slots, self, c_slots++)
    {
        PyObject* val = *slots;
        if (!val) {
            continue;
        }

        val = Copy(val, &conv_params);
        if (val == NULL) {
            Py_DECREF(duplicate);
            return NULL;
        }
        *c_slots = val;
    }

    if (tp->tp_dictoffset) {
        PyObject **addr_dict, *dict, *copy_dict;
        addr_dict = _PyObject_GetDictPtr(self);
        if (!addr_dict || !(dict = *addr_dict)) {
            return duplicate;
        }

        copy_dict = Copy(dict, &conv_params);
        if (!copy_dict) {
            Py_DECREF(duplicate);
            return NULL;
        }

        addr_dict = _PyObject_GetDictPtr(duplicate);
        Py_XDECREF(*addr_dict);
        *addr_dict = copy_dict;
    }
    return duplicate;
}

PyObject*
_DataModel_Copy(PyObject* self)
{
    PyTypeObject* tp = Py_TYPE(self);
    PyObject* copy = _CAST_META(tp)->__copy__;
    if (copy == DataModelType.__copy__) {
        return data_model__copy__(self);
    }

    if (!copy) {
        return PyErr_Format(PyExc_TypeError,
                            "The '__copy__' method is not defined for '%.100s'",
                            tp->tp_name);
    }

    PyObject* res = PyObject_CallOneArg(copy, self);
    if (res && !Py_IS_TYPE(res, tp)) {
        PyErr_Format(PyExc_TypeError,
                     "The '__copy__' method of the '%.100s' "
                     "class returned a different type '%.100s'",
                     tp->tp_name,
                     Py_TYPE(res)->tp_name);
        Py_DECREF(res);
        return NULL;
    }
    return res;
}

static PyObject*
data_model_from_attributes(PyTypeObject* cls, PyObject* obj)
{
    PyObject* self = cls->tp_new(cls, VoidTuple, NULL);
    if (!self || !PyObject_TypeCheck(self, cls)) {
        return self;
    }

    if (data_model_init_from_attributes(self, obj) < 0 ||
        _MetaModel_CallPostInit(self) < 0) {
        Py_DECREF(self);
        return NULL;
    }
    return self;
}

static PyObject*
data_model_from_json(PyTypeObject* cls,
                     PyObject* const* args,
                     size_t nargs,
                     PyObject* kwnames)
{
    Py_ssize_t cnt = PyVectorcall_NARGS(nargs);
    if (!PyCheck_ArgsCnt(".from_json", cnt, 1)) {
        return NULL;
    }

    PyObject* dict = JsonParse((PyObject*)*args);
    if (!dict) {
        return NULL;
    }

    if (!PyDict_Check(dict)) {
        PyErr_SetString(PyExc_TypeError, "JSON must be dict");
        Py_DECREF(dict);
        return NULL;
    }

    if (_Dict_MergeKwnames(dict, args + cnt, kwnames) < 0) {
        Py_DECREF(dict);
        return NULL;
    }

    PyObject* res = data_model_from_attributes(cls, dict);
    Py_DECREF(dict);
    return res;
}

static void
data_model_dealloc(PyObject* self)
{
    PyTypeObject* tp = Py_TYPE(self);
    if (PyType_SUPPORTS_WEAKREFS(tp)) {
        PyObject_ClearWeakRefs(self);
    }

    PyObject_GC_UnTrack(self);
    Py_TRASHCAN_BEGIN(self, data_model_dealloc);
    DataModelForeach(slots, self)
    {
        Py_XDECREF(*slots);
    }

    if (tp->tp_dictoffset) {
        PyObject** addr_dict = _PyObject_GetDictPtr(self);
        if (addr_dict) {
            Py_XDECREF(*addr_dict);
        }
    }

    Py_TYPE(self)->tp_free(self);
    Py_TRASHCAN_END;
}

static int
data_model_clear(PyObject* self)
{
    DataModelForeach(slots, self)
    {
        Py_CLEAR(*slots);
    }

    if (Py_TYPE(self)->tp_dictoffset) {
        PyObject** addr_dict = _PyObject_GetDictPtr(self);
        if (!addr_dict) {
            return 0;
        }
        Py_CLEAR(*addr_dict);
    }
    return 0;
}

static int
data_model_traverse(PyObject* self, visitproc visit, void* arg)
{
    DataModelForeach(slots, self)
    {
        Py_VISIT(*slots);
    }

    if (Py_TYPE(self)->tp_dictoffset) {
        PyObject** addr_dict = _PyObject_GetDictPtr(self);
        if (!addr_dict) {
            return 0;
        }
        Py_VISIT(*addr_dict);
    }
    return 0;
}

static PyObject*
data_model__as_json__(PyObject* self)
{
    ConvParams params = ConvParams_Create(AsDict);
    return data_model__as_dict__nested(self, &params, NULL, NULL, FIELD_JSON);
}

static PyObject*
data_model_as_json(PyObject* self, PyObject* args, PyObject* kwargs)
{
    if (!_PyArg_NoPositional("as_json", args)) {
        return NULL;
    }
    return _MetaModel_AsJsonCall(self, kwargs);
}

PyObject*
_DataModel_Getattro(PyObject* self, PyObject* name)
{
    MetaModel* meta = _CAST_META(Py_TYPE(self));
    const Py_ssize_t offset = HashTable_Get(meta->lookup_table, name);
    if (offset < 0) {
        return PyObject_GenericGetAttr(self, name);
    }

    PyObject** addr = GET_ADDR(self, meta->slot_offset + offset);
    if (*addr) {
        return Py_NewRef(*addr);
    }

    Schema* schema = META_GET_SCHEMA_BY_OFFSET(meta, offset);
    _Schema_GetValue(schema, self, addr, 0);
    return Py_XNewRef(*addr);
}

int
_DataModel_Setattro(PyObject* self, PyObject* name, PyObject* val)
{
    MetaModel* meta = _CAST_META(Py_TYPE(self));
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

    PyObject** addr = GET_ADDR(self, (meta->slot_offset + offset));
    PyObject* old = *addr;
    if (val) {
        Py_XDECREF(old);
        *addr = Py_NewRef(val);
        return 0;
    }

    if (!old) {
        RETURN_ATTRIBUT_ERROR(self, schema->name, -1);
    }

    Py_DECREF(old);
    *addr = NULL;
    return 0;
}

static PyObject*
data_model_get_item(PyObject* self, PyObject* name)
{
    MetaModel* meta = _CAST_META(Py_TYPE(self));
    const Py_ssize_t offset = HashTable_Get(meta->lookup_table, name);
    if (offset < 0) {
        PyErr_SetObject(PyExc_KeyError, name);
        return NULL;
    }

    PyObject** addr = GET_ADDR(self, meta->slot_offset + offset);
    if (*addr) {
        return Py_NewRef(*addr);
    }

    Schema* schema = META_GET_SCHEMA_BY_OFFSET(meta, offset);
    int r = _Schema_GetValue(schema, self, addr, 1);
    if (r < 0) {
        return NULL;
    } else if (!r) {
        PyErr_SetObject(PyExc_KeyError, name);
        return NULL;
    }

    return Py_NewRef(*addr);
}

static PyObject*
data_model_keys(PyObject* self)
{
    PyTypeObject* tp = Py_TYPE(self);
    PyObject* res = PyList_New(META_GET_SIZE(tp));
    if (!res) {
        return NULL;
    }

    Py_ssize_t i = 0;
    SchemaForeach(sc, tp)
    {
        if (IS_FIELD_DICT(sc->field->flags)) {
            PyList_SET_ITEM(res, i++, Py_NewRef(sc->name));
        }
    }

    Py_SET_SIZE(res, i);
    return res;
}

static PyObject*
data_model__setstate__(PyObject* self, PyObject* state)
{
    if (!PyDict_Check(state)) {
        return _RaiseInvalidType("state", "dict", Py_TYPE(state)->tp_name);
    }

    if (data_model_init(self, VoidTuple, state) < 0) {
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyObject*
data_model__getstate__(PyObject* self)
{
    PyObject* dict = PyDict_New();
    if (!dict) {
        return NULL;
    }

    PyObject** slots = DATA_MODEL_GET_SLOTS(self);
    SchemaForeach(sc, Py_TYPE(self), slots++)
    {
        PyObject* val = *slots;
        if (!val) {
            int r = _Schema_GetValue(sc, self, slots, 0);
            if (r < 0) {
                goto error;
            }

            val = *slots;
        }

        if (Dict_SetItem_String(dict, sc->name, val) < 0) {
            goto error;
        }
    }

    return dict;

error:
    Py_DECREF(dict);
    return NULL;
}

static PyMethodDef data_model_methods[] = {
    { "keys", (PyCFunction)data_model_keys, METH_NOARGS, NULL },
    { "from_attributes",
      (PyCFunction)data_model_from_attributes,
      METH_CLASS | METH_O,
      NULL },
    { "from_json",
      (PyCFunction)data_model_from_json,
      METH_CLASS | METH_FASTCALL | METH_KEYWORDS,
      NULL },
    { "as_dict",
      (PyCFunction)data_model_as_dict,
      METH_VARARGS | METH_KEYWORDS,
      NULL },
    { "__setstate__", (PyCFunction)data_model__setstate__, METH_O, NULL },
    { "__getstate__", (PyCFunction)data_model__getstate__, METH_NOARGS, NULL },
    { "__as_dict__", (PyCFunction)data_model__as_dict__, METH_NOARGS, NULL },
    { "__as_json__", (PyCFunction)data_model__as_json__, METH_NOARGS, NULL },
    { "as_json",
      (PyCFunction)data_model_as_json,
      METH_VARARGS | METH_KEYWORDS,
      NULL },
    { "__copy__", (PyCFunction)data_model__copy__, METH_NOARGS, NULL },
    { "copy", (PyCFunction)_DataModel_Copy, METH_NOARGS, NULL },
    { "json_schema",
      (PyCFunction)Schema_JsonSchema,
      METH_CLASS | METH_NOARGS,
      NULL },
    { NULL }
};

PyMappingMethods data_model_as_mapping = {
    .mp_subscript = data_model_get_item,
};

MetaModel DataModelType = {
    .vec_init = data_model_vec_init,
    .vec_new = data_model_vec_new,
    .slot_offset = SIZE_OBJ,
    .head = {
        .ht_type = {
            PyVarObject_HEAD_INIT((PyTypeObject*)&MetaModelType,
                                                 0)
            .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE |
            Py_TPFLAGS_HAVE_GC | TPFLAGS_META_SUBCLASS |
            Py_TPFLAGS_HAVE_VECTORCALL,
            .tp_vectorcall = (vectorcallfunc)_MetaModel_Vectorcall,
            .tp_richcompare = data_model_richcompare,
            .tp_as_mapping = &data_model_as_mapping,
            .tp_name = "frost_typing.DataModel",
            .tp_traverse = data_model_traverse,
            .tp_getattro = _DataModel_Getattro,
            .tp_setattro = _DataModel_Setattro,
            .tp_methods = data_model_methods,
            .tp_dealloc = data_model_dealloc,
            .tp_alloc = PyType_GenericAlloc,
            .tp_clear = data_model_clear,
            .tp_init = data_model_init,
            .tp_repr = data_model_repr,
            .tp_free = PyObject_GC_Del,
            .tp_hash = data_model_hash,
            .tp_new = data_model_new,
        },
    },
};

int
_DataModel_SetDefault(Field* field, PyObject** res)
{
    PyObject* val;
    if (IF_FIELD_CHECK(field, FIELD_DEFAULT_FACTORY)) {
        val = PyObject_CallNoArgs(Field_GET_DEFAULT_FACTORY(field));
    } else {
        val = _Field_GetAttr(field, FIELD_DEFAULT);
        if (!val) {
            return 0;
        }

        val = IF_FIELD_CHECK(field, _FIELD_CONST_DEFAULT) ? Py_NewRef(val)
                                                          : CopyNoKwargs(val);
    }

    if (!val) {
        return -1;
    }
    Py_XDECREF(*res);
    *res = val;
    return 1;
}

void
data_model_free(void)
{
    Py_DECREF(&DataModelType);
}

int
data_model_setup(void)
{
    DataModelType.config = (Field*)Py_NewRef((PyObject*)DefaultConfig);
    DataModelType.schemas = Py_NewRef(VoidTuple);
    Py_SET_TYPE(&DataModelType, &MetaModelType);
    if (PyType_Ready((PyTypeObject*)&DataModelType) < 0) {
        return -1;
    }

    Py_INCREF(&MetaModelType);
    Py_SET_TYPE(&DataModelType, &MetaModelType);

    PyObject* dict = DataModelType.head.ht_type.tp_dict;
    DataModelType.__copy__ = _Dict_GetAscii(dict, __copy__);
    if (!DataModelType.__copy__) {
        return -1;
    }

    DataModelType.__as_dict__ = _Dict_GetAscii(dict, __as_dict__);
    if (!DataModelType.__as_dict__) {
        return -1;
    }

    DataModelType.__as_json__ = _Dict_GetAscii(dict, __as_json__);
    if (!DataModelType.__as_json__) {
        return -1;
    }
    return 0;
}
