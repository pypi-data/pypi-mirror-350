#define PY_SSIZE_T_CLEAN
#include "Python.h"
#define DATA_MODEL_GET_SLOTS(o)                                                \
    _CAST(PyObject**, (char*)o + META_MODEL_GET_OFFSET(Py_TYPE(o)))

typedef PyObject* (*InitGetter)(PyObject*, PyObject*);

typedef struct MetaModel MetaModel;
typedef struct Field Field;
typedef struct ConvParams ConvParams;
typedef PyObject* (*ObjectConverter)(PyObject* val, ConvParams* params);

#define DataModelForeach(s, o, ...)                                            \
    for (PyObject** s = DATA_MODEL_GET_SLOTS(o),                               \
                    ** __end_##s = s + META_GET_SIZE(Py_TYPE(o));              \
         s != __end_##s;                                                       \
         s++, ##__VA_ARGS__)

extern MetaModel DataModelType;

typedef struct DataModelIter
{
    PyObject_HEAD PyObject* model;
    Py_ssize_t ind;
} DataModelIter;

extern void
data_model_free(void);
extern int
data_model_setup(void);
extern int
_DataModel_SetDefault(Field*, PyObject**);
extern PyObject*
_DataModel_Getattro(PyObject* self, PyObject* name);
extern int
_DataModel_Setattro(PyObject* self, PyObject* name, PyObject* val);
extern PyObject*
_DataModel_AsDict(PyObject* self,
                  ConvParams* params,
                  PyObject* include,
                  PyObject* exclude);
extern PyObject*
_DataModel_Copy(PyObject* self);
