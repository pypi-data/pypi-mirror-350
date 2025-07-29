#include "validator/validator.h"

#include "convector.h"
#include "field.h"
#include "json_schema.h"
#include "schema.h"
#include "stddef.h"
#include "valid_model.h"
#include "validated_func.h"
#include "json/json.h"

#define FUNC_GET_FLAGS(f)                                                      \
    (_CAST(PyCodeObject*, _CAST(PyFunctionObject*, f)->func_code)->co_flags)
#define FUNC_GET_KWONLY_CNT(f)                                                 \
    ((_CAST(PyCodeObject*, _CAST(PyFunctionObject*, f)->func_code)             \
        ->co_kwonlyargcount))

#define HAS_COROUTINE(f) ((FUNC_GET_FLAGS(f) & CO_COROUTINE) != 0)
#define HAS_VARARGS(f) ((FUNC_GET_FLAGS(f) & CO_VARARGS) != 0)
#define HAS_VARKEYWORDS(f) ((FUNC_GET_FLAGS(f) & CO_VARKEYWORDS) != 0)

static PyObject* __multiple_values;

static void
func_schema_xdecref(FuncSchema schema)
{
    if (schema.name) {
        Py_XDECREF(schema.type);
        Py_XDECREF(schema.name);
        Py_XDECREF(schema.validator);
    }
}

static PyObject*
validated_func_get(PyObject* self, PyObject* obj, UNUSED PyObject* type)
{
    if (obj == NULL || obj == Py_None) {
        return Py_NewRef(self);
    }
    return PyMethod_New(self, obj);
}

static void
free_func_schemas(FuncSchema* schemas, Py_ssize_t size)
{
    if (!schemas) {
        return;
    }
    for (Py_ssize_t i = 0; i != size; ++i) {
        func_schema_xdecref(schemas[i]);
    }
    PyMem_Free(schemas);
}

static void
validated_func_dealloc(ValidatedFunc* self)
{
    if (self->size) {
        free_func_schemas(self->validators, self->size);
    }
    Py_DECREF(self->func);
    Py_XDECREF(self->gtypes);
    Py_XDECREF(self->head.ctx);
    func_schema_xdecref(self->a_validator);
    func_schema_xdecref(self->r_validator);
}

static PyObject*
validated_func_repr(ValidatedFunc* self)
{
    int r = Py_ReprEnter((PyObject*)self);
    if (r != 0) {
        if (r > 0) {
            return PyUnicode_FromFormat("%U(...)", self->func->func_name);
        }
        return NULL;
    }

    _PyUnicodeWriter writer;
    Py_ssize_t argscnt, size = self->size;
    argscnt = _CAST(PyCodeObject*, self->func->func_code)->co_argcount;

    writer.overallocate = 1;
    _PyUnicodeWriter_Init(&writer);
    writer.min_length = size * 10;

    _UNICODE_WRITE_STR(&writer, self->func->func_name);
    _UNICODE_WRITE_CHAR(&writer, '(');
    for (Py_ssize_t i = 0; i != size; ++i) {
        if (i) {
            _UNICODE_WRITE_STRING(&writer, ", ", 2);
        }
        if (i == argscnt) {
            _UNICODE_WRITE_STRING(&writer, ", *", 2);
            if (self->a_validator.name) {
                if (_PyUnicodeWriter_WriteStr(&writer, self->a_validator.name) <
                    0) {
                    goto error;
                }
                _UNICODE_WRITE_STRING(&writer, ": ", 2);
                _UNICODE_WRITE(
                  &writer, self->a_validator.validator, PyObject_Repr);
            }
        }
        if (_PyUnicodeWriter_WriteStr(&writer, self->validators[i].name) < 0) {
            goto error;
        }
        _UNICODE_WRITE_STRING(&writer, ": ", 2);
        _UNICODE_WRITE(&writer, self->validators[i].validator, PyObject_Repr);
    }

    if (argscnt == size && self->a_validator.name) {
        _UNICODE_WRITE_STRING(&writer, ", *", 3);
        if (_PyUnicodeWriter_WriteStr(&writer, self->a_validator.name) < 0) {
            goto error;
        }
        _UNICODE_WRITE_STRING(&writer, ": ", 2);
        _UNICODE_WRITE(&writer, self->a_validator.validator, PyObject_Repr);
    }

    if (self->r_validator.name == NULL) {
        _UNICODE_WRITE_STRING(&writer, ") -> Any", 8);
    } else {
        _UNICODE_WRITE_STRING(&writer, ") -> ", 5);
        _UNICODE_WRITE(
          &writer, (PyObject*)self->r_validator.validator, PyObject_Repr);
    }

    Py_ReprLeave((PyObject*)self);
    return _PyUnicodeWriter_Finish(&writer);

error:
    _PyUnicodeWriter_Dealloc(&writer);
    Py_ReprLeave((PyObject*)self);
    return NULL;
}

