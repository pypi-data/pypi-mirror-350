#include "convector.h"
#include "data_model.h"
#include "datetime.h"
#include "math.h"
#include "meta_model.h"
#include "stdint.h"
#include "validator/validator.h"
#include "json/json.h"

typedef int (*ConverterFunc)(WriteBuffer*, PyObject*, ConvParams*);
static PyObject* __value;
PyObject* JsonEncodeError;

static int
py_enum_as_json(WriteBuffer* buff, PyObject* obj, ConvParams* params)
{
    if (_Encode_Enter(buff) < 0) {
        return -1;
    }
    PyObject* value = PyObject_GetAttr(obj, __value);
    if (value == NULL) {
        return -1;
    }
    int r = _PyObject_AsJson(buff, value, params);
    Py_DECREF(value);
    _Encode_Leave(buff);
    return r;
}

static inline int
uuid_as_json(WriteBuffer* buff, PyLongObject* value)
{
    if (WriteBuffer_Resize(buff, buff->size + 38) < 0) {
        return -1;
    }

    unsigned char bytes[16] = { 0 };
    if (PyLong_AsByteArray(value, bytes, 16, 0, 0) < 0) {
        return -1;
    }

    static const char hex[] = "0123456789abcdef";
    unsigned char* out = buff->buffer + buff->size;
    *out++ = '"';
    for (int i = 0; i < 16; ++i) {
        if (i == 4 || i == 6 || i == 8 || i == 10) {
            *out++ = '-';
        }

        *out++ = hex[bytes[i] >> 4];
        *out++ = hex[bytes[i] & 0xF];
    }
    *out++ = '"';
    buff->size += 38;
    return 0;
}

int
_Uuid_AsJson(WriteBuffer* buff, PyObject* obj, UNUSED ConvParams* params)
{
    PyObject* val = PyObject_GetAttr(obj, __int);
    if (!val) {
        return -1;
    }

    if (!PyLong_Check(val)) {
        Py_DECREF(val);
        _RaiseInvalidType("int", "int", Py_TYPE(val)->tp_name);
        return -1;
    }

    return uuid_as_json(buff, (PyLongObject*)val);
}

static int
py_bool_as_json(WriteBuffer* buff, PyObject* obj, UNUSED ConvParams* params)
{
    if (obj == Py_True) {
        return WriteBuffer_ConcatSize(buff, "true", 4);
    }
    return WriteBuffer_ConcatSize(buff, "false", 5);
}

static int
py_none_as_json(WriteBuffer* buff,
                UNUSED PyObject* obj,
                UNUSED ConvParams* params)
{
    return WriteBuffer_ConcatSize(buff, "null", 4);
}

const static ConverterFunc convector_object[CONVECTOR_SIZE] = {
    [_DATA_MODEL_POS] = _MetaModel_AsJson,
    [_INT_POS] = _Long_AsJson,
    [_BOOL_POS] = py_bool_as_json,
    [_STR_POS] = _Unicode_AsJson,
    [_BYTES_POS] = _Bytes_AsJson,
    [_NONE_POS] = py_none_as_json,
    [_TUPLE_POS] = _Tuple_AsJson,
    [_LIST_POS] = _List_AsJson,
    [_DICT_POS] = _Dict_AsJson,
    [_VALIDATIO_ERR_POS] = _ValidationError_AsJson,
    [_SET_POS] = _Set_AsJson,
    [_BYTES_ARR_POS] = _BytesArray_AsJson,
    [_FLOAT_POS] = _Float_AsJson,
    [_DATE_POS] = _Date_AsJson,
    [_TIME_POS] = _Time_AsJson,
    [_DATE_TIME_POS] = _Datetime_AsJson,
    [_ENUM_POS] = py_enum_as_json,
    [_UUID_POS] = _Uuid_AsJson,
};

int
_PyObject_AsJson(WriteBuffer* buff, PyObject* obj, ConvParams* params)
{
    PyTypeObject* tp = Py_TYPE(obj);
    int ind = _Conv_Get(tp, __as_json__);
    if (ind < 0) {
        if (ind == -2) {
            PyObject* op = PyObject_CallMethodNoArgs(obj, __as_json__);
            if (!op) {
                return -1;
            }
            int r = _PyObject_AsJson(buff, op, params);
            Py_DECREF(op);
            return r;
        }
        PyErr_Format(JsonEncodeError,
                     "An unregistered type cannot "
                     "be converted to json: '%.100s'",
                     Py_TYPE(obj)->tp_name);
        return -1;
    }
    return convector_object[ind](buff, obj, params);
}

PyObject*
PyObject_AsJson(PyObject* obj, PyObject* kwargs)
{
    ConvParams params = ConvParams_Create(NULL);
    char* kwlist[] = { "by_alias", "exclude_unset", "exclude_none", NULL };
    if (kwargs && !PyArg_ParseTupleAndKeywords(VoidTuple,
                                               kwargs,
                                               "|ppp:as_json",
                                               kwlist,
                                               &params.by_alias,
                                               &params.exclude_unset,
                                               &params.exclude_none)) {
        return NULL;
    }

    WriteBuffer buff = WriteBuffer_Create(512);
    if (buff.buffer == NULL) {
        return PyErr_NoMemory();
    }

    if (_PyObject_AsJson(&buff, obj, &params) < 0) {
        WriteBuffer_Free(&buff);
        return NULL;
    }

    PyObject* res =
      PyBytes_FromStringAndSize((const char*)buff.buffer, buff.size);
    WriteBuffer_Free(&buff);
    return res;
}

int
encoder_setup(void)
{
    if (json_date_time_setup() < 0) {
        return -1;
    }
    PyDateTime_IMPORT;
    if (PyDateTimeAPI == NULL) {
        return -1;
    }

    __value = PyUnicode_FromString("value");
    if (__value == NULL) {
        return -1;
    }
    JsonEncodeError =
      PyErr_NewException("frost_typing.JsonEncodeError", NULL, NULL);
    if (JsonEncodeError == NULL) {
        return -1;
    }
    return 0;
}

void
encoder_free(void)
{
    json_date_time_free();
    Py_DECREF(__value);
}