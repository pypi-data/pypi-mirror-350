#define BUFFER_CONCAT_CHAR(b, c)                                               \
    if (WriteBuffer_ConcatChar(b, c) < 0) {                                    \
        return -1;                                                             \
    }

#define BUFFER_CONCAT_SIZE(b, d, s)                                            \
    if (WriteBuffer_ConcatSize(b, d, s) < 0) {                                 \
        return -1;                                                             \
    }

typedef struct WriteBuffer
{
    Py_ssize_t nesting_level;
    Py_ssize_t buffer_size;
    Py_ssize_t size;
    unsigned char* buffer;
} WriteBuffer;

#define WriteBuffer_Create(presize)                                            \
    (WriteBuffer)                                                              \
    {                                                                          \
        .size = 0, .nesting_level = 0, .buffer_size = presize,                 \
        .buffer = PyMem_Malloc(presize),                                       \
    }

extern int
WriteBuffer_ConcatChar(WriteBuffer*, char);
extern int
WriteBuffer_Resize(WriteBuffer*, Py_ssize_t);
extern int
WriteBuffer_ConcatSize(WriteBuffer*, char*, Py_ssize_t);
extern void
WriteBuffer_Free(WriteBuffer*);
extern int
_Encode_Enter(WriteBuffer*);
extern void
_Encode_Leave(WriteBuffer*);