static inline PyObject*
validated_func_check_result(ValidatedFunc* self,
                            PyObject* val,
                            ValidateContext* ctx)
{
    if (!val || !self->r_validator.name) {
        return val;
    }

    PyObject* res;
    TypeAdapter* vd = self->r_validator.validator;
    if (HAS_COROUTINE(self->func)) {
        res = ValidatorIterable_CreateAsync(val, ctx, vd);
    } else {
        res = TypeAdapter_Conversion(vd, ctx, val);
    }

    if (!res) {
        ValidationError_Raise(__return, vd, val, ctx->model);
    }
    Py_DECREF(val);
    return res;
}

static Py_ssize_t
searh_name(PyObject* tuple, PyObject* name)
{
    if (!tuple) {
        return -1;
    }

    PyObject** items = TUPLE_ITEMS(tuple);
    Py_ssize_t size = PyTuple_GET_SIZE(tuple);
    for (Py_ssize_t i = 0; i != size; ++i) {
        if (items[i] == name) {
            return i;
        }
    }

    const Py_hash_t hash = _Hash_String(name);
    const Py_ssize_t key_len = PyUnicode_GET_LENGTH(name);
    for (Py_ssize_t i = 0; i != size; ++i) {
        PyObject* k = items[i];
        if ((_CAST(PyASCIIObject*, k)->hash == hash &&
             key_len == PyUnicode_GET_LENGTH(k) &&
             !memcmp(PyUnicode_DATA(k), PyUnicode_DATA(name), key_len))) {
            return i;
        }
    }
    return -1;
}

static inline void
stack_decref(PyObject** stack, Py_ssize_t size)
{
    for (Py_ssize_t i = 0; i < size; ++i) {
        Py_XDECREF(stack[i]);
    }
}

static PyObject*
validated_func_get_default_args(ValidatedFunc* self,
                                Py_ssize_t total_args,
                                Py_ssize_t index)
{
    if (self->func->func_defaults == NULL) {
        return NULL;
    }

    Py_ssize_t defaults_count = PyTuple_GET_SIZE(self->func->func_defaults);
    Py_ssize_t required_args_count = total_args - defaults_count;
    if (index < required_args_count) {
        return NULL;
    }

    Py_ssize_t default_index = index - required_args_count;
    if (index < total_args && default_index < defaults_count) {
        return CopyNoKwargs(
          PyTuple_GET_ITEM(self->func->func_defaults, default_index));
    }

    return NULL;
}

static PyObject*
validated_func_get_default_kwargs(ValidatedFunc* self, PyObject* name)
{
    PyObject* kwdefaults = self->func->func_kwdefaults;
    if (kwdefaults == NULL) {
        return NULL;
    }
    PyObject* res = _PyDict_GetItem_Ascii(kwdefaults, name);
    return res ? CopyNoKwargs(res) : NULL;
}

static inline int
validate_args(TypeAdapter* self,
              ValidateContext* ctx,
              PyObject* name,
              PyObject* val,
              PyObject** res,
              PyObject** err)
{
    *res = TypeAdapter_Conversion(self, ctx, val);
    if (!*res) {
        return ValidationError_CREATE(name, self, val, ctx->model, err);
    }
    return 0;
}

