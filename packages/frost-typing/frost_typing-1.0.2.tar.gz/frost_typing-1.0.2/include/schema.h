#define PY_SSIZE_T_CLEAN
#include "Python.h"

#define SCHEMA_GET_SNAME(a, s)                                                 \
    (a && IF_FIELD_CHECK(s->field, FIELD_SERIALIZATION_ALIAS))                 \
      ? Field_GET_SERIALIZATION_ALIAS(s->field)                                \
      : s->name

#define SCHEMA_GET_NAME(s)                                                     \
    !IF_FIELD_CHECK(s->field, FIELD_ALIAS) ? s->name : Field_GET_ALIAS(s->field)

#define SCHEMA_GET_VALUE(s, obj, addr) _Schema_GetValue(s, obj, addr, 0)
#define _CAST_VALID_SCHEMA(s) _CAST(ValidSchema*, s)

typedef struct Field Field;
typedef struct Schema
{
    PyObject_HEAD Field* field;
    PyObject* name;
    PyObject* type;
    PyObject* value;
} Schema;

typedef struct TypeAdapter TypeAdapter;
typedef struct ValidSchema
{
    Schema schema_base;
    TypeAdapter* validator;
} ValidSchema;

typedef Schema* (*SchemaCreate)(PyObject* name,
                                PyObject* type,
                                Field* field,
                                PyObject* value,
                                PyObject* tp,
                                Field* config);

extern PyTypeObject SchemaType, ValidSchemaType;
extern Schema *WeakRefSchema, *DictSchema;
extern Schema*
Schema_Create(PyObject* name,
              PyObject* type,
              Field* field,
              PyObject* value,
              PyObject* tp,
              Field* config);
extern ValidSchema*
ValidSchema_Create(PyObject* name,
                   PyObject* type,
                   Field* field,
                   PyObject* value,
                   PyObject* tp,
                   Field* config);
extern Schema*
Schema_Copy(Schema* self,
            Field* field,
            PyObject* value,
            PyObject* tp,
            Field* config);
extern Py_ssize_t
Schema_GetArgsCnt(PyObject* schemas);
extern PyObject*
Schema_CreateTuple(PyObject* base_schemas,
                   SchemaCreate create_fn,
                   PyObject* annotations,
                   PyTypeObject* tp,
                   Field* field,
                   Field* config,
                   PyObject* defaults);
extern int
_Schema_GetValue(Schema* self, PyObject* obj, PyObject** addr, int missing_ok);
extern int
schema_setup(void);
extern void
schema_free(void);
