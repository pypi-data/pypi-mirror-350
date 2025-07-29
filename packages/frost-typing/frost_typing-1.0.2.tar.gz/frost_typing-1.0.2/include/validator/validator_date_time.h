#define PY_SSIZE_T_CLEAN
#include "Python.h"

extern TypeAdapter *TypeAdapterTime, *TypeAdapterDate, *TypeAdapterDateTime;

extern int
date_time_setup(void);
extern void
date_time_free(void);
extern PyObject*
DateTime_ParseDate(PyObject*);
extern PyObject*
DateTime_ParseTime(PyObject*);
extern PyObject*
DateTime_ParseDateTime(PyObject*);
extern int
DateTime_Is_DateType(PyTypeObject*);
extern int
DateTime_Is_TimeType(PyTypeObject*);
extern int
DateTime_Is_DateTimeType(PyTypeObject*);