static Py_ssize_t
validated_func_args_stack(ValidatedFunc* self,
                          PyObject** args,
                          Py_ssize_t nargsf,
                          PyObject** stack,
                          PyObject* kwnames,
                          PyObject** err,
                          Py_ssize_t* iter,
                          ValidateContext* ctx)
{
    TypeAdapter* validator;
    PyObject *val, *name;
    Py_ssize_t argscnt, size, ind, j = 0, i = 0;

    size = self->size;
    argscnt = _CAST(PyCodeObject*, self->func->func_code)->co_argcount;
    for (; i < argscnt && i < nargsf && j != size; ++j, i++) {
        name = self->validators[j].name;
        validator = self->validators[j].validator;
        ind = searh_name(kwnames, name);
        if (ind > -1) {
            PyErr_Format(PyExc_TypeError,
                         "%.100U() got multiple values for argument '%U'",
                         self->func->func_name,
                         name);
            goto error;
        }

        val = args[i];
        if (validate_args(validator, ctx, name, val, stack + i, err) < 0) {
            goto error;
        }
    }

    for (; i < argscnt && j != size; ++j, i++) {
        name = self->validators[j].name;
        validator = self->validators[j].validator;

        ind = searh_name(kwnames, name);
        if (ind < 0) {
            val = validated_func_get_default_args(self, argscnt, i);
            if (!val &&
                ValidationError_CREATE_MISSING(name, NULL, self, err) < 0) {
                goto error;
            }
            stack[i] = val;
            continue;
        }

        val = args[nargsf + ind];
        if (validate_args(validator, ctx, name, val, stack + i, err) < 0) {
            goto error;
        }
    }

    if (self->a_validator.name) {
        name = self->a_validator.name;
        validator = self->a_validator.validator;
        for (; i < nargsf; ++i) {
            val = args[i];
            PyObject* tmp = TypeAdapter_Conversion(validator, ctx, val);
            if (!tmp) {
                if (ValidationError_CreateAttrIdx(name,
                                                  i - argscnt,
                                                  validator,
                                                  val,
                                                  ctx->model,
                                                  (ValidationError**)err) < 0) {
                    goto error;
                }
            }
            stack[i] = tmp;
        }
    }

    for (; j != size; ++j, i++) {
        name = self->validators[j].name;
        validator = self->validators[j].validator;

        ind = searh_name(kwnames, name);
        if (ind < 0) {
            val = validated_func_get_default_kwargs(self, name);
            if (!val &&
                ValidationError_CREATE_MISSING(name, NULL, self, err) < 0) {
                goto error;
            }
            stack[i] = val;
            continue;
        }

        val = args[nargsf + ind];
        if (validate_args(validator, ctx, name, val, stack + i, err) < 0) {
            goto error;
        }
    }

    *iter = i;
    return j;

error:
    *iter = i;
    return -1;
}

static PyObject*
validated_func_vector_call_ctx(ValidatedFunc* self,
                               PyObject** args,
                               size_t nargsf,
                               PyObject* kwn,
                               ValidateContext* ctx)
{
    Py_ssize_t total_size, kwonly;
    Py_ssize_t i, nargs, stack_size, argscnt;
    PyObject* small_stack[FASTCALL_SMALL_STACK];
    PyObject **stack, *res = NULL, *names = NULL, *err = NULL;

    nargs = PyVectorcall_NARGS(nargsf);
    total_size = kwn ? nargs + PyTuple_GET_SIZE(kwn) : nargs;
    stack_size = Py_MAX(self->size, total_size);
    argscnt = _CAST(PyCodeObject*, self->func->func_code)->co_argcount;
    const char* func_name = (const char*)PyUnicode_DATA(self->func->func_name);

    if (!self->a_validator.name &&
        !PyCheck_MaxArgs(func_name, nargs, argscnt)) {
        return NULL;
    }

    if (!VectorCall_CheckKwStrOnly(kwn)) {
        return NULL;
    }

    if (stack_size <= FASTCALL_SMALL_STACK) {
        stack = small_stack;
    } else {
        stack = PyMem_Malloc(stack_size * sizeof(PyObject*));
        if (!stack) {
            return PyErr_NoMemory();
        }
    }

    i = validated_func_args_stack(
      self, args, nargs, stack, kwn, &err, &total_size, ctx);
    if (i < 0) {
        goto done;
    }

    if (err) {
        ValidationError_RaiseWithModel((ValidationError*)err, ctx->model);
        err = NULL;
        goto done;
    }

    kwonly = FUNC_GET_KWONLY_CNT(self->func);
    if (kwonly) {
        names = PyTuple_New(kwonly);
        if (!names) {
            goto done;
        }
        for (Py_ssize_t j = 0; j < kwonly; ++j) {
            PyObject* name = self->validators[self->size - j - 1].name;
            PyTuple_SET_ITEM(names, j, Py_NewRef(name));
        }
    }

    nargsf = total_size - kwonly;
    res = PyObject_Vectorcall((PyObject*)self->func, stack, nargsf, names);
    Py_XDECREF(names);

    res = validated_func_check_result(self, res, ctx);

done:
    Py_XDECREF(err);
    stack_decref(stack, total_size);
    if (stack != small_stack) {
        PyMem_Free(stack);
    }

    return res;
}

