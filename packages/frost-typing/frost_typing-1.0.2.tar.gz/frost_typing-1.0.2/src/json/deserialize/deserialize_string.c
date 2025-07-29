#include "json/json.h"

#define MAX_UNICODE 0x10ffff

static const Py_UCS1 escape_table[256] = {
    ['\\'] = '\\', ['"'] = '"',  ['b'] = '\b', ['f'] = '\f',
    ['n'] = '\n',  ['r'] = '\r', ['t'] = '\t'
};

const Py_UCS1 hex_table[256] = {
    [0x00] = 255, [0x01] = 255, [0x02] = 255, [0x03] = 255, [0x04] = 255,
    [0x05] = 255, [0x06] = 255, [0x07] = 255, [0x08] = 255, [0x09] = 255,
    [0x0A] = 255, [0x0B] = 255, [0x0C] = 255, [0x0D] = 255, [0x0E] = 255,
    [0x0F] = 255, [0x10] = 255, [0x11] = 255, [0x12] = 255, [0x13] = 255,
    [0x14] = 255, [0x15] = 255, [0x16] = 255, [0x17] = 255, [0x18] = 255,
    [0x19] = 255, [0x1A] = 255, [0x1B] = 255, [0x1C] = 255, [0x1D] = 255,
    [0x1E] = 255, [0x1F] = 255, [' '] = 255,  ['!'] = 255,  ['"'] = 255,
    ['#'] = 255,  ['$'] = 255,  ['%'] = 255,  ['&'] = 255,  ['\''] = 255,
    ['('] = 255,  [')'] = 255,  ['*'] = 255,  ['+'] = 255,  [','] = 255,
    ['-'] = 255,  ['.'] = 255,  ['/'] = 255,  ['0'] = 0,    ['1'] = 1,
    ['2'] = 2,    ['3'] = 3,    ['4'] = 4,    ['5'] = 5,    ['6'] = 6,
    ['7'] = 7,    ['8'] = 8,    ['9'] = 9,    [':'] = 255,  [';'] = 255,
    ['<'] = 255,  ['='] = 255,  ['>'] = 255,  ['?'] = 255,  ['@'] = 255,
    ['A'] = 10,   ['B'] = 11,   ['C'] = 12,   ['D'] = 13,   ['E'] = 14,
    ['F'] = 15,   ['G'] = 255,  ['H'] = 255,  ['I'] = 255,  ['J'] = 255,
    ['K'] = 255,  ['L'] = 255,  ['M'] = 255,  ['N'] = 255,  ['O'] = 255,
    ['P'] = 255,  ['Q'] = 255,  ['R'] = 255,  ['S'] = 255,  ['T'] = 255,
    ['U'] = 255,  ['V'] = 255,  ['W'] = 255,  ['X'] = 255,  ['Y'] = 255,
    ['Z'] = 255,  ['['] = 255,  ['\\'] = 255, [']'] = 255,  ['^'] = 255,
    ['_'] = 255,  ['`'] = 255,  ['a'] = 10,   ['b'] = 11,   ['c'] = 12,
    ['d'] = 13,   ['e'] = 14,   ['f'] = 15,   ['g'] = 255,  ['h'] = 255,
    ['i'] = 255,  ['j'] = 255,  ['k'] = 255,  ['l'] = 255,  ['m'] = 255,
    ['n'] = 255,  ['o'] = 255,  ['p'] = 255,  ['q'] = 255,  ['r'] = 255,
    ['s'] = 255,  ['t'] = 255,  ['u'] = 255,  ['v'] = 255,  ['w'] = 255,
    ['x'] = 255,  ['y'] = 255,  ['z'] = 255,  ['{'] = 255,  ['|'] = 255,
    ['}'] = 255,  ['~'] = 255,  [0x7F] = 255, [0x80] = 255, [0x81] = 255,
    [0x82] = 255, [0x83] = 255, [0x84] = 255, [0x85] = 255, [0x86] = 255,
    [0x87] = 255, [0x88] = 255, [0x89] = 255, [0x8A] = 255, [0x8B] = 255,
    [0x8C] = 255, [0x8D] = 255, [0x8E] = 255, [0x8F] = 255, [0x90] = 255,
    [0x91] = 255, [0x92] = 255, [0x93] = 255, [0x94] = 255, [0x95] = 255,
    [0x96] = 255, [0x97] = 255, [0x98] = 255, [0x99] = 255, [0x9A] = 255,
    [0x9B] = 255, [0x9C] = 255, [0x9D] = 255, [0x9E] = 255, [0x9F] = 255,
    [0xA0] = 255, [0xFF] = 255
};

