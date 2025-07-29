#include "utils_common.h"
#include "json/json.h"

#define PYLONG_BASE (1 << PyLong_SHIFT)
#define PY_LONG_BASE ((uint64_t)(1ULL << 30))

#if PY_MINOR_VERSION < 12
#define _PyLong_IsNegative(o) (Py_SIZE(o) < 0)
#define _PyLong_DigitCount(o) Py_ABS(Py_SIZE(o))
#define PyLong_GET_DIGIT(o) ((PyLongObject*)o)->ob_digit
#else
#define SIGN_MASK 3
#define SIGN_NEGATIVE 2
#define NON_SIZE_BITS 3

static inline int
_PyLong_IsNegative(const PyLongObject* op)
{
    return (op->long_value.lv_tag & SIGN_MASK) == SIGN_NEGATIVE;
}
static inline Py_ssize_t
_PyLong_DigitCount(const PyLongObject* op)
{
    return (Py_ssize_t)(op->long_value.lv_tag >> NON_SIZE_BITS);
}
#define PyLong_GET_DIGIT(o) ((PyLongObject*)o)->long_value.ob_digit
#endif

static const uint16_t digits_u16[100] = {
#define D2(a, b) ((uint16_t)(a) | ((uint16_t)(b) << 8))
    D2('0', '0'), D2('0', '1'), D2('0', '2'), D2('0', '3'), D2('0', '4'),
    D2('0', '5'), D2('0', '6'), D2('0', '7'), D2('0', '8'), D2('0', '9'),
    D2('1', '0'), D2('1', '1'), D2('1', '2'), D2('1', '3'), D2('1', '4'),
    D2('1', '5'), D2('1', '6'), D2('1', '7'), D2('1', '8'), D2('1', '9'),
    D2('2', '0'), D2('2', '1'), D2('2', '2'), D2('2', '3'), D2('2', '4'),
    D2('2', '5'), D2('2', '6'), D2('2', '7'), D2('2', '8'), D2('2', '9'),
    D2('3', '0'), D2('3', '1'), D2('3', '2'), D2('3', '3'), D2('3', '4'),
    D2('3', '5'), D2('3', '6'), D2('3', '7'), D2('3', '8'), D2('3', '9'),
    D2('4', '0'), D2('4', '1'), D2('4', '2'), D2('4', '3'), D2('4', '4'),
    D2('4', '5'), D2('4', '6'), D2('4', '7'), D2('4', '8'), D2('4', '9'),
    D2('5', '0'), D2('5', '1'), D2('5', '2'), D2('5', '3'), D2('5', '4'),
    D2('5', '5'), D2('5', '6'), D2('5', '7'), D2('5', '8'), D2('5', '9'),
    D2('6', '0'), D2('6', '1'), D2('6', '2'), D2('6', '3'), D2('6', '4'),
    D2('6', '5'), D2('6', '6'), D2('6', '7'), D2('6', '8'), D2('6', '9'),
    D2('7', '0'), D2('7', '1'), D2('7', '2'), D2('7', '3'), D2('7', '4'),
    D2('7', '5'), D2('7', '6'), D2('7', '7'), D2('7', '8'), D2('7', '9'),
    D2('8', '0'), D2('8', '1'), D2('8', '2'), D2('8', '3'), D2('8', '4'),
    D2('8', '5'), D2('8', '6'), D2('8', '7'), D2('8', '8'), D2('8', '9'),
    D2('9', '0'), D2('9', '1'), D2('9', '2'), D2('9', '3'), D2('9', '4'),
    D2('9', '5'), D2('9', '6'), D2('9', '7'), D2('9', '8'), D2('9', '9')
#undef D2
};

int
_Long_AsJson(WriteBuffer* buff, PyObject* obj, UNUSED ConvParams* params)
{
    uint64_t val;
    const int is_neg = _PyLong_IsNegative((PyLongObject*)obj);
    Py_ssize_t size_a = _PyLong_DigitCount((PyLongObject*)obj);
    if (size_a < 2) {
        if (!size_a) {
            return WriteBuffer_ConcatChar(buff, '0');
        }

        val = PyLong_GET_DIGIT(obj)[0];
    } else {
        if (PyLong_AsByteArray(obj, (unsigned char*)&val, 8, 1, is_neg) < 0) {
            PyErr_SetString(JsonEncodeError, "Integer exceeds 64-bit range");
            return -1;
        }

        if (is_neg) {
            val = (uint64_t)(-(int64_t)val);
        }
    }

    if (WriteBuffer_Resize(buff, buff->size + 21) < 0) {
        return -1;
    }

    char* restrict p = (char*)buff->buffer + buff->size + 20;
    char* restrict end = p;
    while (val >= 100) {
        uint_fast8_t r = (uint_fast8_t)(val % 100);
        val /= 100;

        uint16_t d = digits_u16[r];
        *--p = (char)(d >> 8);
        *--p = (char)(d & 0xFF);
    }

    if (val < 10) {
        *--p = (char)('0' + val);
    } else {
        uint16_t d = digits_u16[val];
        *--p = (char)(d >> 8);
        *--p = (char)(d & 0xFF);
    }

    if (is_neg) {
        *--p = '-';
    }

    Py_ssize_t len = end - p;
    memcpy(buff->buffer + buff->size, p, len);
    buff->size += len;
    return 0;
}