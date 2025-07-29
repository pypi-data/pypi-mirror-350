#include "hash_table.h"
#include "schema.h"
#include "utils_common.h"

#define OFFSET 1

void
HashTable_Dealloc(HashTable* map)
{
    if (!map) {
        return;
    }
    for (Py_ssize_t i = 0; i < map->mask; i++) {
        Py_XDECREF(map->entries[i].key);
    }
    PyMem_Free(map);
}

static HashTable*
hash_table_alloc(Py_ssize_t len)
{
    Py_ssize_t size = 1;
    while (size < (len * 2.5)) {
        size <<= 1;
    }
    Py_ssize_t total_size = sizeof(HashTable) + sizeof(HashEntry) * size;
    HashTable* map = (HashTable*)PyMem_Malloc(total_size);
    if (!map) {
        PyErr_NoMemory();
        return NULL;
    }

    memset(map, 0, total_size);
    map->mask = size - 1;
    return map;
}

HashTable*
HashTable_Create(PyObject* schema)
{
    Py_ssize_t size = PyTuple_GET_SIZE(schema);
    HashTable* map = hash_table_alloc(size);

    for (Py_ssize_t i = 0; i != size; i++) {
        Schema* sc = _CAST(Schema*, PyTuple_GET_ITEM(schema, i));
        if (sc == WeakRefSchema || sc == DictSchema) {
            continue;
        }

        PyObject* key = sc->name;
        Py_hash_t hash = _Hash_String(key);
        Py_ssize_t j = hash & map->mask;

        while (map->entries[j].key) {
            j = (j + OFFSET) & map->mask;
        }
        map->entries[j].key = Py_NewRef(key);
        map->entries[j].offset = i * BASE_SIZE;
    }

    return map;
}

static inline Py_ssize_t
hash_table_get(HashTable* map, PyObject* string)
{
    if (!map) {
        return -1;
    }

    const Py_ssize_t key_len = PyUnicode_GET_LENGTH(string);
    const Py_hash_t hash = _Hash_String(string);
    const Py_ssize_t mask = map->mask;
    Py_ssize_t i = hash & mask;

    for (;;) {
        PyObject* k = map->entries[i].key;
        if (!k) {
            return -1;
        }

        if (k == string ||
            (_CAST(PyASCIIObject*, k)->hash == hash &&
             key_len == PyUnicode_GET_LENGTH(k) &&
             !memcmp(PyUnicode_DATA(k), PyUnicode_DATA(string), key_len))) {
            return map->entries[i].offset;
        }

        i = (i + OFFSET) & mask;
    }
}

inline Py_ssize_t
HashTable_Get(HashTable* map, PyObject* string)
{
    if (!PyUnicode_Check(string)) {
        return -2;
    }
    return hash_table_get(map, string);
}

int
HashTable_CheckExtraKwnames(HashTable* map,
                            PyObject* kwnames,
                            const char* tp_name,
                            const char* func_name)
{
    if (!map || !kwnames) {
        return 0;
    }

    Py_ssize_t size = PyTuple_GET_SIZE(kwnames);
    for (Py_ssize_t i = 0; i != size; i++) {
        PyObject* name = PyTuple_GET_ITEM(kwnames, i);
        if (HashTable_Get(map, name) == -1) {
            PyErr_Format(PyExc_TypeError,
                         "%s.%s() got an unexpected keyword argument '%U'",
                         tp_name,
                         func_name,
                         name);
            return -1;
        }
    }
    return 0;
}

int
HashTable_CheckExtraDict(HashTable* map,
                         PyObject* dict,
                         const char* tp_name,
                         const char* func_name)
{
    if (!map || !dict) {
        return 0;
    }

    Py_ssize_t pos = 0;
    PyObject *name, *_;
    while (PyDict_Next(dict, &pos, &name, &_)) {
        if (HashTable_Get(map, name) == -1) {
            PyErr_Format(PyExc_TypeError,
                         "%s.%s() got an unexpected keyword argument '%U'",
                         tp_name,
                         func_name,
                         name);
            return -1;
        }
    }
    return 0;
}