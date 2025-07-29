#include "convector.h"
#include "data_model.h"
#include "datetime.h"
#include "meta_model.h"
#include "validator/py_typing.h"
#include "validator/validator.h"

#define _ARGS_SIZE 6
#define ARGS_SIZE 5
#define MAX_NESTING 1000

int
ConvecotrEnterRecCall(ConvParams* params)
{
    if (++(params->nested) > MAX_NESTING) {
        PyErr_SetString(PyExc_RecursionError,
                        "maximum recursion depth exceeded");
        return 0;
    }
    return 1;
}

inline void
ConvecotrLeaveRecCall(ConvParams* params)
{
    params->nested--;
}

static PyObject*
convector_decode(PyObject* val, UNUSED ConvParams* params)
{
    return PyUnicode_FromEncodedObject(val, NULL, NULL);
}

static PyObject*
convector_const(PyObject* val, UNUSED ConvParams* params)
{
    return Py_NewRef(val);
}

static inline PyObject*
convector_type(PyTypeObject* tp, PyObject* obj)
{
    if (tp == Py_TYPE(obj)) {
        return obj;
    }
    PyObject* tmp = PyObject_CallOneArg((PyObject*)tp, obj);
    Py_DECREF(obj);
    return tmp;
}

static PyObject*
convector_dict(PyObject* dict, ConvParams* params)
{
    if (!ConvecotrEnterRecCall(params)) {
        return NULL;
    }

    PyObject *key, *val, *res;
    res = PyDict_New();
    if (!res) {
        return NULL;
    }

    Py_ssize_t pos = 0;
    ObjectConverter converter = params->conv;
    while (PyDict_Next(dict, &pos, &key, &val)) {
        key = converter(key, params);
        if (!key) {
            goto error;
        }

        val = converter(val, params);
        if (!val) {
            goto error;
        }

        int r = PyDict_SetItem(res, key, val);
        Py_DECREF(val);
        Py_DECREF(key);
        if (r < 0) {
            goto error;
        }
    }

    ConvecotrLeaveRecCall(params);
    return convector_type(Py_TYPE(dict), res);
error:
    Py_DECREF(res);
    return NULL;
}

static int
convector_array(PyObject** arr,
                Py_ssize_t size,
                PyObject** res,
                ConvParams* params)
{
    ObjectConverter converter = params->conv;
    for (Py_ssize_t i = 0; i != size; i++) {
        PyObject* val = converter(arr[i], params);
        if (!val) {
            return -1;
        }
        res[i] = val;
    }
    return 0;
}

static PyObject*
convector_tuple(PyObject* tuple, ConvParams* params)
{
    if (!ConvecotrEnterRecCall(params)) {
        return NULL;
    }

    Py_ssize_t size = PyTuple_GET_SIZE(tuple);
    PyObject* res = PyTuple_New(size);
    if (!res) {
        return NULL;
    }

    int r = convector_array(TUPLE_ITEMS(tuple), size, TUPLE_ITEMS(res), params);
    ConvecotrLeaveRecCall(params);
    if (r < 0) {
        Py_DECREF(res);
        return NULL;
    }
    return convector_type(Py_TYPE(tuple), res);
}

static PyObject*
convector_tuple_as_list(PyObject* tuple, ConvParams* params)
{
    if (!ConvecotrEnterRecCall(params)) {
        return NULL;
    }

    Py_ssize_t size = PyTuple_GET_SIZE(tuple);
    PyObject* res = PyList_New(size);
    if (!res) {
        return NULL;
    }

    int r = convector_array(TUPLE_ITEMS(tuple), size, LIST_ITEMS(res), params);
    ConvecotrLeaveRecCall(params);
    if (r < 0) {
        Py_DECREF(res);
        return NULL;
    }
    return res;
}

static PyObject*
convector_list(PyObject* list, ConvParams* params)
{
    if (!ConvecotrEnterRecCall(params)) {
        return NULL;
    }

    Py_ssize_t size = PyList_GET_SIZE(list);
    PyObject* res = PyList_New(size);
    if (!res) {
        return NULL;
    }

    int r = convector_array(LIST_ITEMS(list), size, LIST_ITEMS(res), params);
    ConvecotrLeaveRecCall(params);
    if (r < 0) {
        Py_DECREF(res);
        return NULL;
    }
    return convector_type(Py_TYPE(list), res);
}

static PyObject*
convector_any_set(PyObject* set, ConvParams* params)
{
    if (!ConvecotrEnterRecCall(params)) {
        return NULL;
    }

    PyObject *val, *res, *item;
    res = Py_IS_TYPE(set, &PyFrozenSet_Type) ? PyFrozenSet_New(NULL)
                                             : PySet_New(NULL);
    if (!res) {
        return NULL;
    }

    Py_ssize_t pos = 0;
    ObjectConverter converter = params->conv;
    while (_PySet_Next(set, &pos, &item)) {
        val = converter(item, params);
        if (!val) {
            goto error;
        }
        if (PySet_Add(res, val) < 0) {
            goto error;
        }
    }

    ConvecotrLeaveRecCall(params);
    return convector_type(Py_TYPE(set), res);

error:
    Py_DECREF(res);
    return NULL;
}

