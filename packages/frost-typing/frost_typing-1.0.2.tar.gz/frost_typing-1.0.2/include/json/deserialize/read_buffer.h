typedef struct ReadBuffer
{
    char* iter;
    char* start;
    char* end_data;
} ReadBuffer;

extern void
ReadBuffer_GetPos(ReadBuffer*, Py_ssize_t*, Py_ssize_t*);