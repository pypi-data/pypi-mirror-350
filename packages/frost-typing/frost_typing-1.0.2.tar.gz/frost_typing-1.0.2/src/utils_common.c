#include "utils_common.h"
#include "stdio.h"

PyObject *__annotations__, *__sep_and__, *__slots__, *__post_init__, *__return,
  *__dict__, *__weakref__, *__default_factory, *__name__, *__config__,
  *__as_dict__, *__copy__, *__as_json__, *VoidTuple, *VoidDict, *Long_Zero,
  *Long_One, *__origin__, *__module__, *__required_keys__, *__metadata__,
  *__instancecheck__, *__bound__, *__constraints__, *__args__, *__type_params__,
  *__exclude, *__include, *VoidSet, *_value2member_map_, *__is_safe, *__int,
  *__new__, *__init__;
PyTypeObject* PyNone_Type;
typedef Py_hash_t (*hash_func)(const void*, Py_ssize_t);
hash_func get_hash_bytes;

#if PY_VERSION_HEX >= 0x030D0000 // Python 3.13+
int
_PyArg_NoPositional(const char* funcname, PyObject* args)
{
    if (!args || PyTuple_GET_SIZE(args) == 0) {
        return 1;
    }
    PyErr_Format(
      PyExc_TypeError, "%s() takes no positional arguments", funcname);
    return 0;
}
int
_PyArg_NoKeywords(const char* funcname, PyObject* kwargs)
{
    if (!kwargs || !PyDict_GET_SIZE(kwargs)) {
        return 1;
    }
    PyErr_Format(PyExc_TypeError, "%s() takes no keyword arguments", funcname);
    return 0;
}
#endif

int
VectorCall_CheckKwStrOnly(PyObject* kwnames)
{
    if (!kwnames) {
        return 1;
    }

    PyObject** restrict names = TUPLE_ITEMS(kwnames);
    Py_ssize_t size = PyTuple_GET_SIZE(kwnames);
    for (Py_ssize_t i = 0; i != size; i++) {
        if (!PyUnicode_Check(names[i])) {
            PyErr_SetString(PyExc_TypeError, "keywords must be strings");
            return 0;
        }
    }
    return 1;
}

int
set_next(PySetObject* set, Py_ssize_t* pos, PyObject** val)
{
    Py_ssize_t i;
    Py_ssize_t mask;
    setentry* entry;

    i = *pos;
    mask = set->mask;
    entry = &set->table[i];
    while (i <= mask && (entry->key == NULL || entry->key == _PySet_Dummy)) {
        i++;
        entry++;
    }
    *pos = i + 1;
    if (i > mask) {
        return 0;
    }
    *val = entry->key;
    return 1;
}

inline int
_PySet_Next(PyObject* set, Py_ssize_t* pos, PyObject** val)
{
    return set_next((PySetObject*)set, pos, val);
}

int
_PyIter_GetNext(PyObject* iter, PyObject** item)
{
    iternextfunc tp_iternext = Py_TYPE(iter)->tp_iternext;
    if ((*item = tp_iternext(iter))) {
        return 1;
    }

    if (!PyErr_Occurred()) {
        return 0;
    }

    if (PyErr_ExceptionMatches(PyExc_StopIteration)) {
        PyErr_Clear();
        return 0;
    }
    return -1;
}

PyObject*
_Object_Call_Prepend(PyObject* callable,
                     PyObject* obj,
                     PyObject* const* args,
                     size_t nargs,
                     PyObject* kwnms)
{
    PyObject **stack, *res;
    if (nargs & PY_VECTORCALL_ARGUMENTS_OFFSET) {
        stack = (PyObject**)(args - 1);
        PyObject* tmp = stack[0];
        stack[0] = obj;
        res = PyObject_Vectorcall(
          callable, stack, PyVectorcall_NARGS(nargs) + 1, kwnms);
        stack[0] = tmp;
        return res;
    }

    PyObject* small_stack[FASTCALL_SMALL_STACK];
    Py_ssize_t total_size = (nargs + (kwnms ? Py_SIZE(kwnms) : 0));
    if (total_size < FASTCALL_SMALL_STACK) {
        stack = small_stack;
    } else {
        stack = PyMem_Malloc((total_size + 1) * BASE_SIZE);
        if (!stack) {
            PyErr_NoMemory();
            return NULL;
        }
    }

    stack[0] = obj;
    memcpy(&stack[1], args, total_size * BASE_SIZE);

    res = PyObject_Vectorcall(callable, stack, nargs + 1, kwnms);
    if (stack != small_stack) {
        PyMem_Free(stack);
    }
    return res;
}

