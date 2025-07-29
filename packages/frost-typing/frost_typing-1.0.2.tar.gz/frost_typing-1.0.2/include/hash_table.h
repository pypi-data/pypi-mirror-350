#define PY_SSIZE_T_CLEAN
#include "Python.h"

typedef struct HashEntry
{
    PyObject* key;
    Py_ssize_t offset;
} HashEntry;

typedef struct HashTable
{
    Py_ssize_t mask;
    HashEntry entries[1];
} HashTable;

extern void
HashTable_Dealloc(HashTable* map);
extern HashTable*
HashTable_Create(PyObject* schema);
extern Py_ssize_t
HashTable_Get(HashTable* map, PyObject* string);
extern int
HashTable_CheckExtraKwnames(HashTable* map,
                            PyObject* kwnames,
                            const char* tp_name,
                            const char* func_name);
extern int
HashTable_CheckExtraDict(HashTable* map,
                         PyObject* dict,
                         const char* tp_name,
                         const char* func_name);