static int
decode_unicode(char** cursor, char* end, Py_UCS4* res)
{
    char* cur = *cursor;
    if (end - cur < 4) {
        return -1;
    }

    Py_UCS1 d0 = hex_table[(unsigned char)cur[0]];
    Py_UCS1 d1 = hex_table[(unsigned char)cur[1]];
    Py_UCS1 d2 = hex_table[(unsigned char)cur[2]];
    Py_UCS1 d3 = hex_table[(unsigned char)cur[3]];
    if ((d0 | d1 | d2 | d3) == 255) {
        return -1;
    }

    *res = (d0 << 12) | (d1 << 8) | (d2 << 4) | d3;
    // must stay on the last character
    *cursor += 3;
    return 0;
}

static inline void
filling_string_1(Py_UCS1* data, char* cur, char* end)
{
    int slash = 0;

    Py_UCS1 ch;
    for (; cur != end; cur++) {
        ch = *cur;
        if (!slash) {
            if (ch == '\\') {
                slash = 1;
                continue;
            }
            *data++ = ch;
            continue;
        }

        slash = 0;
        Py_UCS1 esc = escape_table[ch];
        if (esc) {
            *data++ = esc;
        } else if (ch == 'u') {
            cur++;
            Py_UCS4 u_ch = 0;
            decode_unicode(&cur, end, &u_ch);
            *data++ = (Py_UCS1)u_ch;
        }
    }
}

static inline void
filling_string_2(Py_UCS2* data, char* cur, char* end)
{
    int slash = 0;
    Py_UCS2 ch;

    for (; cur != end; cur++) {
        ch = *cur;
        if (!slash) {
            if (ch == '\\') {
                slash = 1;
                continue;
            }

            Py_UCS2 c = 0;
            if ((ch & 0x80) == 0) {
                c = ch;
            } else if ((ch & 0xE0) == 0xC0) {
                c = ((ch & 0x1F) << 6);
                c |= (*++cur & 0x3F);
            } else if ((ch & 0xF0) == 0xE0) {
                c = ((ch & 0x0F) << 12);
                c |= ((*++cur & 0x3F) << 6);
                c |= (*++cur & 0x3F);
            }
            *data++ = c;
            continue;
        }
        slash = 0;
        Py_UCS1 esc = escape_table[ch];
        if (esc) {
            *data++ = esc;
        } else if (ch == 'u') {
            cur++;
            Py_UCS4 u_ch = 0;
            decode_unicode(&cur, end, &u_ch);
            *data++ = (Py_UCS2)u_ch;
        }
    }
}

static inline void
filling_string_4(Py_UCS4* data, char* cur, char* end)
{
    int slash = 0;
    Py_UCS1 ch;

    for (; cur != end; cur++) {
        ch = *cur;
        if (!slash) {
            if (ch == '\\') {
                slash = 1;
                continue;
            }

            Py_UCS4 c;
            if ((ch & 0x80) == 0) {
                c = ch;
            } else if ((ch & 0xE0) == 0xC0) {
                c = ((ch & 0x1F) << 6);
                c |= (*++cur & 0x3F);
            } else if ((ch & 0xF0) == 0xE0) {
                c = ((ch & 0x0F) << 12);
                c |= ((*++cur & 0x3F) << 6);
                c |= (*++cur & 0x3F);
            } else {
                c = ((ch & 0x07) << 18);
                c |= ((*++cur & 0x3F) << 12);
                c |= ((*++cur & 0x3F) << 6);
                c |= (*++cur & 0x3F);
            }

            *data++ = c;
            continue;
        }
        slash = 0;
        Py_UCS1 esc = escape_table[ch];
        if (esc) {
            *data++ = esc;
        } else if (ch == 'u') {
            cur++;
            Py_UCS4 u_ch = 0;
            decode_unicode(&cur, end, &u_ch);
            if (Py_UNICODE_IS_HIGH_SURROGATE(u_ch) && (cur + 5) < end &&
                *(cur + 1) == '\\' && *(cur + 2) == 'u') {
                cur += 3;
                Py_UCS4 u_ch2 = 0;
                decode_unicode(&cur, end, &u_ch2);
                if (Py_UNICODE_IS_LOW_SURROGATE(u_ch2)) {
                    *data++ = Py_UNICODE_JOIN_SURROGATES(u_ch, u_ch2);
                } else {
                    *data++ = u_ch;
                    *data++ = u_ch2;
                }
            } else {
                *data++ = u_ch;
            }
        }
    }
}

