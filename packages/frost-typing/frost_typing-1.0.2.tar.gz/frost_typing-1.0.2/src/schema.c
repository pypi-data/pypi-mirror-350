#include "convector.h"
#include "data_model.h"
#include "field.h"
#include "field_serializer.h"
#include "json_schema.h"
#include "meta_model.h"
#include "stddef.h"
#include "structmember.h"
#include "valid_model.h"
#include "validated_func.h"
#include "validator/validator.h"

Schema *WeakRefSchema, *DictSchema;

static Schema*
schema_create(PyTypeObject* cls,
              PyObject* name,
              PyObject* type,
              Field* field,
              PyObject* value,
              PyObject* tp,
              Field* config)
{
    PyUnicode_InternInPlace(&name);
    PyObject* serializer = tp ? FieldSerializer_RegisteredPop(tp, name) : NULL;
    if (!serializer) {
        serializer = Field_GET_SERIALIZER(field);
    }

    field = _Field_SetConfig(field, config, name, serializer);
    Py_XDECREF(serializer);
    if (!field) {
        return NULL;
    }

    Schema* self = (Schema*)cls->tp_alloc(cls, 0);
    if (!self) {
        return NULL;
    }
    self->field = field;
    self->name = Py_NewRef(name);
    self->type = Py_NewRef(type);
    self->value = Py_XNewRef(value);
    return self;
}

Schema*
Schema_Create(PyObject* name,
              PyObject* type,
              Field* field,
              PyObject* value,
              PyObject* tp,
              Field* config)
{
    return schema_create(&SchemaType, name, type, field, value, tp, config);
}

static inline int
is_validate(Field* config, PyObject* name)
{
    return !Unicode_IsPrivate(name) ||
           IF_FIELD_CHECK(config, FIELD_VALIDATE_PRIVATE);
}

int
valid_schema_set_validator(ValidSchema* self, Field* config, PyObject* tp)
{
    PyObject* hint = is_validate(config, self->schema_base.name)
                       ? self->schema_base.type
                       : PyAny;
    self->validator = ParseHintAndName(hint, tp, self->schema_base.name);
    return self->validator ? 0 : -1;
}

ValidSchema*
ValidSchema_Create(PyObject* name,
                   PyObject* type,
                   Field* field,
                   PyObject* value,
                   PyObject* tp,
                   Field* config)
{
    ValidSchema* schema = (ValidSchema*)schema_create(
      &ValidSchemaType, name, type, field, value, tp, config);
    if (!schema) {
        return NULL;
    }
    if (valid_schema_set_validator(schema, config, tp) < 0) {
        Py_DECREF(schema);
        return NULL;
    }
    return schema;
}

Schema*
Schema_Copy(Schema* self,
            Field* field,
            PyObject* value,
            PyObject* tp,
            Field* config)
{
    Schema* schema = schema_create(
      Py_TYPE(self), self->name, self->type, field, value, tp, config);
    if (!schema) {
        return NULL;
    }

    if (!Py_IS_TYPE(schema, &ValidSchemaType)) {
        return schema;
    }

    if (!Py_IS_TYPE(self, &ValidSchemaType)) {
        if (valid_schema_set_validator((ValidSchema*)schema, config, tp) < 0) {
            Py_DECREF(schema);
            return NULL;
        }
        return schema;
    }

    TypeAdapter* vd = _TypeAdapter_Create_FieldValidator(
      _CAST_VALID_SCHEMA(self)->validator, tp, self->name);
    if (!vd) {
        Py_DECREF(schema);
        return NULL;
    }
    _CAST_VALID_SCHEMA(schema)->validator = vd;
    return schema;
}

static void
schema_dealloc(Schema* self)
{
    Py_DECREF(self->name);
    Py_DECREF(self->type);
    Py_DECREF(self->field);
    Py_XDECREF(self->value);
    Py_TYPE(self)->tp_free(self);
}

static void
valid_schema_dealloc(ValidSchema* self)
{
    Py_XDECREF(self->validator);
    schema_dealloc((Schema*)self);
}

static PyObject*
schema_repr(Schema* self)
{
    return PyUnicode_FromFormat("%.100s(name='%S', type=%S, field=%S)",
                                Py_TYPE(self)->tp_name,
                                self->name,
                                self->type,
                                self->field);
}

static PyObject*
valid_schema_repr(ValidSchema* self)
{
    return PyUnicode_FromFormat(
      "%.100s(name='%S', type=%S, field=%S, validator=%S)",
      Py_TYPE(self)->tp_name,
      self->schema_base.name,
      self->schema_base.type,
      self->schema_base.field,
      self->validator);
}

