#define PY_SSIZE_T_CLEAN
#include "Python.h"

#ifdef __GNUC__
#define UNUSED __attribute__((unused))
#elif defined(_MSC_VER)
#define UNUSED __pragma(warning(suppress : 4100))
#else
#define UNUSED
#endif

#define _CAST(tp, o) ((tp)(o))
#define _STRLEN(s) (sizeof(s) / sizeof(s[0]))
#define SIZE_OBJ ((Py_ssize_t)sizeof(PyObject))
#define BASE_SIZE ((Py_ssize_t)sizeof(PyObject*))
#define FASTCALL_SMALL_STACK 5

#define TUPLE_ITEMS(o) (_CAST(PyTupleObject*, o)->ob_item)
#define LIST_ITEMS(o) (_CAST(PyListObject*, o)->ob_item)
#define TYPE_SIZE(tp) (_CAST(PyTypeObject*, tp)->tp_basicsize)
#define TYPE_WEAK_OFFSET(m) (_CAST(PyTypeObject*, m)->tp_weaklistoffset)
#define TYPE_DICT_OFFSET(m) (_CAST(PyTypeObject*, m)->tp_dictoffset)
#define GET_ADDR(obj, o) (_CAST(PyObject**, _CAST(char*, obj) + o))
#define GET_OBJ(obj, o) (*_CAST(PyObject**, _CAST(char*, obj) + o))
#define SET_OBJ(obj, o, v) *_CAST(PyObject**, _CAST(char*, obj) + o) = v
#define _AnySetType_Check(tp)                                                  \
    (tp == &PySet_Type || tp == &PyFrozenSet_Type ||                           \
     PyType_IsSubtype(tp, &PySet_Type) ||                                      \
     PyType_IsSubtype(tp, &PyFrozenSet_Type))

#if SIZEOF_Py_hash_t > 4
#define _PyHASH_XXPRIME_1 ((Py_hash_t)11400714785074694791ULL)
#define _PyHASH_XXPRIME_2 ((Py_hash_t)14029467366897019727ULL)
#define _PyHASH_XXPRIME_5 ((Py_hash_t)2870177450012600261ULL)
#define _PyHASH_XXROTATE(x) ((x << 31) | (x >> 33)) /* Rotate left 31 bits */
#else
#define _PyHASH_XXPRIME_1 ((Py_hash_t)2654435761UL)
#define _PyHASH_XXPRIME_2 ((Py_hash_t)2246822519UL)
#define _PyHASH_XXPRIME_5 ((Py_hash_t)374761393UL)
#define _PyHASH_XXROTATE(x) ((x << 13) | (x >> 19)) /* Rotate left 13 bits */
#endif

#define _CAST_TYPE(tp) _CAST(PyTypeObject*, tp)

#if PY_MINOR_VERSION < 10
static inline PyObject*
_Py_NewRef(PyObject* o)
{
    Py_INCREF(o);
    return o;
}

static inline PyObject*
_Py_XNewRef(PyObject* o)
{
    Py_XINCREF(o);
    return o;
}
#define Py_NewRef(o) _Py_NewRef(_CAST(PyObject*, o))
#define Py_XNewRef(o) _Py_XNewRef(_CAST(PyObject*, o))
#endif

#define _PyDict_GetItem_Ascii(d, n)                                            \
    _PyDict_GetItem_KnownHash(d, n, _CAST(PyASCIIObject*, n)->hash)

#define CREATE_VAR_INTERN___STING(v)                                           \
    __##v = PyUnicode_InternFromString(#v);                                    \
    if (__##v == NULL) {                                                       \
        return -1;                                                             \
    }

