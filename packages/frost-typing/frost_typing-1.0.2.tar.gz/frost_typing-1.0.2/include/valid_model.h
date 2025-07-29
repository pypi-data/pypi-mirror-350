#define PY_SSIZE_T_CLEAN
#include "Python.h"

#define _VALID_MODEL_GET_CTX(s) _ValidModel_GetCtx((ValidModel*)s)

typedef struct MetaValidModel MetaValidModel;
typedef struct ValidateContext ValidateContext;
typedef struct ContextManager ContextManager;

typedef struct ValidModel
{
    PyObject_HEAD ContextManager* ctx;
} ValidModel;

extern MetaValidModel ValidModelType;
PyObject*
_ValidModel_CtxCall(PyTypeObject* cls,
                    ContextManager* ctx,
                    PyObject* args,
                    PyObject* kwargs,
                    PyObject* obj);
extern int
_ValidModel_Setattro(PyObject* self, PyObject* name, PyObject* val);
extern ValidateContext
_ValidModel_GetCtx(ValidModel* self);
extern PyObject*
_ValidModel_Construct(PyTypeObject* cls,
                      PyObject* const* args,
                      Py_ssize_t nargs,
                      PyObject* kwnames);
extern PyObject*
_ValidModel_FrostValidate(PyTypeObject* cls,
                          PyObject* val,
                          ContextManager* ctx);
extern int
valid_model_setup(void);
extern void
valid_model_free(void);