static PyMemberDef schema_members[] = {
    { "name", T_OBJECT, offsetof(Schema, name), READONLY },
    { "type", T_OBJECT, offsetof(Schema, type), READONLY },
    { "field", T_OBJECT, offsetof(Schema, field), READONLY },
    { NULL }
};

PyTypeObject SchemaType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_dealloc = (destructor)schema_dealloc,
    .tp_name = "frost_typing.Schema",
    .tp_repr = (reprfunc)schema_repr,
    .tp_basicsize = sizeof(Schema),
    .tp_members = schema_members,
};

static PyMemberDef valid_schema_members[] = {
    { "validator", T_OBJECT, offsetof(ValidSchema, validator), READONLY },
    { NULL }
};

PyTypeObject ValidSchemaType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_dealloc = (destructor)valid_schema_dealloc,
    .tp_repr = (reprfunc)valid_schema_repr,
    .tp_name = "frost_typing.ValidSchema",
    .tp_basicsize = sizeof(ValidSchema),
    .tp_members = valid_schema_members,
    .tp_base = &SchemaType,
};

int
_Schema_GetValue(Schema* self, PyObject* obj, PyObject** addr, int missing_ok)
{
    Field* field = self->field;
    if (IF_FIELD_CHECK(field, _FIELD_COMPUTED_FIELD)) {
        PyObject* func = _Field_GetAttr(field, _FIELD_COMPUTED_FIELD);
        if (!func) {
            goto missing;
        }
        *addr = PyObject_CallOneArg(func, obj);
        return *addr ? 1 : -1;
    }

    if (IF_FIELD_CHECK(field, FIELD_CLASS_LOOKUP)) {
        if (self->value) {
            *addr = self->value;
            return 1;
        }
    }

missing:
    *addr = NULL;
    if (missing_ok) {
        return 0;
    }
    RETURN_ATTRIBUT_ERROR(obj, self->name, -1);
}

static inline Field*
field_inheritance(Field* activ, Field* new)
{
    if (!activ) {
        Py_INCREF(new);
        return new;
    }

    Field* res = Field_Inheritance(new, activ);
    Py_DECREF(activ);
    return res;
}

static int
get_field_in_annotated(PyObject* hint, Field** res)
{
    if (!Py_IS_TYPE(hint, (PyTypeObject*)Py_AnnotatedAlias)) {
        *res = NULL;
        return 0;
    }

    Field* activ = NULL;
    PyObject* metadata = PyTyping_Get_Metadata(hint);
    if (!metadata) {
        goto error;
    }

    Py_ssize_t size = PyTuple_GET_SIZE(metadata);
    for (Py_ssize_t i = 0; i != size; i++) {
        PyObject* hint = PyTuple_GET_ITEM(metadata, i);
        if (Field_Check(hint)) {
            activ = field_inheritance(activ, _CAST_FIELD(hint));
            if (!activ) {
                goto error;
            }
        } else if (Py_IS_TYPE(hint, (PyTypeObject*)Py_AnnotatedAlias)) {
            Field* tmp;
            int r = get_field_in_annotated(hint, &tmp);
            if (r < 0) {
                Py_XDECREF(activ);
                goto error;
            } else if (r) {
                activ = field_inheritance(activ, tmp);
                if (!activ) {
                    goto error;
                }
            }
        }
    }

    *res = activ;
    Py_DECREF(metadata);
    return activ ? 1 : 0;

error:
    *res = NULL;
    Py_XDECREF(metadata);
    return -1;
}

static Schema*
create_schema_from_annot(PyTypeObject* tp,
                         PyObject* name,
                         PyObject* hint,
                         PyObject* value,
                         Field* default_field,
                         Field* config,
                         SchemaCreate schema_create)
{
    Field* field;
    int r = get_field_in_annotated(hint, &field);
    if (r < 0) {
        return NULL;
    } else if (!r) {
        field = Unicode_IsPrivate(name) ? DefaultFieldPrivate : default_field;
        Py_INCREF(field);
    }

    Schema* res =
      schema_create(name, hint, field, value, (PyObject*)tp, config);
    Py_DECREF(field);
    return res;
}

