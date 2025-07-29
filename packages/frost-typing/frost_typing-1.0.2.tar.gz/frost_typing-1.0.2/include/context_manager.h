#define PY_SSIZE_T_CLEAN
#include "Python.h"

#define CTX_NUM_ITEMS(c) Py_SIZE(c)
#define ContextManager_Check(o) (Py_TYPE(o) == &ContextManager_Type)
#define ContextManager_CREATE(m) _ContextManager_New((PyObject*)m, NULL)

typedef struct ValidateContext ValidateContext;
typedef struct ContextManager ContextManager;
typedef struct MetaValidModel MetaValidModel;
typedef struct ValidModel ValidModel;
typedef struct TypeAdapter TypeAdapter;

typedef PyObject* (*ContextManagerCall)(PyObject* model,
                                        ContextManager* ctx,
                                        PyObject* args,
                                        PyObject* kwargs,
                                        PyObject* obj);

typedef struct ContextManagerItem
{
    TypeAdapter* validator;
    PyObject* hint;
} ContextManagerItem;

struct ContextManager
{
    PyObject_VAR_HEAD PyObject* model;
    PyObject* gtypes;
    ContextManagerCall validate_call;
    ContextManagerItem items[1];
};

extern PyTypeObject ContextManager_Type;
extern int
_ParseFrostValidate(PyObject* const*, Py_ssize_t, PyObject**, ContextManager**);
extern PyObject*
_ContextManager_Get_THint(PyObject* cls, ContextManager* ctx);
extern int
_ContextManager_Get_TTypeAdapter(PyObject* cls,
                                 ContextManager* ctx,
                                 TypeAdapter** validator);
extern ContextManager*
_ContextManager_CreateByOld(ContextManager* self, ContextManager* ctx);
extern PyObject*
_ContextManager_CreateGetItem(PyObject* model,
                              PyObject* gtypes,
                              PyObject* key,
                              ContextManagerCall call);
extern ContextManager*
_ContextManager_New(PyObject* model, ContextManagerCall call);
extern int
_ContextManager_ReprModel(_PyUnicodeWriter* writer, PyObject* model);
extern PyObject*
_ContextManager_FrostValidate(ContextManager* self,
                              PyObject* val,
                              ContextManager* ctx);
extern int
context_setup(void);
extern void
context_free(void);