static ContextManager*
validated_func_get_ctx(ValidModel* self)
{
    ContextManager* context_manager = _CAST(ValidModel*, self)->ctx;
    if (context_manager) {
        return context_manager;
    }

    context_manager = ContextManager_CREATE(self);
    if (!context_manager) {
        return NULL;
    }
    _CAST(ValidModel*, self)->ctx = context_manager;
    return context_manager;
}

static PyObject*
validated_func_vector_call(ValidatedFunc* self,
                           PyObject** args,
                           size_t nargsf,
                           PyObject* kwn)
{
    ContextManager* ctx = validated_func_get_ctx((ValidModel*)self);
    if (!ctx) {
        return NULL;
    }
    ValidateContext vctx =
      ValidateContext_Create(ctx, self, ctx, FIELD_ALLOW_INF_NAN);
    return validated_func_vector_call_ctx(self, args, nargsf, kwn, &vctx);
}

ValidatedFunc*
ValidatedFunc_Create(PyTypeObject* type, PyFunctionObject* func)
{
    ValidatedFunc* self;
    TypeAdapter* validator;
    Py_ssize_t names_cnt, argscnt, size;
    PyObject *name, *hint, *annot, *co_varnames;
    FuncSchema *validators = NULL, a_validator = { NULL },
               r_validator = { NULL };

    if (HAS_VARKEYWORDS(func)) {
        PyErr_Format(PyExc_ValueError,
                     "%.100S It is not allowed to use kwargs only",
                     func);
        return NULL;
    }

    annot = PyFunction_GetAnnotations((PyObject*)func);
    if (!annot) {
        PyErr_Format(
          PyExc_ValueError, "%.100S has no attribute '__annotations__'", func);
        return NULL;
    }

    co_varnames = PyObject_GetAttrString(func->func_code, "co_varnames");
    if (!co_varnames) {
        return NULL;
    }
    if (!PyTuple_Check(co_varnames)) {
        _RaiseInvalidType(
          "co_varnames", "tuple", Py_TYPE(co_varnames)->tp_name);
        Py_XDECREF(co_varnames);
        return NULL;
    }

    argscnt = _CAST(PyCodeObject*, func->func_code)->co_argcount;
    size = argscnt + FUNC_GET_KWONLY_CNT(func) + HAS_VARARGS(func);
    names_cnt = size - HAS_VARARGS(func);
    if (names_cnt) {
        validators = PyMem_Malloc(names_cnt * sizeof(FuncSchema));
        if (validators == NULL) {
            Py_XDECREF(co_varnames);
            return NULL;
        }
        memset(validators, 0, names_cnt * sizeof(FuncSchema));
    }

    for (Py_ssize_t i = 0, j = 0; i < size; i++) {
        name = PyTuple_GET_ITEM(co_varnames, i);
        hint = PyDict_GetItem(annot, name);
        if (!hint) {
            hint = PyAny;
        }

        validator = ParseHint(hint, NULL);
        if (!validator) {
            goto error;
        }
        if (i == argscnt && HAS_VARARGS(func)) {
            a_validator = (FuncSchema){ .validator = validator,
                                        .name = Py_NewRef(name),
                                        .type = Py_NewRef(hint) };
        } else {
            validators[j++] = (FuncSchema){ .validator = validator,
                                            .name = Py_NewRef(name),
                                            .type = Py_NewRef(hint) };
        }
    }
    Py_XDECREF(co_varnames);

    hint = PyDict_GetItem(annot, __return);
    if (hint != NULL) {
        validator = ParseHint(hint, NULL);
        if (validator == NULL) {
            goto error;
        }
        r_validator = (FuncSchema){ .validator = validator,
                                    .name = Py_NewRef(__return),
                                    .type = Py_NewRef(hint) };
    }

    self = (ValidatedFunc*)type->tp_alloc(type, 0);
    if (self == NULL) {
        goto error;
    }

    Py_INCREF(func);
    self->func = func;
    self->size = names_cnt;
    self->validators = validators;
    self->a_validator = a_validator;
    self->r_validator = r_validator;
    self->vectorcall = (vectorcallfunc)validated_func_vector_call;
    self->gtypes = _Object_Gettr((PyObject*)func, __type_params__);
    return self;
error:
    func_schema_xdecref(r_validator);
    func_schema_xdecref(a_validator);
    free_func_schemas(validators, names_cnt);
    return NULL;
}