static inline PyObject*
parse_string(char* cur, char* end, Py_UCS4 max_char, Py_ssize_t size)
{
    PyObject* res = PyUnicode_New(size, max_char);
    if (!res) {
        return NULL;
    }

    void* data = PyUnicode_DATA(res);
    if (max_char < 128 && (end - cur) == size) {
        memcpy(data, cur, size);
    } else if (max_char < 256) {
        filling_string_1(data, cur, end);
    } else if (max_char < 65536) {
        filling_string_2(data, cur, end);
    } else {
        if (max_char > MAX_UNICODE) {
            PyErr_SetString(PyExc_SystemError,
                            "invalid maximum character passed "
                            "to PyUnicode_New");
            return NULL;
        }
        filling_string_4(data, cur, end);
    }
    return res;
}

PyObject*
JsonParse_String(ReadBuffer* buffer)
{
    int slash = 0;
    Py_ssize_t size = 0;
    Py_UCS4 max_char = '\0';
    char *st, *cur, *end;
    st = cur = ++buffer->iter;
    end = buffer->end_data;

    for (; cur != end; cur++) {
        Py_UCS1 ch = *cur;
        if (!slash) {
            if (ch == '\\') {
                slash = 1;
                continue;
            }
            if (ch == '"') {
                PyObject* res = parse_string(st, cur, max_char, size);
                buffer->iter = res ? cur + 1 : cur;
                return res;
            }

            Py_UCS4 c;
            if ((ch & 0x80) == 0) {
                c = ch;
            } else if ((ch & 0xE0) == 0xC0) {
                if (cur + 2 > end) {
                    return NULL;
                }
                c = ((ch & 0x1F) << 6);
                c |= (*++cur & 0x3F);
            } else if ((ch & 0xF0) == 0xE0) {
                if (cur + 3 > end) {
                    return NULL;
                }
                c = ((ch & 0x0F) << 12);
                c |= ((*++cur & 0x3F) << 6);
                c |= (*++cur & 0x3F);
            } else if ((ch & 0xF8) == 0xF0) {
                if (cur + 4 > end) {
                    return NULL;
                }
                c = ((ch & 0x07) << 18);
                c |= ((*++cur & 0x3F) << 12);
                c |= ((*++cur & 0x3F) << 6);
                c |= (*++cur & 0x3F);
            } else {
                return NULL;
            }

            if (c > max_char) {
                max_char = c;
            }
            size++;
            continue;
        }

        slash = 0;
        if (escape_table[ch]) {
            size++;
        } else if (ch == 'u') {
            cur++;
            Py_UCS4 u_ch = 0;
            if (decode_unicode(&cur, end, &u_ch) < 0) {
                return NULL;
            }
            if (Py_UNICODE_IS_HIGH_SURROGATE(u_ch) && (cur + 5) < end &&
                *(cur + 1) == '\\' && *(cur + 2) == 'u') {
                cur += 3;
                Py_UCS4 u_ch2 = 0;
                if (decode_unicode(&cur, end, &u_ch2) < 0) {
                    return NULL;
                }
                if (Py_UNICODE_IS_LOW_SURROGATE(u_ch2)) {
                    u_ch = Py_UNICODE_JOIN_SURROGATES(u_ch, u_ch2);
                } else {
                    size++;
                    if (u_ch2 > max_char) {
                        max_char = u_ch2;
                    }
                }
            }
            size++;
            if (u_ch > max_char) {
                max_char = u_ch;
            }
        } else {
            return NULL;
        }
    }

    buffer->iter = cur - 1;
    return NULL;
}