int
_UnicodeWriter_WriteSsize(_PyUnicodeWriter* writer, Py_ssize_t digit)
{
    char buffer_digit[21];
    int size_cnt = sprintf(buffer_digit, "%zu", digit);
    return _PyUnicodeWriter_WriteASCIIString(writer, buffer_digit, size_cnt);
}

int
_UnicodeWriter_Write(_PyUnicodeWriter* writer,
                     PyObject* obj,
                     PyObject* (*to_str)(PyObject*))
{
    PyObject* s = to_str(obj);
    if (s == NULL) {
        return -1;
    }
    int r = _PyUnicodeWriter_WriteStr(writer, s);
    Py_DECREF(s);
    return r;
}

inline int
Unicode_IsPrivate(PyObject* unicode)
{
    return PyUnicode_GET_LENGTH(unicode) &&
           PyUnicode_READ_CHAR(unicode, 0) == (Py_UCS4)'_';
}

int
CheckValidityOfAttribute(PyObject* name)
{
    if (PyUnicode_Check(name) && PyUnicode_IS_ASCII(name) &&
        PyUnicode_IsIdentifier(name)) {
        // Calculate the hash for caching
        _Hash_String(name);
        return 1;
    }
    PyErr_Format(
      PyExc_ValueError, "Invalid name for the attribute: '%S'", name);
    return 0;
}

inline int
PyCheck_MaxArgs(const char* const func_name,
                Py_ssize_t args_cnt,
                Py_ssize_t max_arg_cnt)
{
    if (args_cnt > max_arg_cnt) {
        PyErr_Format(PyExc_TypeError,
                     "%s() takes %zu positional argument but %zu were given",
                     func_name,
                     max_arg_cnt,
                     args_cnt);
        return 0;
    }
    return 1;
}

inline int
PyCheck_ArgsCnt(const char* msg,
                Py_ssize_t args_cnt,
                Py_ssize_t expected_arg_cnt)
{
    if (args_cnt != expected_arg_cnt) {
        PyErr_Format(PyExc_TypeError,
                     "%s() takes %zu positional argument but %zu were given",
                     msg,
                     expected_arg_cnt,
                     args_cnt);
        return 0;
    }
    return 1;
}

inline PyObject*
Parse_OneArgs(const char* msg, PyObject* args)
{
    Py_ssize_t size = PyTuple_GET_SIZE(args);
    if (!PyCheck_ArgsCnt(msg, size, 1)) {
        return NULL;
    }
    return PyTuple_GET_ITEM(args, 0);
}

inline PyObject*
Parse_OneArgsNoKw(const char* msg, PyObject* args, PyObject* kw)
{
    if (!_PyArg_NoKeywords(msg, kw)) {
        return NULL;
    }
    return Parse_OneArgs(msg, args);
}

inline int
PyDict_SetItemStringDecrefVal(PyObject* mp, PyObject* str, PyObject* item)
{
    int r = Dict_SetItem_String(mp, str, item);
    Py_DECREF(item);
    return r;
}

int
PyDict_SetItemDecrefVal(PyObject* mp, PyObject* key, PyObject* item)
{
    int r = PyDict_SetItem(mp, key, item);
    Py_DECREF(item);
    return r;
}

int
PyDict_SetItemWithTransform(PyObject* mp,
                            PyObject* key,
                            PyObject* item,
                            PyObject* (*call)(PyObject*))
{
    PyObject* tmp = call(item);
    if (!tmp) {
        return -1;
    }
    return PyDict_SetItemDecrefVal(mp, key, tmp);
}

inline Py_ssize_t
_ArrayFastSearh(PyObject* const* array, PyObject* key, Py_ssize_t size)
{
    PyObject* const* end = array + size;
    for (PyObject* const* it = array; it < end; ++it) {
        if (*it == key) {
            return it - array;
        }
    }
    return -1;
}