static inline Schema*
copy_existing_schema(PyTypeObject* tp,
                     Schema* old,
                     PyObject* value,
                     Field* config)
{
    Field* field;
    int r = get_field_in_annotated(old->type, &field);
    if (r < 0) {
        return NULL;
    } else if (!r) {
        field = _CAST_FIELD(Py_NewRef(old->field));
    }

    Schema* res = Schema_Copy(
      old, field, value ? value : old->value, (PyObject*)tp, config);
    Py_DECREF(field);
    return res;
}

Py_ssize_t
Schema_GetArgsCnt(PyObject* schemas)
{
    Py_ssize_t cnt = 0;
    for (Py_ssize_t i = 0; i != PyTuple_GET_SIZE(schemas); i++) {
        Schema* sc = (Schema*)PyTuple_GET_ITEM(schemas, i);
        cnt += !IS_FIELD_KW_ONLY(sc->field->flags);
    }
    return cnt;
}

PyObject*
Schema_CreateTuple(PyObject* base_schemas,
                   SchemaCreate create_fn,
                   PyObject* annotations,
                   PyTypeObject* tp,
                   Field* field,
                   Field* config,
                   PyObject* defaults)
{
    Py_ssize_t ind = 0, copied = 0;
    Py_ssize_t base_count = PyTuple_GET_SIZE(base_schemas);
    Py_ssize_t total = base_count + PyDict_GET_SIZE(annotations);

    const int include_dict =
      !tp ? 0
          : TYPE_DICT_OFFSET(tp) != TYPE_DICT_OFFSET(tp->tp_base) &&
              TYPE_DICT_OFFSET(tp) > 0;
    const int include_weak =
      !tp ? 0
          : TYPE_WEAK_OFFSET(tp) != TYPE_WEAK_OFFSET(tp->tp_base) &&
              TYPE_WEAK_OFFSET(tp) > 0;

    total += include_dict + include_weak;

    PyObject* res = PyTuple_New(total);
    if (!res) {
        return NULL;
    }

    Schema* schema;
    for (; ind < base_count; ++ind) {
        Schema* old_schema = (Schema*)PyTuple_GET_ITEM(base_schemas, ind);
        PyObject* hint = _PyDict_GetItem_Ascii(annotations, old_schema->name);
        PyObject* value = _PyDict_GetItem_Ascii(defaults, old_schema->name);

        if (hint) {
            ++copied;
            if (PyDict_DelItem(annotations, old_schema->name) < 0) {
                goto error;
            }
            schema = create_schema_from_annot(
              tp, old_schema->name, hint, value, field, config, create_fn);
        } else {
            schema = copy_existing_schema(tp, old_schema, value, config);
        }

        if (!schema) {
            goto error;
        }

        PyTuple_SET_ITEM(res, ind, (PyObject*)schema);
    }

    if (copied) {
        if (_PyTuple_Resize(&res, total - copied) < 0) {
            goto error;
        }
    }

    if (include_weak) {
        PyTuple_SET_ITEM(res, ind++, Py_NewRef(WeakRefSchema));
    }

    if (include_dict) {
        PyTuple_SET_ITEM(res, ind++, Py_NewRef(DictSchema));
    }

    PyObject *key, *hint;
    Py_ssize_t pos = 0;
    while (PyDict_Next(annotations, &pos, &key, &hint)) {
        if (!CheckValidityOfAttribute(key)) {
            goto error;
        }

        PyObject* value = PyDict_GetItem(defaults, key);
        schema = create_schema_from_annot(
          tp, key, hint, value, field, config, create_fn);
        if (!schema) {
            goto error;
        }

        PyTuple_SET_ITEM(res, ind++, (PyObject*)schema);
    }

    return res;

error:
    Py_DECREF(res);
    return NULL;
}

int
schema_setup(void)
{
    SchemaType.tp_flags |= Py_TPFLAGS_BASETYPE;
    if (PyType_Ready(&SchemaType) < 0) {
        return -1;
    }
    SchemaType.tp_flags ^= Py_TPFLAGS_BASETYPE;

    if (PyType_Ready(&ValidSchemaType) < 0) {
        return -1;
    }

    WeakRefSchema =
      Schema_Create(__weakref__, PyAny, VoidField, NULL, NULL, DefaultConfig);
    if (WeakRefSchema == NULL) {
        return -1;
    }

    DictSchema =
      Schema_Create(__dict__, PyAny, VoidField, NULL, NULL, DefaultConfig);
    if (DictSchema == NULL) {
        return -1;
    }
    return 0;
}

void
schema_free(void)
{
    Py_DECREF(WeakRefSchema);
    Py_DECREF(DictSchema);
}