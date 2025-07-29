#include "field.h"
#include "json_schema.h"
#include "meta_valid_model.h"
#include "valid_model.h"
#include "validator/validator.h"
#include "json/deserialize/decoder.h"

static PyObject*
context_repr(ContextManager* self)
{
    int r = Py_ReprEnter((PyObject*)self);
    if (r) {
        return r > 0 ? PyObject_Repr(self->model) : NULL;
    }

    _PyUnicodeWriter writer;
    _PyUnicodeWriter_Init(&writer);
    writer.overallocate = 1;
    writer.min_length = 64;
    if (_ContextManager_ReprModel(&writer, self->model) < 0) {
        goto error;
    }

    if (!CTX_NUM_ITEMS(self)) {
        Py_ReprLeave((PyObject*)self);
        return _PyUnicodeWriter_Finish(&writer);
    }

    _UNICODE_WRITE_CHAR(&writer, '[');
    for (Py_ssize_t i = 0; i != CTX_NUM_ITEMS(self); i++) {
        if (i) {
            _UNICODE_WRITE_STRING(&writer, ", ", 2);
        }
        PyObject* val = self->items[i].hint;
        if (PyType_Check(val)) {
            _UNICODE_WRITE_STRING(
              &writer, _CAST(PyTypeObject*, val)->tp_name, -1);
        } else {
            _UNICODE_WRITE(&writer, val, PyObject_Repr);
        }
    }

    _UNICODE_WRITE_CHAR(&writer, ']');
    Py_ReprLeave((PyObject*)self);
    return _PyUnicodeWriter_Finish(&writer);

error:
    _PyUnicodeWriter_Dealloc(&writer);
    Py_ReprLeave((PyObject*)self);
    return NULL;
}

static void
context_dealloc(ContextManager* self)
{
    for (Py_ssize_t i = 0; i < CTX_NUM_ITEMS(self); i++) {
        Py_XDECREF(self->items[i].hint);
        Py_XDECREF(self->items[i].validator);
    }
    Py_XDECREF(self->model);
    Py_XDECREF(self->gtypes);
    Py_TYPE(self)->tp_free(self);
}

static ContextManager*
context_new(Py_ssize_t size,
            PyObject* model,
            PyObject* gtypes,
            ContextManagerCall validate_call)
{
    ContextManager* self =
      (ContextManager*)ContextManager_Type.tp_alloc(&ContextManager_Type, size);
    if (!self) {
        return NULL;
    }

    self->model = Py_NewRef(model);
    self->gtypes = Py_XNewRef(gtypes);
    self->validate_call = validate_call;
    return self;
}

static inline PyObject*
context_call(ContextManager* self, PyObject* args, PyObject* kw)
{
    if (!self->validate_call) {
        return PyErr_Format(PyExc_TypeError,
                            "'%.100s' object is not callable",
                            Py_TYPE(self)->tp_name);
    }
    return self->validate_call(self->model, self, args, kw, NULL);
}

static inline int
context_check_size(PyObject* model, PyObject* gtypes, Py_ssize_t key_size)
{
    if (!gtypes) {
        PyErr_Format(PyExc_TypeError,
                     "type '%.100s' is not subscriptable",
                     Py_TYPE(model)->tp_name);
        return 0;
    }

    Py_ssize_t gtypes_size = PyTuple_GET_SIZE(gtypes);
    return PyCheck_ArgsCnt("__class_getitem__", key_size, gtypes_size);
}

static inline PyObject*
context_creat_by_key(PyObject* model,
                     PyObject* gtypes,
                     PyObject* key,
                     ContextManagerCall validate_call)
{
    int is_tuple = PyTuple_Check(key);
    Py_ssize_t key_size = is_tuple ? PyTuple_GET_SIZE(key) : 1;
    PyObject* const* keys =
      is_tuple ? (PyObject* const*)TUPLE_ITEMS(key) : &key;
    if (!context_check_size(model, gtypes, key_size)) {
        return NULL;
    }

    ContextManager* self;
    self = context_new(key_size, model, gtypes, validate_call);
    if (!self) {
        return NULL;
    }

    PyObject* tp = (PyObject*)(PyTuple_Check(model) ? model : NULL);
    for (Py_ssize_t i = 0; i != CTX_NUM_ITEMS(self); i++) {
        PyObject* key_item = keys[i];
        TypeAdapter* validator = ParseHint(key_item, tp);
        if (!validator) {
            Py_DECREF(self);
            return NULL;
        }
        self->items[i].hint = Py_NewRef(key_item);
        self->items[i].validator = validator;
    }
    return (PyObject*)self;
}

PyObject*
_ContextManager_CreateGetItem(PyObject* model,
                              PyObject* gtypes,
                              PyObject* key,
                              ContextManagerCall call)
{
    return context_creat_by_key(model, gtypes, key, call);
}