static PyFunctionObject*
validated_func_parse_args(PyObject* args, PyObject* kwargs)
{
    if (!_PyArg_NoKeywords("validated_func.__new__", kwargs)) {
        return NULL;
    }

    PyFunctionObject* func;
    if (!PyArg_ParseTuple(
          args, "O!:validated_func.__new__", &PyFunction_Type, &func)) {
        return NULL;
    }
    return func;
}

static PyObject*
validated_func_new(PyTypeObject* type, PyObject* args, PyObject* kwargs)
{
    PyFunctionObject* func = validated_func_parse_args(args, kwargs);
    return func ? (PyObject*)ValidatedFunc_Create(type, func) : NULL;
}

static PyObject*
validated_func_from_json(ValidatedFunc* self,
                         PyObject* const* args,
                         size_t nargs,
                         PyObject* kwnames)
{
    Py_ssize_t cnt = PyVectorcall_NARGS(nargs);
    if (!PyCheck_ArgsCnt(".from_json", cnt, 1)) {
        return NULL;
    }

    PyObject* obj = (PyObject*)*args;
    PyObject* dict = JsonParse(obj);
    if (!dict) {
        ValidationError_RaiseInvalidJson(obj, (PyObject*)self);
        return NULL;
    }

    if (!PyDict_Check(dict)) {
        ValidationError_RaiseModelType((PyObject*)self, dict);
        Py_DECREF(dict);
        return NULL;
    }

    if (_Dict_MergeKwnames(dict, args + cnt, kwnames) < 0) {
        Py_DECREF(dict);
        return NULL;
    }

    PyObject* res = PyObject_Call((PyObject*)self, VoidTuple, dict);
    Py_DECREF(dict);
    return res;
}

static PyObject*
sequence_set_key(PyTypeObject* cls,
                 ContextManager* ctx,
                 PyObject* args,
                 PyObject* kwargs,
                 PyObject* obj)
{
    PyFunctionObject* func;
    if (obj) {
        if (!Py_IS_TYPE(obj, &PyFunction_Type)) {
            return PyErr_Format(PyExc_TypeError,
                                "validated_func.__new__() argument must be a "
                                "funtionc, not '%.100s'",
                                Py_TYPE(obj)->tp_name);
        }
        func = (PyFunctionObject*)obj;
    } else {
        func = validated_func_parse_args(args, kwargs);
        if (!func) {
            return NULL;
        }
    }

    if (ctx->gtypes) {
        if (PyObject_SetAttr((PyObject*)func, __type_params__, ctx->gtypes) <
            0) {
            return NULL;
        }
    }
    return (PyObject*)ValidatedFunc_Create(cls, func);
}

static PyObject*
validated_func_from_subscript(PyTypeObject* cls, PyObject* key)
{
    PyObject* gtypes;
    if (PyTuple_Check(key)) {
        gtypes = Py_NewRef(key);
    } else {
        gtypes = PyTuple_Pack(1, key);
        if (!gtypes) {
            return NULL;
        }
    }

    PyObject* res = (PyObject*)_ContextManager_CreateGetItem(
      (PyObject*)cls, gtypes, key, (ContextManagerCall)sequence_set_key);
    Py_DECREF(gtypes);
    return res;
}

static PyMethodDef validated_func_methods[] = {
    { "__class_getitem__",
      (PyCFunction)validated_func_from_subscript,
      METH_CLASS | METH_O | METH_COEXIST,
      NULL },
    { "json_schema", (PyCFunction)Schema_JsonSchema, METH_NOARGS, NULL },
    { "from_json",
      (PyCFunction)validated_func_from_json,
      METH_FASTCALL | METH_KEYWORDS,
      NULL },
    { NULL }
};

static PyObject*
get_func(ValidatedFunc* self, UNUSED void* m)
{
    return Py_NewRef((PyObject*)self->func);
}

