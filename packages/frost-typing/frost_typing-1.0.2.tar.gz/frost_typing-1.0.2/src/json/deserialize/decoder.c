#include "utils_common.h"
#include "json/json.h"

static PyObject*
json_parse_infinity(ReadBuffer*);
static PyObject*
json_parse_true(ReadBuffer*);
static PyObject*
json_parse_false(ReadBuffer*);
static PyObject*
json_parse_null(ReadBuffer*);
static PyObject*
json_parse_nan(ReadBuffer*);
static PyObject*
json_parse_negatic(ReadBuffer*);
static PyObject*
json_parse_array(ReadBuffer*);
static PyObject*
json_parse_dict(ReadBuffer*);
PyObject* JsonDecodeError;
typedef PyObject* (*parser)(ReadBuffer*);
static PyObject*
json_parse_continue(UNUSED ReadBuffer* buff)
{
    return NULL;
}

static const parser parse_router[256] = {
    ['I'] = json_parse_infinity,  ['t'] = json_parse_true,
    ['f'] = json_parse_false,     ['n'] = json_parse_null,
    ['N'] = json_parse_nan,       ['-'] = json_parse_negatic,
    ['"'] = JsonParse_String,     ['['] = json_parse_array,
    ['{'] = json_parse_dict,      ['0'] = JsonParse_Numeric,
    ['1'] = JsonParse_Numeric,    ['2'] = JsonParse_Numeric,
    ['3'] = JsonParse_Numeric,    ['4'] = JsonParse_Numeric,
    ['5'] = JsonParse_Numeric,    ['6'] = JsonParse_Numeric,
    ['7'] = JsonParse_Numeric,    ['8'] = JsonParse_Numeric,
    ['9'] = JsonParse_Numeric,    ['\b'] = json_parse_continue,
    ['\f'] = json_parse_continue, ['\n'] = json_parse_continue,
    ['\r'] = json_parse_continue, ['\t'] = json_parse_continue,
    [' '] = json_parse_continue,
};

static void
json_parse_raise(ReadBuffer* buffer)
{
    Py_ssize_t line, column;
    ReadBuffer_GetPos(buffer, &column, &line);
    PyErr_Format(JsonDecodeError,
                 "invalid literal: line %zu"
                 " column %zu (char '%c')",
                 line,
                 column,
                 *buffer->iter);
}

static PyObject*
json_parse_dict(ReadBuffer* buffer)
{
    int is_key = 1;
    PyObject* key = NULL;
    PyObject* dict = PyDict_New();
    Py_ssize_t cnt_sep = 0;
    if (dict == NULL) {
        return NULL;
    }

    for (buffer->iter++; buffer->iter != buffer->end_data; buffer->iter++) {
        unsigned char ch = (unsigned char)*buffer->iter;
        parser p = parse_router[ch];
        if (p) {
            if (p == json_parse_continue) {
                continue;
            }

            PyObject* tmp = p(buffer);
            if (!tmp) {
                goto error;
            }

            if (is_key) {
                if (!PyUnicode_CheckExact(tmp)) {
                    Py_DECREF(tmp);
                    goto error;
                }
                key = tmp;
            } else {
                int r = Dict_SetItem_String(dict, key, tmp);
                Py_DECREF(key);
                Py_DECREF(tmp);
                if (r < 0) {
                    goto error;
                }
                is_key = 1;
            }
            buffer->iter--;
            continue;
        }

        switch (ch) {
            case ':':
                if (is_key) {
                    is_key = 0;
                    continue;
                }
                goto error;
            case ',':
                if (!is_key || (++cnt_sep != PyDict_GET_SIZE(dict))) {
                    goto error;
                }
                continue;
            case '}':
                if (is_key && (!(cnt_sep && PyDict_GET_SIZE(dict)) ||
                               cnt_sep == (PyDict_GET_SIZE(dict) - 1))) {
                    buffer->iter++;
                    return dict;
                }
                goto error;
            default:
                goto error;
        }
    }

error:
    if (!is_key) {
        Py_XDECREF(key);
    }
    Py_DECREF(dict);
    return NULL;
}

