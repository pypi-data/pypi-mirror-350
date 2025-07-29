#include "validator/validator.h"
#include "json/json.h"

static int
validation_error_as_json_nested(WriteBuffer* buff,
                                PyObject* obj,
                                ConvParams* params)
{
    ValidationError* v = (ValidationError*)obj;
    BUFFER_CONCAT_CHAR(buff, '{');
    BUFFER_CONCAT_SIZE(buff, "\"type\":", 7);
    if (_PyObject_AsJson(buff, v->type, params) < 0) {
        return -1;
    }

    BUFFER_CONCAT_SIZE(buff, ",\"loc\":", 7);
    if (_PyObject_AsJson(buff, v->attrs, params) < 0) {
        return -1;
    }

    BUFFER_CONCAT_SIZE(buff, ",\"input\":", 9);
    if (_PyObject_AsJson(buff, v->input_value, params) < 0) {
        return -1;
    }

    BUFFER_CONCAT_SIZE(buff, ",\"msg\":", 7);
    if (_PyObject_AsJson(buff, v->msg, params) < 0) {
        return -1;
    }

    return WriteBuffer_ConcatChar(buff, '}');
}

int
_ValidationError_AsJson(WriteBuffer* buff, PyObject* obj, ConvParams* params)
{
    ValidationError* self = (ValidationError*)obj;
    BUFFER_CONCAT_CHAR(buff, '[');
    do {
        if (validation_error_as_json_nested(buff, (PyObject*)self, params) <
            0) {
            return -1;
        }
        self = self->next;
        if (self) {
            BUFFER_CONCAT_CHAR(buff, ',');
        }
    } while (self);
    return WriteBuffer_ConcatChar(buff, ']');
}