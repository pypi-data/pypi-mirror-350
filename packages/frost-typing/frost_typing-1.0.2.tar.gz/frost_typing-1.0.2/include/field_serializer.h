#define PY_SSIZE_T_CLEAN
#include "Python.h"

#define FieldSerializer_Check(op)                                              \
    PyType_IsSubtype(Py_TYPE(op), &FieldSerializerType)
#define FieldSerializer_CheckExact(op) Py_IS_TYPE((op), &FieldSerializerType)

typedef struct
{
    PyObject_HEAD PyObject* func;
    vectorcallfunc vectorcall;
    PyObject* fields_name;
} FieldSerializer;

extern PyTypeObject FieldSerializerType;
extern int
field_serializer_setup(void);
extern void
field_serializer_free(void);
extern int
FieldSerializer_CheckRegistered(PyObject*);
extern PyObject*
FieldSerializer_RegisteredPop(PyObject*, PyObject*);