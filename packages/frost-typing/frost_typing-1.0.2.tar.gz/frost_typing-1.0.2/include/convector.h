#define PY_SSIZE_T_CLEAN
#include "Python.h"
#define CONVECTOR_SIZE 18

typedef struct ConvParams ConvParams;

#define _DATA_MODEL_POS 0
#define _BOOL_POS 1
#define _INT_POS 2
#define _STR_POS 3
#define _SET_POS 4
#define _LIST_POS 5
#define _DICT_POS 6
#define _NONE_POS 7
#define _FLOAT_POS 8
#define _TUPLE_POS 9
#define _BYTES_POS 10
#define _BYTES_ARR_POS 11
#define _DATE_POS 12
#define _TIME_POS 13
#define _ENUM_POS 14
#define _UUID_POS 15
#define _DATE_TIME_POS 16
#define _VALIDATIO_ERR_POS 17

typedef PyObject* (*ObjectConverter)(PyObject* val, ConvParams* params);
#define ConvParams_Create(converter)                                           \
    (ConvParams)                                                               \
    {                                                                          \
        .by_alias = 1, .exclude_unset = 0, .exclude_none = 0,                  \
        .conv = converter, .nested = 0,                                        \
    }

struct ConvParams
{
    ObjectConverter conv;
    Py_ssize_t nested;
    int by_alias;
    int exclude_unset;
    int exclude_none;
};

extern PyObject*
AsDictNoKwargs(PyObject* obj);
extern PyObject*
CopyNoKwargs(PyObject* obj);
extern PyObject*
Copy(PyObject*, ConvParams*);
extern PyObject*
PyCopy(PyObject* obj);
extern PyObject*
AsDict(PyObject*, ConvParams*);
extern PyObject*
AsDictJson(PyObject* val, ConvParams* conv_params);
extern int
Convector_ValidateInclue(PyObject* include, PyObject* exclude);
extern int
_Conv_Get(PyTypeObject* tp, PyObject* attr);
extern int
Convector_IsConstVal(PyObject* val);
extern int
ConvecotrEnterRecCall(ConvParams* params);
extern void
ConvecotrLeaveRecCall(ConvParams* params);
extern int
convector_setup(void);
extern void
convector_free(void);