#define CREATE_VAR_INTERN_STING(v)                                             \
    v = PyUnicode_InternFromString(#v);                                        \
    if (v == NULL) {                                                           \
        return -1;                                                             \
    }

/*UNICODE*/
#define _UNICODE_WRITE_STRING(w, s, i)                                         \
    if (_PyUnicodeWriter_WriteASCIIString(w, s, i) < 0) {                      \
        goto error;                                                            \
    }

#define _UNICODE_WRITE_STR(w, s)                                               \
    if (_PyUnicodeWriter_WriteStr(w, s) < 0) {                                 \
        goto error;                                                            \
    }

#define _UNICODE_WRITE_CHAR(w, s)                                              \
    if (_PyUnicodeWriter_WriteChar(w, s) < 0) {                                \
        goto error;                                                            \
    }

#define _UNICODE_WRITE(w, o, f)                                                \
    if (_UnicodeWriter_Write(w, (PyObject*)o, f) < 0) {                        \
        goto error;                                                            \
    }

#define _UNICODE_WRITE_SSIZE(w, d)                                             \
    if (_UnicodeWriter_WriteSsize(w, d) < 0) {                                 \
        goto error;                                                            \
    }

#define RETURN_ATTRIBUT_ERROR(o, name, r)                                      \
    PyErr_Format(PyExc_AttributeError,                                         \
                 "'%.100s' object has no attribute '%.100U'",                  \
                 Py_TYPE(o)->tp_name,                                          \
                 name);                                                        \
    return r;

#if PY_VERSION_HEX >= 0x30d00f0 // Python 3.13+
#define Py_BUILD_CORE 1
#include "internal/pycore_setobject.h"
#undef Py_BUILD_CORE

extern int
_PyDict_SetItem_KnownHash_LockHeld(PyObject* mp,
                                   PyObject* key,
                                   PyObject* value,
                                   Py_hash_t hash);
#define PyDict_SetItem_KnownHash _PyDict_SetItem_KnownHash_LockHeld
extern int
_PyArg_NoPositional(const char* funcname, PyObject* args);
extern int
_PyArg_NoKeywords(const char* funcname, PyObject* kwargs);
#define PyLong_AsByteArray(v, bytes, n, little_endian, is_signed)              \
    _PyLong_AsByteArray((PyLongObject*)v, bytes, n, little_endian, is_signed, 1)
#else
#define PyLong_AsByteArray(v, bytes, n, little_endian, is_signed)              \
    _PyLong_AsByteArray((PyLongObject*)v, bytes, n, little_endian, is_signed)
#define PyDict_SetItem_KnownHash _PyDict_SetItem_KnownHash
#endif

#define Dict_SetItem_String(d, k, v)                                           \
    PyDict_SetItem_KnownHash(d, k, v, _Hash_String(k))

extern PyTypeObject* PyNone_Type;
extern PyObject *__annotations__, *__sep_and__, *__slots__, *__post_init__,
  *__return, *__dict__, *__weakref__, *__default_factory, *__config__,
  *__as_dict__, *__copy__, *__name__, *__as_json__, *VoidTuple, *VoidDict,
  *Long_Zero, *Long_One, *__origin__, *__module__, *__required_keys__,
  *__instancecheck__, *__type_params__, *__metadata__, *__bound__, *VoidSet,
  *__constraints__, *__args__, *__exclude, *__include, *_value2member_map_,
  *__is_safe, *__int, *__new__, *__init__;

int
VectorCall_CheckKwStrOnly(PyObject* kwnames);
extern int
_UnicodeWriter_WriteSsize(_PyUnicodeWriter*, Py_ssize_t);
extern int
_UnicodeWriter_Write(_PyUnicodeWriter*,
                     PyObject*,
                     PyObject* (*to_str)(PyObject*));
extern int
PyDict_SetItemDecrefVal(PyObject*, PyObject*, PyObject*);
extern int
PyDict_SetItemStringDecrefVal(PyObject*, PyObject*, PyObject*);
extern int
PyDict_SetItemWithTransform(PyObject*,
                            PyObject*,
                            PyObject*,
                            PyObject* (*call)(PyObject*));
extern PyObject*
_Object_Call_Prepend(PyObject* callable,
                     PyObject* obj,
                     PyObject* const* args,
                     size_t nargs,
                     PyObject* kwnms);
extern PyObject*
_RaiseInvalidType(const char* attr,
                  const char* expected_tp,
                  const char* received_tp);
extern int
EqString(PyObject* str_bytes, char* const str, Py_ssize_t size);
extern int
CheckValidityOfAttribute(PyObject*);
extern int
PyCheck_MaxArgs(const char* const func_name,
                Py_ssize_t args_cnt,
                Py_ssize_t max_arg_cnt);
extern int
PyCheck_ArgsCnt(const char* msg,
                Py_ssize_t args_cnt,
                Py_ssize_t expected_arg_cnt);
extern PyObject*
Parse_OneArgs(const char* msg, PyObject* args);
extern PyObject*
Parse_OneArgsNoKw(const char* msg, PyObject* args, PyObject* kw);
extern int
Unicode_IsPrivate(PyObject* unicode);
extern PyObject*
_VectorCall_GetFuncArg(char* const msg,
                       PyObject* const* args,
                       size_t nargsf,
                       PyObject* kwnames);
extern Py_hash_t
_PyHashBytes(const void*, Py_ssize_t);
extern Py_ssize_t
_ArrayFastSearh(PyObject* const* array, PyObject* key, Py_ssize_t size);
extern PyObject*
_VectorCall_GetOneArg(char* const msg,
                      PyObject* const* args,
                      size_t nargsf,
                      PyObject* kwnames);
extern PyObject*
_PyObject_Get_Func(PyObject* func, const char* attr);
extern PyObject*
_Object_Gettr(PyObject* obj, PyObject* name);
extern PyObject*
_Dict_GetAscii(PyObject* dict, PyObject* name);
extern Py_hash_t
_Hash_String(PyObject* str);
extern int
_Dict_MergeKwnames(PyObject* dict, PyObject* const* args, PyObject* kwnames);
extern int
_PySet_Next(PyObject* set, Py_ssize_t* pos, PyObject** val);
extern int
_PyIter_GetNext(PyObject* iter, PyObject** item);
extern int
PyObject_CheckHashable(PyObject* obj);
extern int
PyObject_CheckIter(PyObject* obj);
extern PyObject*
PyObject_Get_annotations(PyObject* obj);
extern int
utils_common_setup(void);
extern void
utils_common_free(void);