int
EqString(PyObject* str_bytes, char* const str, Py_ssize_t size)
{
    if (PyUnicode_Check(str_bytes)) {
        return PyUnicode_KIND(str_bytes) == 1 &&
               PyUnicode_GET_LENGTH(str_bytes) == size &&
               !memcmp(PyUnicode_DATA(str_bytes), str, size);
    }
    if (PyBytes_Check(str_bytes)) {
        return PyBytes_GET_SIZE(str_bytes) == size &&
               !memcmp(_CAST(PyBytesObject*, str_bytes)->ob_sval, str, size);
    }
    if (PyByteArray_Check(str_bytes)) {
        return PyByteArray_GET_SIZE(str_bytes) == size &&
               !memcmp(
                 _CAST(PyByteArrayObject*, str_bytes)->ob_bytes, str, size);
    }
    return -1;
}

inline int
PyObject_CheckHashable(PyObject* obj)
{
    hashfunc tp_hash = Py_TYPE(obj)->tp_hash;
    return tp_hash && tp_hash != PyObject_HashNotImplemented;
}

inline int
PyObject_CheckIter(PyObject* obj)
{
    return Py_TYPE(obj)->tp_iter || PySequence_Check(obj);
}

inline PyObject*
_RaiseInvalidType(const char* attr,
                  const char* expected_tp,
                  const char* received_tp)
{
    return PyErr_Format(PyExc_TypeError,
                        "Attribute '%.100s' must be a %.100s, not '%.100s'",
                        attr,
                        expected_tp,
                        received_tp);
}

inline Py_hash_t
_Hash_String(PyObject* str)
{
    Py_hash_t x = _CAST(PyASCIIObject*, str)->hash;
    if (x != -1) {
        return x;
    }
    x = _PyHashBytes(PyUnicode_DATA(str),
                     PyUnicode_GET_LENGTH(str) * PyUnicode_KIND(str));
    _CAST(PyASCIIObject*, str)->hash = x;
    return x;
}

PyObject*
_PyObject_Get_Func(PyObject* func, const char* attr)
{
    if (Py_IS_TYPE(func, &PyFunction_Type)) {
        return Py_NewRef(func);
    }
    if (Py_IS_TYPE(func, &PyClassMethod_Type)) {
        func = PyObject_GetAttrString(func, "__func__");
        if (func) {
            PyObject* tmp = _PyObject_Get_Func(func, attr);
            Py_DECREF(func);
            return tmp;
        }
        return func;
    }

    return _RaiseInvalidType(
      attr, "function or classmethod", Py_TYPE(func)->tp_name);
}

inline Py_hash_t
_PyHashBytes(const void* data, Py_ssize_t size)
{
    return get_hash_bytes(data, size);
}

PyObject*
_Dict_GetAscii(PyObject* dict, PyObject* name)
{
    return Py_XNewRef(_PyDict_GetItem_Ascii(dict, name));
}

PyObject*
_Object_Gettr(PyObject* obj, PyObject* name)
{
    PyObject* res = PyObject_GetAttr(obj, name);
    if (!res) {
        PyErr_Clear();
    }
    return res;
}

PyObject*
PyObject_Get_annotations(PyObject* obj)
{
    PyObject* annot = PyObject_GetAttr(obj, __annotations__);
    if (!annot) {
        return NULL;
    }

    if (!PyDict_Check(annot)) {
        _RaiseInvalidType("__annotations__", "dict", Py_TYPE(annot)->tp_name);
        Py_DECREF(annot);
        return NULL;
    }

    return annot;
}

PyObject*
_VectorCall_GetOneArg(char* const msg,
                      PyObject* const* args,
                      size_t nargsf,
                      PyObject* kwnames)
{
    if (kwnames && PyTuple_GET_SIZE(kwnames)) {
        return PyErr_Format(
          PyExc_TypeError, "%s() takes no keyword arguments", msg);
    }

    if (!PyCheck_ArgsCnt(msg, PyVectorcall_NARGS(nargsf), 1)) {
        return NULL;
    }
    return *args;
}

int
_Dict_MergeKwnames(PyObject* dict, PyObject* const* args, PyObject* kwnames)
{
    if (!kwnames) {
        return 0;
    }

    Py_ssize_t size = PyTuple_GET_SIZE(kwnames);
    for (Py_ssize_t i = 0; i != size; i++) {
        PyObject* name = PyTuple_GET_ITEM(kwnames, i);
        if (!PyUnicode_Check(name)) {
            PyErr_SetString(PyExc_TypeError, "keywords must be strings");
            return -1;
        }

        if (Dict_SetItem_String(dict, name, args[i]) < 0) {
            return -1;
        }
    }
    return 0;
}

