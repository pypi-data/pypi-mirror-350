#define PY_SSIZE_T_CLEAN
#include "Python.h"
#define _CAST_V_ERROR(o) ((ValidationError*)o)
#define ValidationError_CREATE(n, v, val, s, e)                                \
    ValidationError_Create(n,                                                  \
                           ((TypeAdapter*)v),                                  \
                           ((PyObject*)val),                                   \
                           (PyObject*)s,                                       \
                           ((ValidationError**)e))

#define ValidationError_CREATE_MISSING(n, v, s, e)                             \
    ValidationError_CreateMissing(n, v, (PyObject*)s, ((ValidationError**)e))
typedef struct ConvParams ConvParams;
typedef struct TypeAdapter TypeAdapter;
typedef struct ValidationError
{
    PyBaseExceptionObject base;
    struct ValidationError* next;
    PyObject* msg;
    PyObject* type;
    PyObject* attrs;
    PyObject* model;
    PyObject* input_value;
} ValidationError;

extern PyObject *ValidationErrorType, *FrostUserError;
extern PyTypeObject _ValidationErrorType;
extern int
validation_error_setup(void);
extern void
validation_error_free(void);
extern int
ValidationError_CreateMissing(PyObject*,
                              PyObject*,
                              PyObject*,
                              ValidationError**);
extern int
ValidationError_Raise(PyObject* attr,
                      TypeAdapter* hint,
                      PyObject* val,
                      PyObject* model);
extern int
ValidationError_RaiseModelType(PyObject* model, PyObject* val);
extern int
ValidationError_RaiseInvalidJson(PyObject* val, PyObject* model);
extern int
ValidationError_RaiseFormat(const char*,
                            PyObject*,
                            PyObject*,
                            PyObject*,
                            PyObject*,
                            ...);
extern int
ValidationError_RaiseIndex(Py_ssize_t, TypeAdapter*, PyObject*, PyObject*);
extern int
ValidationError_IndexCreate(Py_ssize_t,
                            TypeAdapter*,
                            PyObject*,
                            PyObject*,
                            ValidationError**);
extern int
ValidationError_CreateAttrIdx(PyObject* attr,
                              Py_ssize_t ind,
                              TypeAdapter* hint,
                              PyObject* val,
                              PyObject* model,
                              ValidationError** activ);
extern int
ValidationError_Create(PyObject*,
                       TypeAdapter*,
                       PyObject*,
                       PyObject*,
                       ValidationError**);
extern void
ValidationError_RaiseWithModel(ValidationError* err, PyObject* model);
extern int
ValidationError_ExceptionHandling(PyObject* model, PyObject* val);
extern PyObject*
_ValidationError_AsList(PyObject* self, ConvParams* params);