int
_ContextManager_ReprModel(_PyUnicodeWriter* writer, PyObject* model)
{
    if (PyType_Check(model)) {
        return _PyUnicodeWriter_WriteASCIIString(
          writer, _CAST(PyTypeObject*, model)->tp_name, -1);
    }

    PyObject* name = _Object_Gettr(model, __name__);
    if (!name) {
        return _UnicodeWriter_Write(writer, model, PyObject_Repr);
    }

    int r;
    if (PyUnicode_Check(name)) {
        r = _PyUnicodeWriter_WriteStr(writer, name);
    } else {
        r = _UnicodeWriter_Write(writer, name, PyObject_Str);
    }
    Py_DECREF(name);
    return r;
}

PyObject*
_ContextManager_Get_THint(PyObject* cls, ContextManager* ctx)
{
    if (!ctx->gtypes) {
        return NULL;
    }

    PyObject** items = TUPLE_ITEMS(ctx->gtypes);
    Py_ssize_t size = PyTuple_GET_SIZE(ctx->gtypes);
    Py_ssize_t i = _ArrayFastSearh(items, cls, size);
    if (i < 0 || i >= CTX_NUM_ITEMS(ctx)) {
        return NULL;
    }

    /* Protection against recursion if the
        user has passed himself as a parameter.*/
    PyObject* res = ctx->items[i].hint;
    return _ArrayFastSearh(items, res, size) < 0 ? res : NULL;
}

int
_ContextManager_Get_TTypeAdapter(PyObject* cls,
                                 ContextManager* ctx,
                                 TypeAdapter** validator)
{
    if (!ctx->gtypes) {
        return 0;
    }

    PyObject** items = TUPLE_ITEMS(ctx->gtypes);
    Py_ssize_t size = PyTuple_GET_SIZE(ctx->gtypes);
    Py_ssize_t i = _ArrayFastSearh(items, cls, size);
    if (i < 0 || i >= CTX_NUM_ITEMS(ctx)) {
        return 0;
    }

    ContextManagerItem item = ctx->items[i];
    /* Protection against recursion if the
        user has passed himself as a parameter.*/
    if (_ArrayFastSearh(items, item.hint, size) < 0) {
        if (item.validator) {
            *validator = item.validator;
            return 1;
        }
    }
    return 0;
}

ContextManager*
_ContextManager_New(PyObject* model, ContextManagerCall call)
{
    return context_new(0, model, NULL, call);
}

int
_ParseFrostValidate(PyObject* const* args,
                    Py_ssize_t nargs,
                    PyObject** val,
                    ContextManager** ctx)
{
    if (!PyCheck_ArgsCnt("__frost_validate__", PyVectorcall_NARGS(nargs), 2)) {
        return -1;
    }

    ContextManager* context = (ContextManager*)args[1];
    if (!ContextManager_Check(context)) {
        PyErr_Format(PyExc_TypeError,
                     "__frost_validate__() argument 2 must "
                     "be ContextManager, not %.100s",
                     Py_TYPE(context)->tp_name);
        return -1;
    }

    *val = args[0];
    *ctx = context;
    return 0;
}

static inline PyObject*
context_call_frost_validate(ContextManager* self, PyObject* obj)
{
    if (!self->validate_call) {
        return PyErr_Format(PyExc_TypeError,
                            "'%.100s' object is not callable",
                            Py_TYPE(self)->tp_name);
    }
    return self->validate_call(self->model, self, VoidTuple, NULL, obj);
}

ContextManager*
_ContextManager_CreateByOld(ContextManager* self, ContextManager* ctx)
{
    Py_ssize_t size = CTX_NUM_ITEMS(self);
    ContextManager* new_ctx =
      context_new(size, self->model, self->gtypes, self->validate_call);
    if (!new_ctx) {
        return new_ctx;
    }

    Py_ssize_t array_size = ctx->gtypes ? PyTuple_GET_SIZE(ctx->gtypes) : 0;
    PyObject* const* array = ctx->gtypes ? TUPLE_ITEMS(ctx->gtypes) : NULL;
    for (Py_ssize_t i = 0; i != size; i++) {
        Py_ssize_t j = _ArrayFastSearh(array, self->items[i].hint, array_size);
        if (j < 0) {
            new_ctx->items[i].hint = Py_XNewRef(self->items[i].hint);
            continue;
        }
        ContextManagerItem item = ctx->items[j];
        new_ctx->items[i] = item;
        Py_INCREF(item.hint);
        Py_XINCREF(item.validator);
    }
    return new_ctx;
}

PyObject*
_ContextManager_FrostValidate(ContextManager* self,
                              PyObject* val,
                              ContextManager* ctx)
{
    ContextManager* new_ctx = _ContextManager_CreateByOld(self, ctx);
    if (!new_ctx) {
        return NULL;
    }

    PyObject* res = context_call_frost_validate(new_ctx, val);
    Py_DECREF(new_ctx);
    return res;
}

