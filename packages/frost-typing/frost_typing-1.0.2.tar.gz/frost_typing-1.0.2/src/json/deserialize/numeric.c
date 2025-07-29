#include "json/json.h"

#define MIN(a, b) (a < b ? a : b)
#define MAX_DOUBLE_SIZE ((Py_ssize_t)308)
#define _CHAR_TO_INT(c) ((int)(c - '0'))
#define _CHAR_IS_NUM(c) (c >= '0' && c <= '9')

static void
json_parse_raise_big_long(ReadBuffer* buffer)
{
    Py_ssize_t line, column;
    ReadBuffer_GetPos(buffer, &column, &line);
    PyErr_Format(JsonDecodeError,
                 "number is big when parsed as integer"
                 ": line %zu column %zu (char '%c')",
                 line,
                 column,
                 *buffer->iter);
}

static void
json_parse_raise_infinity(ReadBuffer* buffer)
{
    Py_ssize_t line, column;
    ReadBuffer_GetPos(buffer, &column, &line);
    PyErr_Format(JsonDecodeError,
                 "number is infinity when parsed as double"
                 ": line %zu column %zu (char '%c')",
                 line,
                 column,
                 *buffer->iter);
}

static PyObject*
json_parse_e(char* start, ReadBuffer* buffer, double val)
{
    if (buffer->end_data - buffer->iter < 2) {
        return NULL;
    }
    int sign;
    double degree = 0.0;
    char ch = *(++buffer->iter);
    if (ch == '-') {
        sign = -1;
    } else if (ch == '+') {
        sign = 1;
    } else if (_CHAR_IS_NUM(ch)) {
        sign = 1;
        buffer->iter--;
    } else {
        return NULL;
    }

    for (buffer->iter++; buffer->iter != buffer->end_data; buffer->iter++) {
        ch = *buffer->iter;
        if (_CHAR_IS_NUM(ch)) {
            degree = degree * 10 + (double)_CHAR_TO_INT(ch);
        } else {
            break;
        }
    }

    val *= pow(10.0, degree * sign);
    if (isinf(val)) {
        buffer->iter = start;
        json_parse_raise_infinity(buffer);
        return NULL;
    }
    return PyFloat_FromDouble(val);
}

static PyObject*
json_parse_dobule(char* start, double val, int sign, ReadBuffer* buffer)
{
    double frac_part = 0;
    double frac_div = 1;
    int point = 0;
    char ch;

    for (; buffer->iter != buffer->end_data; buffer->iter++) {
        ch = *buffer->iter;
        if (_CHAR_IS_NUM(ch)) {
            val = val * 10 + _CHAR_TO_INT(ch);
        } else if (ch == '.') {
            point = 1;
            buffer->iter++;
            break;
        } else if (ch == 'e' || ch == 'E') {
            return json_parse_e(start, buffer, val * sign);
        } else {
            // The integer is too large
            buffer->iter = start;
            json_parse_raise_big_long(buffer);
            return NULL;
        }
    }

    // check overflow
    if (isinf(val)) {
        buffer->iter = start;
        json_parse_raise_infinity(buffer);
        return NULL;
    }
    if (!point) {
        buffer->iter = start;
        json_parse_raise_big_long(buffer);
        return NULL;
    }

    for (; buffer->iter != buffer->end_data; buffer->iter++) {
        ch = *buffer->iter;
        if (_CHAR_IS_NUM(ch)) {
            frac_part = frac_part * 10 + _CHAR_TO_INT(ch);
            frac_div *= 10.0;
        } else if (ch == 'e' || ch == 'E') {
            double d = (val + (double)frac_part / frac_div) * sign;
            return json_parse_e(start, buffer, d);
        } else {
            break;
        }
    }

    if (frac_div == 1.0) {
        buffer->iter--;
        return NULL;
    }

    // check overflow
    if (isinf(val)) {
        buffer->iter = start;
        json_parse_raise_infinity(buffer);
        return NULL;
    }

    double d = (val + (double)frac_part / frac_div) * sign;
    return PyFloat_FromDouble(d);
}

static PyObject*
json_parse_unsigned_numeric(ReadBuffer* buffer)
{
    unsigned long long interger = 0;
    char ch, *st, *end;
    st = buffer->iter;
    end = MIN(buffer->end_data, buffer->iter + 19);
    for (; buffer->iter != end; buffer->iter++) {
        ch = *buffer->iter;
        if (_CHAR_IS_NUM(ch)) {
            interger = interger * 10 + _CHAR_TO_INT(ch);
        } else if (ch == '.') {
            return json_parse_dobule(st, (double)interger, 1, buffer);
        } else if (ch == 'e' || ch == 'E') {
            return json_parse_e(st, buffer, (double)interger);
        } else {
            return PyLong_FromUnsignedLongLong(interger);
        }
    }

    // check overflow
    if (interger > PY_LLONG_MAX) {
        buffer->iter = st;
        json_parse_raise_big_long(buffer);
        return NULL;
    }
    if ((end != buffer->end_data) && _CHAR_IS_NUM(*buffer->iter)) {
        return json_parse_dobule(st, (double)interger, 1, buffer);
    }
    return PyLong_FromUnsignedLongLong(interger);
}

static PyObject*
json_parse_negativ_numeric(ReadBuffer* buffer)
{
    unsigned long long interger = 0;
    char ch, *st, *end;
    st = buffer->iter;
    end = MIN(buffer->end_data, buffer->iter + 19);

    for (buffer->iter++; buffer->iter != end; buffer->iter++) {
        ch = *buffer->iter;
        if (_CHAR_IS_NUM(ch)) {
            interger = interger * 10 + _CHAR_TO_INT(ch);
        } else if (ch == '.') {
            return json_parse_dobule(st, (double)interger, -1, buffer);
        } else if (ch == 'e' || ch == 'E') {
            return json_parse_e(st, buffer, (double)interger);
        } else {
            return PyLong_FromLongLong(((long long)interger) * -1);
        }
    }

    // checks overflow
    if ((interger > PY_LLONG_MAX) ||
        (end != buffer->end_data && _CHAR_IS_NUM(*buffer->iter))) {
        return json_parse_dobule(st, (double)interger, -1, buffer);
    }
    return PyLong_FromLongLong(((long long)interger) * -1);
}

PyObject*
JsonParse_Numeric(ReadBuffer* buffer)
{
    if (*buffer->iter == '-') {
        return json_parse_negativ_numeric(buffer);
    }
    return json_parse_unsigned_numeric(buffer);
}