#include "json/json.h"

void
ReadBuffer_GetPos(ReadBuffer* buffer, Py_ssize_t* column, Py_ssize_t* line)
{
    Py_ssize_t c = 1;
    Py_ssize_t l = 1;
    char* st = buffer->start;
    while (st != buffer->iter) {
        char ch = *st++;
        if (ch != '\n') {
            c++;
        } else {
            l++;
            c = 1;
        }
    }
    *column = c;
    *line = l;
}
