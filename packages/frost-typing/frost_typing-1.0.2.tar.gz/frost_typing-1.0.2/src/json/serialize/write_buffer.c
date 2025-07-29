#include "json/json.h"

#define RECURSION_LIMIT 254

int
_Encode_Enter(WriteBuffer* buff)
{
    if (buff->nesting_level++ > RECURSION_LIMIT) {
        PyErr_SetString(PyExc_RecursionError,
                        "maximum recursion depth exceeded"
                        " while encoding a JSON object");
        return -1;
    }
    return 0;
}

inline void
_Encode_Leave(WriteBuffer* buff)
{
    buff->nesting_level--;
}

inline Py_ssize_t
write_buffer_new_size(Py_ssize_t size, Py_ssize_t new_size)
{
    do {
        size *= 2;
    } while (size < new_size);
    return size;
}

int
WriteBuffer_Resize(WriteBuffer* buffer, Py_ssize_t size)
{
    size += 2; // For separators
    if (buffer->buffer_size >= size) {
        return 0;
    }

    size = write_buffer_new_size(buffer->buffer_size, size);
    unsigned char* new_buffer = PyMem_Realloc(buffer->buffer, size);
    if (new_buffer == NULL) {
        PyErr_NoMemory();
        return -1;
    }
    buffer->buffer_size = size;
    buffer->buffer = new_buffer;
    return 0;
}

inline int
WriteBuffer_ConcatChar(WriteBuffer* buffer, char ch)
{
    if (WriteBuffer_Resize(buffer, buffer->size + 1) < 0) {
        return -1;
    }
    buffer->buffer[buffer->size++] = ch;
    return 0;
}

inline int
WriteBuffer_ConcatSize(WriteBuffer* buffer, char* data, Py_ssize_t size)
{
    Py_ssize_t new_size = buffer->size + size;
    if (WriteBuffer_Resize(buffer, new_size) < 0) {
        return -1;
    }
    memcpy(buffer->buffer + buffer->size, data, size);
    buffer->size = new_size;
    return 0;
}

inline void
WriteBuffer_Free(WriteBuffer* buffer)
{
    PyMem_Free(buffer->buffer);
}