static PyObject*
get_name(ValidatedFunc* self, UNUSED void* m)
{
    return Py_NewRef(self->func->func_name);
}

static void
unpacking_args_free(PyObject** array, Py_ssize_t nargs, PyObject* kwnames)
{
    Py_ssize_t total_size = nargs + (kwnames ? PyTuple_GET_SIZE(kwnames) : 0);
    for (Py_ssize_t i = 0; i != total_size; i++) {
        Py_DECREF(array[i]);
    }
    PyObject_Free(array);
    Py_XDECREF(kwnames);
}

static PyObject**
unpacking_args(PyObject** array,
               Py_ssize_t nargs,
               PyObject* kwargs,
               PyObject** kwnames)
{
    Py_ssize_t kw_size = kwargs ? PyDict_GET_SIZE(kwargs) : 0;
    Py_ssize_t total_size = nargs + kw_size;
    PyObject** args = PyObject_Malloc(BASE_SIZE * total_size);
    if (!args) {
        PyErr_NoMemory();
        return NULL;
    }

    for (Py_ssize_t i = 0; i != nargs; i++) {
        args[i] = Py_NewRef(array[i]);
    }

    if (kwargs) {
        PyObject* kwn = PyTuple_New(kw_size);
        if (!kwn) {
            unpacking_args_free(args, nargs, NULL);
            return NULL;
        }

        *kwnames = kwn;

        Py_ssize_t pos = 0, j = 0;
        PyObject *name, *val;

        while (PyDict_Next(kwargs, &pos, &name, &val)) {
            args[nargs + j] = Py_NewRef(val);
            PyTuple_SET_ITEM(kwn, j, Py_NewRef(name));
            j++;
        }
    }
    return args;
}

static PyObject*
validated_func_call_frost_validate(ValidatedFunc* self,
                                   ContextManager* ctx,
                                   PyObject* args,
                                   PyObject* kwargs,
                                   PyObject* obj)
{
    if (obj) {
        if (!PyDict_Check(obj)) {
            PyErr_SetString(PyExc_ValueError, "Not a callable object");
            return NULL;
        }
        kwargs = obj;
    }

    PyObject **f_args, *res, *kwn = NULL;
    Py_ssize_t nargs = PyTuple_GET_SIZE(args);
    f_args = unpacking_args(TUPLE_ITEMS(args), nargs, kwargs, &kwn);
    if (!f_args) {
        return NULL;
    }

    ValidateContext vctx =
      ValidateContext_Create(ctx, self, ctx, FIELD_ALLOW_INF_NAN);
    res = validated_func_vector_call_ctx(self, f_args, nargs, kwn, &vctx);
    unpacking_args_free(f_args, nargs, kwn);
    return res;
}

static PyObject*
validated_func_get_item(ValidatedFunc* self, PyObject* key)
{
    return _ContextManager_CreateGetItem(
      (PyObject*)self,
      self->gtypes,
      key,
      (ContextManagerCall)validated_func_call_frost_validate);
};

static PyMappingMethods validated_func_map_methods = {
    .mp_subscript = (binaryfunc)validated_func_get_item,
};

static PyGetSetDef validated_func_getsets[] = {
    { "__func__", (getter)get_func, NULL, NULL, NULL },
    { "__name__", (getter)get_name, NULL, NULL, NULL },
    { 0 }
};

PyTypeObject ValidatedFuncType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_dealloc =
      (destructor)validated_func_dealloc,
    .tp_vectorcall_offset = offsetof(ValidatedFunc, vectorcall),
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_VECTORCALL,
    .tp_descr_get = (descrgetfunc)validated_func_get,
    .tp_as_mapping = &validated_func_map_methods,
    .tp_repr = (reprfunc)validated_func_repr,
    .tp_name = "frost_typing.validated_func",
    .tp_basicsize = sizeof(ValidatedFunc),
    .tp_methods = validated_func_methods,
    .tp_getset = validated_func_getsets,
    .tp_call = PyVectorcall_Call,
    .tp_new = validated_func_new,
};

int
validated_func_setup(void)
{
    CREATE_VAR_INTERN___STING(multiple_values);
    return PyType_Ready(&ValidatedFuncType);
}

void
validated_func_free(void)
{
    Py_DECREF(&ValidatedFuncType);
    Py_DECREF(__multiple_values);
}