static PyObject*
json_parse_array(ReadBuffer* buffer)
{
    Py_ssize_t cnt_sep = 0;
    PyObject* list = PyList_New(0);
    if (list == NULL) {
        return NULL;
    }

    for (buffer->iter++; buffer->iter != buffer->end_data; buffer->iter++) {
        unsigned char ch = (unsigned char)*buffer->iter;
        parser p = parse_router[ch];
        if (p) {
            if (p == json_parse_continue) {
                continue;
            }

            PyObject* tmp = p(buffer);
            if (!tmp) {
                goto error;
            }

            buffer->iter--;
            int r = PyList_Append(list, tmp);
            Py_DECREF(tmp);
            if (r < 0) {
                goto error;
            }
            continue;
        }

        if (ch == ',') {
            if (++cnt_sep == Py_SIZE(list)) {
                continue;
            }
        } else if (ch == ']') {
            if (!(cnt_sep && Py_SIZE(list)) || cnt_sep == (Py_SIZE(list) - 1)) {
                buffer->iter++;
                return list;
            }
        }
        goto error;
    }

error:
    Py_DECREF(list);
    return NULL;
}

static inline int
json_parse_pattern(ReadBuffer* buff,
                   const char* pattern,
                   Py_ssize_t pattern_size)
{
    if ((buff->end_data - buff->iter) < pattern_size) {
        return 0;
    }
    if (memcmp(buff->iter, pattern, pattern_size)) {
        return 0;
    }
    buff->iter += pattern_size;
    return 1;
}

static PyObject*
json_parse_null(ReadBuffer* buff)
{
    return json_parse_pattern(buff, "null", 4) ? Py_NewRef(Py_None) : NULL;
}

static PyObject*
json_parse_true(ReadBuffer* buff)
{
    return json_parse_pattern(buff, "true", 4) ? Py_NewRef(Py_True) : NULL;
}

static PyObject*
json_parse_false(ReadBuffer* buff)
{
    return json_parse_pattern(buff, "false", 5) ? Py_NewRef(Py_False) : NULL;
}

static PyObject*
json_parse_nan(ReadBuffer* buff)
{
    return json_parse_pattern(buff, "NaN", 3) ? PyFloat_FromDouble(NAN) : NULL;
}

static PyObject*
json_parse_infinity(ReadBuffer* buff)
{
    return json_parse_pattern(buff, "Infinity", 8)
             ? PyFloat_FromDouble(INFINITY)
             : NULL;
}

static PyObject*
json_parse_n_infinity(ReadBuffer* buff)
{
    return json_parse_pattern(buff, "-Infinity", 9)
             ? PyFloat_FromDouble(-INFINITY)
             : NULL;
}

static PyObject*
json_parse_negatic(ReadBuffer* buff)
{
    char* next = buff->iter + 1;
    if (next != buff->end_data && *next == 'I') {
        return json_parse_n_infinity(buff);
    }
    return JsonParse_Numeric(buff);
}

static PyObject*
json_parse(char* s, Py_ssize_t length)
{
    ReadBuffer buffer = { .start = s, .iter = s, .end_data = s + length };
    for (; buffer.iter != buffer.end_data; buffer.iter++) {
        parser p = parse_router[(unsigned char)*buffer.iter];
        if (!p) {
            goto error;
        }
        if (p == json_parse_continue) {
            continue;
        }

        PyObject* tmp = p(&buffer);
        if (!tmp) {
            if (PyErr_Occurred()) {
                return NULL;
            }
            goto error;
        }

        // Check that all characters at the end are not significant
        while (buffer.iter < buffer.end_data) {
            if (parse_router[(unsigned char)*buffer.iter++] !=
                json_parse_continue) {
                Py_DECREF(tmp);
                goto error;
            }
        }
        return tmp;
    }

error:
    json_parse_raise(&buffer);
    return NULL;
}

PyObject*
JsonParse(PyObject* obj)
{
    if (PyBytes_Check(obj)) {
        return json_parse(PyBytes_AS_STRING(obj), Py_SIZE(obj));
    } else if (PyByteArray_Check(obj)) {
        return json_parse(PyByteArray_AS_STRING(obj), Py_SIZE(obj));
    } else if (PyUnicode_Check(obj)) {
        PyObject* bytes = PyUnicode_EncodeFSDefault(obj);
        if (!bytes) {
            return NULL;
        }
        PyObject* res = json_parse(PyBytes_AS_STRING(bytes), Py_SIZE(bytes));
        Py_DECREF(bytes);
        return res;
    }
    return _RaiseInvalidType(
      "0", "string, a bytes-like object", Py_TYPE(obj)->tp_name);
}

int
decoder_setup(void)
{
    JsonDecodeError =
      PyErr_NewException("frost_typing.JsonDecodeError", NULL, NULL);
    return JsonDecodeError ? 0 : -1;
}

void
decoder_free(void)
{
    Py_DECREF(JsonDecodeError);
}