static PyObject*
context_frost_validate(ContextManager* self,
                       PyObject* const* args,
                       Py_ssize_t nargs)
{
    PyObject* val;
    ContextManager* ctx;
    if (_ParseFrostValidate(args, nargs, &val, &ctx) < 0) {
        return NULL;
    }
    return _ContextManager_FrostValidate(self, val, ctx);
}

static PyObject*
context_construct(ContextManager* self,
                  PyObject* const* args,
                  Py_ssize_t nargs,
                  PyObject* kwnames)
{
    if (!PyType_Check(self->model) || !MetaValid_IS_SUBCLASS(self->model)) {
        return PyErr_Format(PyExc_AttributeError,
                            "'%.100s' object has no attribute 'construct'",
                            Py_TYPE(self)->tp_name);
    }

    PyObject* res =
      _ValidModel_Construct((PyTypeObject*)self->model, args, nargs, kwnames);
    if (res && Py_IS_TYPE(res, (PyTypeObject*)self->model)) {
        Py_INCREF(self);
        _CAST(ValidModel*, res)->ctx = self;
    }
    return res;
}

static PyObject*
context_from_json(ContextManager* self,
                  PyObject* const* args,
                  Py_ssize_t nargs,
                  PyObject* kwnames)
{
    Py_ssize_t cnt = PyVectorcall_NARGS(nargs);
    if (!PyCheck_ArgsCnt(".from_json", cnt, 1)) {
        return NULL;
    }

    PyObject* obj = (PyObject*)*args;
    PyObject* dict = JsonParse(obj);
    if (!dict) {
        ValidationError_RaiseInvalidJson(obj, self->model);
        return NULL;
    }

    if (!PyDict_Check(dict)) {
        ValidationError_RaiseModelType(self->model, dict);
        Py_DECREF(dict);
        return NULL;
    }

    if (_Dict_MergeKwnames(dict, args + cnt, kwnames) < 0) {
        Py_DECREF(dict);
        return NULL;
    }

    PyObject* res = context_call_frost_validate(self, dict);
    Py_DECREF(dict);
    return res;
}

static PyObject*
context_from_attributes(ContextManager* self, PyObject* obj)
{
    if (!PyType_Check(self->model)) {
        return PyErr_Format(PyExc_AttributeError,
                            "'%R' object has no attribute 'from_attributes'",
                            self);
    }
    return context_call_frost_validate(self, obj);
}

static int
context_traverse(ContextManager* self, visitproc visit, void* arg)
{
    Py_VISIT(self->model);
    Py_VISIT(self->gtypes);
    for (Py_ssize_t i = 0; i != CTX_NUM_ITEMS(self); i++) {
        ContextManagerItem item = self->items[i];
        Py_VISIT(item.validator);
        Py_VISIT(item.hint);
    }
    return 0;
}

static int
context_clear(ContextManager* self)
{
    Py_CLEAR(self->model);
    Py_CLEAR(self->gtypes);
    for (Py_ssize_t i = 0; i != CTX_NUM_ITEMS(self); i++) {
        ContextManagerItem item = self->items[i];
        Py_CLEAR(item.validator);
        Py_CLEAR(item.hint);
    }
    return 0;
}

static PyMethodDef context_methods[] = {
    { "__frost_validate__",
      (PyCFunction)context_frost_validate,
      METH_FASTCALL,
      NULL },
    { "construct",
      (PyCFunction)context_construct,
      METH_FASTCALL | METH_KEYWORDS,
      NULL },
    { "json_schema", (PyCFunction)Schema_JsonSchema, METH_NOARGS, NULL },
    { "from_attributes", (PyCFunction)context_from_attributes, METH_O, NULL },
    { "from_json",
      (PyCFunction)context_from_json,
      METH_FASTCALL | METH_KEYWORDS,
      NULL },
    { NULL }
};

static PyObject*
get_name(ContextManager* self, UNUSED void* _)
{
    return context_repr(self);
}

static PyGetSetDef context_getsets[] = {
    { "__name__", (getter)get_name, NULL, NULL, (void*)(FIELD_INIT) },
    { NULL },
};

PyTypeObject ContextManager_Type = {
    PyVarObject_HEAD_INIT(0, 0).tp_flags =
      Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,
    .tp_traverse = (traverseproc)context_traverse,
    .tp_name = "frost_typing.ContextManager",
    .tp_dealloc = (destructor)context_dealloc,
    .tp_itemsize = sizeof(ContextManagerItem),
    .tp_basicsize = sizeof(ContextManager) - sizeof(ContextManagerItem),
    .tp_call = (ternaryfunc)context_call,
    .tp_clear = (inquiry)context_clear,
    .tp_repr = (reprfunc)context_repr,
    .tp_str = (reprfunc)context_repr,
    .tp_alloc = PyType_GenericAlloc,
    .tp_methods = context_methods,
    .tp_getset = context_getsets,
    .tp_free = PyObject_GC_Del,
};

int
context_setup(void)
{
    return PyType_Ready(&ContextManager_Type);
}

void
context_free(void)
{
}