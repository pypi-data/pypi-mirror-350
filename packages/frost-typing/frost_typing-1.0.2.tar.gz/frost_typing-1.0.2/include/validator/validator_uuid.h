#define PY_SSIZE_T_CLEAN
#include "Python.h"

typedef struct TypeAdapter TypeAdapter;

extern TypeAdapter*
TypeAdapter_Create_Uuid(PyObject* hint);
extern int
validator_uuid_setup(void);
extern void
validator_uuid_free(void);