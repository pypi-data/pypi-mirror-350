#include "module.h"
#include "alias_generator.h"
#include "computed_field.h"
#include "convector.h"
#include "data_model.h"
#include "field.h"
#include "field_serializer.h"
#include "json_schema.h"
#include "meta_valid_model.h"
#include "valid_model.h"
#include "validated_func.h"
#include "validator/discriminator.h"
#include "validator/validator.h"
#include "vector_dict.h"
#include "weakref_cache.h"
#include "json/json.h"

#define PYMODULE_ADD_TYPE(m, tp)                                               \
    if (PyModule_AddType(m, (PyTypeObject*)tp) < 0) {                          \
        return NULL;                                                           \
    }

static PyObject*
copy(UNUSED PyObject* self, PyObject* obj)
{
    return PyCopy(obj);
}

static PyObject*
dumps(UNUSED PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* obj = Parse_OneArgs("dumps", args);
    return obj ? PyObject_AsJson(obj, kwargs) : NULL;
}

static PyObject*
loads(UNUSED PyObject* self, PyObject* obj)
{
    return JsonParse(obj);
}

static PyObject*
as_dict(UNUSED PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject* obj = Parse_OneArgs("as_dict", args);
    if (!obj) {
        return NULL;
    }

    ConvParams params = ConvParams_Create(AsDict);
    char* kwlist[] = { "by_alias", "exclude_unset", "exclude_none", NULL };
    if (kwargs && !PyArg_ParseTupleAndKeywords(VoidTuple,
                                               kwargs,
                                               "|ppp:as_dict",
                                               kwlist,
                                               &params.by_alias,
                                               &params.exclude_unset,
                                               &params.exclude_none)) {
        return NULL;
    }
    return AsDict(obj, &params);
}

static PyObject*
parse_date(UNUSED PyObject* self, PyObject* obj)
{
    return DateTime_ParseDate(obj);
}

static PyObject*
parse_time(UNUSED PyObject* self, PyObject* obj)
{
    return DateTime_ParseTime(obj);
}

static PyObject*
parse_datetime(UNUSED PyObject* self, PyObject* obj)
{
    return DateTime_ParseDateTime(obj);
}

static PyObject*
json_schema(UNUSED PyObject* self, PyObject* obj)
{
    return Schema_JsonSchema(obj);
}

static PyObject*
field(UNUSED PyObject* self, PyObject* args, PyObject* kwargs)
{
    PyObject *type, *field, *res;
    type = Parse_OneArgs("field", args);
    if (!type) {
        return NULL;
    }

    field = PyObject_Call((PyObject*)&FieldType, VoidTuple, kwargs);
    if (!field) {
        return NULL;
    }

    res = PyTyping_AnnotatedGetItem(type, field);
    Py_DECREF(field);
    return res;
}

static PyObject*
create_con(PyTypeObject* type_con, PyObject* args, PyObject* kw, char* err)
{
    PyObject *con, *type, *res;
    type = Parse_OneArgs(err, args);
    if (!type) {
        return NULL;
    }

    con = PyObject_Call((PyObject*)type_con, VoidTuple, kw);
    if (!con) {
        return NULL;
    }

    res = PyTyping_AnnotatedGetItem(type, con);
    Py_DECREF(con);
    return res;
}

static PyObject*
con_sequence(UNUSED PyObject* self, PyObject* args, PyObject* kwargs)
{
    return create_con(&SequenceConstraintsType, args, kwargs, "con_sequence");
}

static PyObject*
con_string(UNUSED PyObject* self, PyObject* args, PyObject* kwargs)
{
    return create_con(&StringConstraintsType, args, kwargs, "con_string");
}

static PyObject*
con_comparison(UNUSED PyObject* self, PyObject* args, PyObject* kwargs)
{
    return create_con(
      &ComparisonConstraintsType, args, kwargs, "con_comparison");
}

static PyMethodDef frost_typing_methods[] = {
    { "copy", (PyCFunction)copy, METH_O, NULL },
    { "dumps", (PyCFunction)dumps, METH_VARARGS | METH_KEYWORDS, NULL },
    { "loads", (PyCFunction)loads, METH_O, NULL },
    { "as_dict", (PyCFunction)as_dict, METH_VARARGS | METH_KEYWORDS, NULL },
    { "parse_date", (PyCFunction)parse_date, METH_O, NULL },
    { "parse_time", (PyCFunction)parse_time, METH_O, NULL },
    { "json_schema", (PyCFunction)json_schema, METH_O, NULL },
    { "parse_datetime", (PyCFunction)parse_datetime, METH_O, NULL },
    { "field", (PyCFunction)field, METH_VARARGS | METH_KEYWORDS, NULL },
    { "con_sequence",
      (PyCFunction)con_sequence,
      METH_VARARGS | METH_KEYWORDS,
      NULL },
    { "con_string",
      (PyCFunction)con_string,
      METH_VARARGS | METH_KEYWORDS,
      NULL },
    { "con_comparison",
      (PyCFunction)con_comparison,
      METH_VARARGS | METH_KEYWORDS,
      NULL },
    { NULL },
};

