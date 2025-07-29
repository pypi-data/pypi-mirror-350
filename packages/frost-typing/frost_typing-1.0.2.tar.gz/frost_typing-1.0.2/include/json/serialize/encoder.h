typedef struct WriteBuffer WriteBuffer;

typedef struct ConvParams ConvParams;
extern PyObject* JsonEncodeError;
extern PyObject*
PyObject_AsJson(PyObject* obj, PyObject* kwargs);
extern int
_Uuid_AsJson(WriteBuffer* buff, PyObject* obj, ConvParams* params);
extern int
_PyObject_AsJson(WriteBuffer* buff, PyObject* obj, ConvParams* params);
extern int
encoder_setup(void);
extern void
encoder_free(void);