static PyObject*
convector_set_as_list(PyObject* set, ConvParams* params)
{
    if (!ConvecotrEnterRecCall(params)) {
        return NULL;
    }

    PyObject* res = PyList_New(PySet_GET_SIZE(set));
    if (!res) {
        return NULL;
    }

    Py_ssize_t pos = 0, i = 0;
    PyObject *item, *val, **items = LIST_ITEMS(res);
    ObjectConverter converter = params->conv;
    while (_PySet_Next(set, &pos, &item)) {
        val = converter(item, params);
        if (!val) {
            Py_DECREF(res);
            return NULL;
        }
        items[i++] = val;
    }

    ConvecotrLeaveRecCall(params);
    return res;
}

int
_Conv_Get(PyTypeObject* tp, PyObject* attr)
{
    if (Meta_IS_SUBCLASS(tp)) {
        return _DATA_MODEL_POS;
    }

    if (!(tp->tp_flags & Py_TPFLAGS_HEAPTYPE)) {
        if (tp == &PyLong_Type)
            return _INT_POS;
        if (tp == &PyUnicode_Type)
            return _STR_POS;
        if (tp == &PyTuple_Type)
            return _TUPLE_POS;
        if (tp == &PyList_Type)
            return _LIST_POS;
        if (tp == &PyDict_Type)
            return _DICT_POS;
        if (tp == PyNone_Type)
            return _NONE_POS;
        if (tp == &PyFloat_Type)
            return _FLOAT_POS;
        if (tp == &PyBool_Type)
            return _BOOL_POS;
        if (tp == &PyBytes_Type || tp == &PyByteArray_Type)
            return _BYTES_POS;
        if (tp == &PySet_Type || tp == &PyFrozenSet_Type)
            return _SET_POS;
        if (tp == PyDateTimeAPI->DateType)
            return _DATE_POS;
        if (tp == PyDateTimeAPI->TimeType)
            return _TIME_POS;
        if (tp == PyDateTimeAPI->DateTimeType)
            return _DATE_TIME_POS;
        if (tp == (PyTypeObject*)ValidationErrorType)
            return _VALIDATIO_ERR_POS;
    } else if (tp == PyUuidType) {
        return _UUID_POS;
    }

    if (attr && PyObject_HasAttr((PyObject*)tp, attr)) {
        return -2;
    }

    switch (tp->tp_flags &
            (Py_TPFLAGS_LONG_SUBCLASS | Py_TPFLAGS_UNICODE_SUBCLASS |
             Py_TPFLAGS_BYTES_SUBCLASS | Py_TPFLAGS_TUPLE_SUBCLASS |
             Py_TPFLAGS_LIST_SUBCLASS | Py_TPFLAGS_DICT_SUBCLASS)) {
        case Py_TPFLAGS_LONG_SUBCLASS:
            return _INT_POS;
        case Py_TPFLAGS_UNICODE_SUBCLASS:
            return _STR_POS;
        case Py_TPFLAGS_BYTES_SUBCLASS:
            return _BYTES_POS;
        case Py_TPFLAGS_TUPLE_SUBCLASS:
            return _TUPLE_POS;
        case Py_TPFLAGS_LIST_SUBCLASS:
            return _LIST_POS;
        case Py_TPFLAGS_DICT_SUBCLASS:
            return _DICT_POS;
    }

    if (PyType_IsSubtype(tp, &PyFloat_Type))
        return _FLOAT_POS;
    if (PyType_IsSubtype(tp, PyDateTimeAPI->DateType))
        return _DATE_POS;
    if (PyType_IsSubtype(tp, PyDateTimeAPI->TimeType))
        return _TIME_POS;
    if (PyType_IsSubtype(tp, PyDateTimeAPI->DateTimeType))
        return _DATE_TIME_POS;
    if (PyType_IsSubtype(tp, &PySet_Type) ||
        PyType_IsSubtype(tp, &PyFrozenSet_Type))
        return _SET_POS;
    if (PyType_IsSubtype(tp, &PyByteArray_Type))
        return _BYTES_POS;
    if (PyType_IsSubtype(tp, (PyTypeObject*)PyEnumType))
        return _ENUM_POS;
    if (PyType_IsSubtype(tp, PyUuidType))
        return _UUID_POS;
    return -1;
}

int
Convector_IsConstVal(PyObject* val)
{
    switch (_Conv_Get(Py_TYPE(val), NULL)) {
        case _UUID_POS:
        case _BYTES_POS:
        case _DATE_TIME_POS:
        case _TIME_POS:
        case _DATE_POS:
        case _FLOAT_POS:
        case _STR_POS:
        case _INT_POS:
        case _NONE_POS:
            return 1;
        default:
            return 0;
    }
}

