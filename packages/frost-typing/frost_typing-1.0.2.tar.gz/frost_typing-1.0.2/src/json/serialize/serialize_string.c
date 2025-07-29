#include "utils_common.h"
#include "json/json.h"

static const char hex_digits[] = "0123456789ABCDEF";
static const unsigned char size_table[256] = {
    [0x00] = 6, [0x01] = 6, [0x02] = 6, [0x03] = 6, [0x04] = 6, [0x05] = 6,
    [0x06] = 6, [0x07] = 6, [0x08] = 6, [0x09] = 6, [0x0a] = 6, [0x0b] = 6,
    [0x0c] = 6, [0x0d] = 6, [0x0e] = 6, [0x0f] = 6, [0x10] = 6, [0x11] = 6,
    [0x12] = 6, [0x13] = 6, [0x14] = 6, [0x15] = 6, [0x16] = 6, [0x17] = 6,
    [0x18] = 6, [0x19] = 6, [0x1a] = 6, [0x1b] = 6, [0x1c] = 6, [0x1d] = 6,
    [0x1e] = 6, [0x1f] = 6, ['\\'] = 2, ['"'] = 2,  ['\b'] = 2, ['\f'] = 2,
    ['\n'] = 2, ['\r'] = 2, ['\t'] = 2, [0x7F] = 6,
};

static const unsigned char escape_table[256] = {
    [0x00] = 255, [0x01] = 255, [0x02] = 255,  [0x03] = 255, [0x04] = 255,
    [0x05] = 255, [0x06] = 255, [0x07] = 255,  [0x08] = 255, [0x09] = 255,
    [0x0a] = 255, [0x0b] = 255, [0x0c] = 255,  [0x0d] = 255, [0x0e] = 255,
    [0x0f] = 255, [0x10] = 255, [0x11] = 255,  [0x12] = 255, [0x13] = 255,
    [0x14] = 255, [0x15] = 255, [0x16] = 255,  [0x17] = 255, [0x18] = 255,
    [0x19] = 255, [0x1a] = 255, [0x1b] = 255,  [0x1c] = 255, [0x1d] = 255,
    [0x1e] = 255, [0x1f] = 255, ['\\'] = '\\', ['"'] = '"',  ['\b'] = 'b',
    ['\f'] = 'f', ['\n'] = 'n', ['\r'] = 'r',  ['\t'] = 't', [0x7F] = 255,
};

static inline Py_ssize_t
count_escape_chars_fast(unsigned char* restrict data, Py_ssize_t length)
{
    Py_ssize_t i = 0, esc_count = 0;
    for (; i + 4 < length; i += 4) {
        esc_count += size_table[data[i]];
        esc_count += size_table[data[i + 1]];
        esc_count += size_table[data[i + 2]];
        esc_count += size_table[data[i + 3]];
    }

    for (; i < length; i++) {
        esc_count += size_table[data[i]];
    }
    return esc_count;
}

static inline Py_ssize_t
count_escape_chars(unsigned char* restrict data, Py_ssize_t length)
{
    Py_ssize_t esc_count = 0;
    for (Py_ssize_t i = 0; i < length; i++) {
        unsigned char ch = data[i];
        if ((ch & 0x80) == 0) {
            esc_count += size_table[ch];
        } else if ((ch & 0xE0) == 0xC0) {
            i++;
        } else if ((ch & 0xF0) == 0xE0) {
            i += 2;
        } else if ((ch & 0xF8) == 0xF0) {
            i += 3;
        }
    }
    return esc_count;
}

static inline int
unicode_fast_as_json(WriteBuffer* buff,
                     unsigned char* restrict data,
                     Py_ssize_t length)
{
    if (WriteBuffer_Resize(buff, buff->size + length + 2) < 0) {
        return -1;
    }

    unsigned char* restrict s = buff->buffer + buff->size;
    *s++ = '"';
    memcpy(s, data, length);
    s += length;
    *s++ = '"';

    buff->size += length + 2;
    return 0;
}

static int
unicode_as_json(WriteBuffer* buff,
                unsigned char* restrict data,
                Py_ssize_t length,
                Py_ssize_t esc_count)
{
    if (!esc_count) {
        return unicode_fast_as_json(buff, data, length);
    }

    Py_ssize_t extra_space = length + esc_count + 2;
    if (WriteBuffer_Resize(buff, buff->size + extra_space) < 0) {
        return -1;
    }

    unsigned char* restrict s = buff->buffer + buff->size;
    *s++ = '"';
    Py_ssize_t i = 0;
    while (i < length) {
        unsigned char ch = data[i++];
        if ((ch & 0x80) == 0) {
            unsigned char esc = escape_table[ch];
            if (esc) {
                if (esc != 255) {
                    *s++ = '\\';
                    *s++ = esc;
                } else {
                    *s++ = '\\';
                    *s++ = 'u';
                    *s++ = '0';
                    *s++ = '0';
                    *s++ = hex_digits[ch >> 4];
                    *s++ = hex_digits[ch & 0xF];
                }
            } else {
                *s++ = ch;
            }
        } else {
            *s++ = ch;
            if ((ch & 0xE0) == 0xC0) {
                *s++ = data[i++];
            } else if ((ch & 0xF0) == 0xE0) {
                *s++ = data[i++];
                *s++ = data[i++];
            } else if ((ch & 0xF8) == 0xF0) {
                *s++ = data[i++];
                *s++ = data[i++];
                *s++ = data[i++];
            }
        }
    }

    *s++ = '"';
    buff->size = (s - buff->buffer);
    return 0;
}

inline int
_Unicode_FastAsJson(WriteBuffer* buff, PyObject* obj)
{
    return unicode_fast_as_json(
      buff, PyUnicode_DATA(obj), PyUnicode_GET_LENGTH(obj));
}

int
_Bytes_AsJson(WriteBuffer* buff, PyObject* obj, UNUSED ConvParams* _)
{
    Py_ssize_t length = PyBytes_GET_SIZE(obj);
    unsigned char* data = (unsigned char*)((PyBytesObject*)obj)->ob_sval;
    Py_ssize_t esc_count = count_escape_chars(data, length);
    return unicode_as_json(buff, data, length, esc_count);
}

int
_BytesArray_AsJson(WriteBuffer* buff, PyObject* obj, UNUSED ConvParams* _)
{
    Py_ssize_t length = PyByteArray_GET_SIZE(obj);
    unsigned char* data = (unsigned char*)((PyByteArrayObject*)obj)->ob_bytes;
    Py_ssize_t esc_count = count_escape_chars(data, length);
    return unicode_as_json(buff, data, length, esc_count);
}

inline int
_Unicode_AsJson(WriteBuffer* buff, PyObject* obj, UNUSED ConvParams* _)
{
    Py_ssize_t length;
    unsigned char* data = (unsigned char*)PyUnicode_AsUTF8AndSize(obj, &length);
    if (!data) {
        return -1;
    }

    Py_ssize_t esc_count;
    if (PyUnicode_IS_COMPACT_ASCII(obj)) {
        esc_count = count_escape_chars_fast(data, length);
    } else {
        esc_count = count_escape_chars(data, length);
    }
    return unicode_as_json(buff, data, length, esc_count);
}