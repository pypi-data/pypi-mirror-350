#define PY_SSIZE_T_CLEAN
#include "Python.h"

#define _CAST_FUNC_VALIDATOR(o) _CAST(ValidatedFunc*, o)

#define ValidatedFunc_Check(op)                                                \
    PyType_IsSubtype(Py_TYPE(op), &ValidatedFuncType)
#define ValidatedFunc_CheckExact(op) Py_IS_TYPE((op), &ValidatedFuncType)

typedef struct TypeAdapter TypeAdapter;
typedef struct ValidModel ValidModel;

typedef struct FuncSchema
{
    TypeAdapter* validator;
    PyObject* name;
    PyObject* type;
} FuncSchema;

typedef struct
{
    ValidModel head;
    Py_ssize_t size;
    PyObject* gtypes;
    FuncSchema* validators;
    FuncSchema a_validator;
    FuncSchema r_validator;
    PyFunctionObject* func;
    vectorcallfunc vectorcall;
} ValidatedFunc;

extern PyTypeObject ValidatedFuncType;
extern int
validated_func_setup(void);
extern void
validated_func_free(void);
extern ValidatedFunc*
ValidatedFunc_Create(PyTypeObject*, PyFunctionObject*);