static PyObject*
as_dict(PyObject* val,
        ConvParams* conv_params,
        PyObject* attr,
        const ObjectConverter* convector)
{
    int ind = _Conv_Get(Py_TYPE(val), attr);
    if (ind < 0) {
        if (ind == -2) {
            return PyObject_CallMethodNoArgs(val, attr);
        }
        return PyErr_Format(
          PyExc_TypeError,
          "Unsupported type %.100s. The '%u' method is not defined",
          Py_TYPE(val)->tp_name,
          attr);
    }

    if (ind == _DATA_MODEL_POS) {
        return _DataModel_AsDict(val, conv_params, NULL, NULL);
    }
    if (ind == _VALIDATIO_ERR_POS) {
        return _ValidationError_AsList(val, conv_params);
    }
    return convector[ind](val, conv_params);
}

int
Convector_ValidateInclue(PyObject* include, PyObject* exclude)
{
    if (include && !(include == Py_None || Py_IS_TYPE(include, &PySet_Type))) {
        PyErr_Format(PyExc_ValueError,
                     "The parameter 'include' should be set or None, but "
                     "received '%.100s'",
                     Py_TYPE(include)->tp_name);
        return -1;
    }

    if (exclude && !(exclude == Py_None || Py_IS_TYPE(exclude, &PySet_Type))) {
        PyErr_Format(PyExc_ValueError,
                     "The parameter 'exclude' should be set or None, but "
                     "received '%.100s'",
                     Py_TYPE(exclude)->tp_name);
        return -1;
    }
    return 0;
}

const static ObjectConverter convector_object[CONVECTOR_SIZE] = {
    [_STR_POS] = convector_const,           [_BYTES_POS] = convector_const,
    [_NONE_POS] = convector_const,          [_FLOAT_POS] = convector_const,
    [_TUPLE_POS] = convector_tuple,         [_BOOL_POS] = convector_const,
    [_INT_POS] = convector_const,           [_LIST_POS] = convector_list,
    [_DICT_POS] = convector_dict,           [_SET_POS] = convector_any_set,
    [_VALIDATIO_ERR_POS] = convector_const, [_DATA_MODEL_POS] = convector_const,
    [_DATE_POS] = convector_const,          [_TIME_POS] = convector_const,
    [_DATE_TIME_POS] = convector_const,     [_ENUM_POS] = convector_const,
    [_UUID_POS] = convector_const,

};

const static ObjectConverter convector_as_dict_as_json[CONVECTOR_SIZE] = {
    [_STR_POS] = convector_const,           [_BYTES_POS] = convector_decode,
    [_NONE_POS] = convector_const,          [_FLOAT_POS] = convector_const,
    [_TUPLE_POS] = convector_tuple_as_list, [_BOOL_POS] = convector_const,
    [_INT_POS] = convector_const,           [_LIST_POS] = convector_list,
    [_DICT_POS] = convector_dict,           [_SET_POS] = convector_set_as_list,
    [_VALIDATIO_ERR_POS] = convector_const, [_DATA_MODEL_POS] = convector_const,
    [_DATE_POS] = convector_const,          [_TIME_POS] = convector_const,
    [_DATE_TIME_POS] = convector_const,     [_ENUM_POS] = convector_const,
    [_UUID_POS] = convector_const,
};

inline PyObject*
AsDictJson(PyObject* val, ConvParams* conv_params)
{
    return as_dict(val, conv_params, __as_json__, convector_as_dict_as_json);
}

inline PyObject*
AsDict(PyObject* val, ConvParams* conv_params)
{
    return as_dict(val, conv_params, __as_dict__, convector_object);
}

PyObject*
Copy(PyObject* val, ConvParams* conv_params)
{
    PyTypeObject* tp = Py_TYPE(val);
    int ind = _Conv_Get(tp, __copy__);
    if (ind < 0) {
        if (ind == -2) {
            return PyObject_CallMethodNoArgs(val, __copy__);
        }
        return PyErr_Format(
          PyExc_TypeError,
          "Unsupported type %.100s. The '__copy__' method is not defined",
          tp->tp_name);
    }
    if (ind == _DATA_MODEL_POS) {
        return _DataModel_Copy(val);
    }
    return convector_object[ind](val, conv_params);
}

inline PyObject*
CopyNoKwargs(PyObject* obj)
{
    ConvParams conv_params = ConvParams_Create(Copy);
    return Copy(obj, &conv_params);
}

inline PyObject*
AsDictNoKwargs(PyObject* obj)
{
    ConvParams conv_params = ConvParams_Create(AsDict);
    return AsDict(obj, &conv_params);
}

inline PyObject*
PyCopy(PyObject* obj)
{
    ConvParams conv_params = ConvParams_Create(Copy);
    return Copy(obj, &conv_params);
}

int
convector_setup(void)
{
    PyDateTime_IMPORT;
    return PyDateTimeAPI ? 0 : -1;
}

void
convector_free(void)
{
}