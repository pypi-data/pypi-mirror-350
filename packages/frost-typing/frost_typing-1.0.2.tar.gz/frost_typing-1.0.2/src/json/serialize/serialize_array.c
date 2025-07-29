#include "utils_common.h"
#include "json/json.h"

static int
array_as_json(WriteBuffer* buff,
              PyObject** data_ptr,
              Py_ssize_t length,
              ConvParams* params)
{
    if (!length) {
        return WriteBuffer_ConcatSize(buff, "[]", 2);
    }

    if (_Encode_Enter(buff) < 0) {
        return -1;
    }

    BUFFER_CONCAT_CHAR(buff, '[');
    PyObject** end = data_ptr + length;
    if (_PyObject_AsJson(buff, *data_ptr++, params) < 0) {
        return -1;
    }

    while (data_ptr != end) {
        buff->buffer[buff->size++] = ',';
        if (_PyObject_AsJson(buff, *data_ptr++, params) < 0) {
            return -1;
        }
    }

    buff->buffer[buff->size++] = ']';
    _Encode_Leave(buff);
    return 0;
}

int
_Set_AsJson(WriteBuffer* buff, PyObject* obj, ConvParams* params)
{
    if (!PySet_GET_SIZE(obj)) {
        return WriteBuffer_ConcatSize(buff, "[]", 2);
    }

    if (_Encode_Enter(buff) < 0) {
        return -1;
    }

    BUFFER_CONCAT_CHAR(buff, '[');

    PyObject* item;
    Py_ssize_t pos = 0;
    _PySet_Next(obj, &pos, &item);
    if (_PyObject_AsJson(buff, item, params) < 0) {
        return -1;
    }

    while (_PySet_Next(obj, &pos, &item)) {
        buff->buffer[buff->size++] = ',';
        if (_PyObject_AsJson(buff, item, params) < 0) {
            return -1;
        }
    }

    buff->buffer[buff->size++] = ']';
    _Encode_Leave(buff);
    return 0;
}

int
_Tuple_AsJson(WriteBuffer* buff, PyObject* obj, ConvParams* params)
{
    return array_as_json(buff, TUPLE_ITEMS(obj), PyTuple_GET_SIZE(obj), params);
}

int
_List_AsJson(WriteBuffer* buff, PyObject* obj, ConvParams* params)
{
    return array_as_json(buff, LIST_ITEMS(obj), PyList_GET_SIZE(obj), params);
}
