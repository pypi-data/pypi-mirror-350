extern PyObject* JsonDecodeError;

extern PyObject*
JsonParse(PyObject*);
extern int
decoder_setup(void);
extern void
decoder_free(void);