PyObject*
_VectorCall_GetFuncArg(char* const msg,
                       PyObject* const* args,
                       size_t nargsf,
                       PyObject* kwnames)
{
    PyObject* func = _VectorCall_GetOneArg(msg, args, nargsf, kwnames);
    return func ? _PyObject_Get_Func(func, "func") : func;
}

int
utils_common_setup(void)
{
    VoidSet = PyFrozenSet_New(NULL);
    if (!VoidSet) {
        return -1;
    }
    PyNone_Type = Py_TYPE(Py_None);
    CREATE_VAR_INTERN_STING(__new__)
    CREATE_VAR_INTERN_STING(__init__)
    CREATE_VAR_INTERN_STING(__copy__)
    CREATE_VAR_INTERN_STING(__dict__)
    CREATE_VAR_INTERN_STING(__name__)
    CREATE_VAR_INTERN_STING(__args__)
    CREATE_VAR_INTERN_STING(__bound__)
    CREATE_VAR_INTERN_STING(__slots__)
    CREATE_VAR_INTERN_STING(__config__)
    CREATE_VAR_INTERN_STING(__origin__)
    CREATE_VAR_INTERN_STING(__module__)
    CREATE_VAR_INTERN_STING(__as_json__)
    CREATE_VAR_INTERN_STING(__weakref__)
    CREATE_VAR_INTERN_STING(__as_dict__)
    CREATE_VAR_INTERN_STING(__metadata__)
    CREATE_VAR_INTERN_STING(__post_init__)
    CREATE_VAR_INTERN_STING(__annotations__)
    CREATE_VAR_INTERN_STING(__constraints__)
    CREATE_VAR_INTERN_STING(__type_params__)
    CREATE_VAR_INTERN_STING(__required_keys__)
    CREATE_VAR_INTERN_STING(__instancecheck__)
    CREATE_VAR_INTERN_STING(_value2member_map_)
    CREATE_VAR_INTERN___STING(default_factory)
    CREATE_VAR_INTERN___STING(is_safe)
    CREATE_VAR_INTERN___STING(return)
    CREATE_VAR_INTERN___STING(exclude)
    CREATE_VAR_INTERN___STING(include)
    CREATE_VAR_INTERN___STING(int)

    get_hash_bytes = PyHash_GetFuncDef()->hash;
    Long_Zero = PyLong_FromSsize_t(0);
    if (!Long_Zero) {
        return -1;
    }

    Long_One = PyLong_FromSsize_t(1);
    if (!Long_One) {
        return -1;
    }

    VoidTuple = PyTuple_New(0);
    if (!VoidTuple) {
        return -1;
    }

    VoidDict = _PyDict_NewPresized(0);
    if (!VoidDict) {
        return -1;
    }

    __sep_and__ = PyUnicode_FromString("' and '");
    if (!__sep_and__) {
        return -1;
    }
    return 0;
}

void
utils_common_free(void)
{
    Py_DECREF(VoidSet);
    Py_DECREF(VoidDict);
    Py_DECREF(__int);
    Py_DECREF(__new__);
    Py_DECREF(__init__);
    Py_DECREF(__copy__);
    Py_DECREF(__dict__);
    Py_DECREF(__return);
    Py_DECREF(__is_safe);
    Py_DECREF(__slots__);
    Py_DECREF(Long_Zero);
    Py_DECREF(Long_One);
    Py_DECREF(VoidTuple);
    Py_DECREF(__config__);
    Py_DECREF(__as_dict__);
    Py_DECREF(__weakref__);
    Py_DECREF(__sep_and__);
    Py_DECREF(__as_json__);
    Py_DECREF(__post_init__);
    Py_DECREF(__annotations__);
    Py_DECREF(__type_params__);
    Py_DECREF(__instancecheck__);
    Py_DECREF(__default_factory);
    Py_DECREF(_value2member_map_);
    Py_DECREF(__required_keys__);
    Py_DECREF(__constraints__);
    Py_DECREF(__metadata__);
    Py_DECREF(__origin__);
    Py_DECREF(__module__);
    Py_DECREF(__args__);
    Py_DECREF(__bound__);
    Py_DECREF(__exclude);
    Py_DECREF(__include);
}