static void
frost_typing_free(UNUSED void* self)
{
    discriminator_free();
    computed_field_free();
    schema_free();
    json_free();
    field_validator_free();
    field_serializer_free();
    typing_free();
    validation_error_free();
    field_free();
    utils_common_free();
    meta_model_free();
    data_model_free();
    validator_free();
    validated_func_free();
    constraints_free();
    meta_valid_model_free();
    valid_model_free();
    convector_free();
    context_free();
    weakref_cache_free();
    alias_generator_free();
    json_schema_free();
    vector_dict_free();
}

static int
frost_typing_setup(void)
{
    if (discriminator_setup() < 0 || utils_common_setup() < 0 ||
        weakref_cache_setup() < 0 || context_setup() < 0 ||
        field_validator_setup() < 0 || field_serializer_setup() < 0 ||
        typing_setup() < 0 || validation_error_setup() < 0 ||
        field_setup() < 0 || schema_setup() < 0 || meta_model_setup() < 0 ||
        data_model_setup() < 0 || validator_setup() < 0 ||
        validated_func_setup() < 0 || constraints_setup() < 0 ||
        meta_valid_model_setup() < 0 || valid_model_setup() < 0 ||
        convector_setup() < 0 || json_setup() < 0 ||
        computed_field_setup() < 0 || alias_generator_setup() < 0 ||
        json_schema_setup() || vector_dict_setup() < 0) {
        return -1;
    }
    return 0;
}

static PyModuleDef frost_typing = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_methods = frost_typing_methods,
    .m_free = frost_typing_free,
    .m_name = "frost_typing",
    .m_doc = NULL,
    .m_size = -1,
};

PyMODINIT_FUNC
PyInit_frost_typing(void)
{
    PyObject* m;
    if (frost_typing_setup() < 0) {
        return NULL;
    }
    m = PyModule_Create(&frost_typing);
    if (m == NULL) {
        return NULL;
    }
    PYMODULE_ADD_TYPE(m, &MetaModelType);
    PYMODULE_ADD_TYPE(m, &MetaValidModelType);
    PYMODULE_ADD_TYPE(m, &DataModelType);
    PYMODULE_ADD_TYPE(m, &FieldType);
    PYMODULE_ADD_TYPE(m, &ConfigType);
    PYMODULE_ADD_TYPE(m, &ValidModelType);
    PYMODULE_ADD_TYPE(m, ValidationErrorType);
    PYMODULE_ADD_TYPE(m, JsonEncodeError);
    PYMODULE_ADD_TYPE(m, JsonDecodeError);
    PYMODULE_ADD_TYPE(m, FrostUserError);
    PYMODULE_ADD_TYPE(m, &ComparisonConstraintsType);
    PYMODULE_ADD_TYPE(m, &SequenceConstraintsType);
    PYMODULE_ADD_TYPE(m, &StringConstraintsType);
    PYMODULE_ADD_TYPE(m, &ValidatedFuncType);
    PYMODULE_ADD_TYPE(m, &TypeAdapterType);
    PYMODULE_ADD_TYPE(m, &FieldValidatorType);
    PYMODULE_ADD_TYPE(m, &FieldSerializerType);
    PYMODULE_ADD_TYPE(m, &ComputedFieldType);
    PYMODULE_ADD_TYPE(m, &ContextManager_Type);
    PYMODULE_ADD_TYPE(m, &AliasGeneratorType);
    PYMODULE_ADD_TYPE(m, &DiscriminatorType);
    PYMODULE_ADD_TYPE(m, &ValidSchemaType);
    PYMODULE_ADD_TYPE(m, &SchemaType);

    if (PyModule_AddObject(m, "AwareDatetime", AwareDatetime) < 0) {
        return NULL;
    }
    if (PyModule_AddObject(m, "NaiveDatetime", NaiveDatetime) < 0) {
        return NULL;
    }
    if (PyModule_AddObject(m, "PastDatetime", PastDatetime) < 0) {
        return NULL;
    }
    if (PyModule_AddObject(m, "FutureDatetime", FutureDatetime) < 0) {
        return NULL;
    }
    return m;
}