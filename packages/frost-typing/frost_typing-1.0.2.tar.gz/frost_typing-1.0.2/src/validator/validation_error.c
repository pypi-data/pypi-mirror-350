#include "convector.h"
#include "structmember.h"
#include "validator/validator.h"
#include "vector_dict.h"
#include "json/json.h"

PyObject *ValidationErrorType, *FrostUserError;
static PyObject *__missing_type, *__msg_missing, *__msg, *__type,
  *__json_invalid_type, *__loc, *__input, *__invalid_json, *__value_error;

static void
validation_error_dealloc(ValidationError* self)
{
    Py_DECREF(self->msg);
    Py_DECREF(self->type);
    Py_XDECREF(self->next);
    Py_DECREF(self->attrs);
    Py_DECREF(self->model);
    Py_DECREF(self->input_value);
    Py_TYPE(self)->tp_base->tp_dealloc((PyObject*)self);
}

static ValidationError*
validation_error_new(PyObject* msg,
                     PyObject* attr,
                     PyObject* e_type,
                     PyObject* model,
                     PyObject* input_value)
{
    PyTypeObject* tp;
    ValidationError* self;
    PyObject *attrs, *err_type;

    if (input_value) {
        Py_NewRef(input_value);
    } else {
        input_value = PyDict_New();
        if (!input_value) {
            return NULL;
        }
    }

    if (PyUnicode_CheckExact(e_type)) {
        err_type = Py_NewRef(e_type);
    } else {
        err_type = PyObject_Str(e_type);
        if (!err_type) {
            Py_DECREF(input_value);
            return NULL;
        }
    }

    attrs = PyList_New(attr ? 1 : 0);
    if (!attrs) {
        Py_DECREF(input_value);
        Py_DECREF(err_type);
        return NULL;
    }

    if (attr) {
        PyList_SET_ITEM(attrs, 0, Py_NewRef(attr));
    }

    tp = &_ValidationErrorType;
    self = (ValidationError*)tp->tp_alloc(tp, 0);
    if (!self) {
        Py_DECREF(input_value);
        Py_DECREF(err_type);
        Py_DECREF(attrs);
        return NULL;
    }

    self->attrs = attrs;
    self->type = err_type;
    self->msg = Py_NewRef(msg);
    self->model = Py_NewRef(model);
    self->input_value = input_value;
    return self;
}

static int
validation_error_repr_nested(ValidationError* self, _PyUnicodeWriter* writer)
{
    PyTypeObject* tp = Py_TYPE(self);
    int r = Py_ReprEnter((PyObject*)self);
    if (r != 0) {
        if (r > 0) {
            _UNICODE_WRITE_STRING(writer, tp->tp_name, -1);
            return _PyUnicodeWriter_WriteASCIIString(writer, "(...)", 5);
        }
        return -1;
    }

    PyObject* val;
    Py_ssize_t size = PyList_GET_SIZE(self->attrs);
    for (Py_ssize_t i = 0; i < size; i++) {
        if (i > 0 && size > 1) {
            _UNICODE_WRITE_CHAR(writer, '.');
        }
        val = PyList_GET_ITEM(self->attrs, i);
        if (PyUnicode_Check(val)) {
            _UNICODE_WRITE_STR(writer, val);
        } else {
            _UNICODE_WRITE(writer, val, PyObject_Str);
        }
    }

    if (size) {
        _UNICODE_WRITE_CHAR(writer, '\n');
    }
    _UNICODE_WRITE_STR(writer, self->msg);
    _UNICODE_WRITE_STRING(writer, " [type=", 7)
    _UNICODE_WRITE_STR(writer, self->type);
    _UNICODE_WRITE_STRING(writer, ", input_value=", 14)
    _UNICODE_WRITE(writer, self->input_value, PyObject_Repr)
    _UNICODE_WRITE_STRING(writer, ", input_type=", 13)
    _UNICODE_WRITE_STRING(writer, Py_TYPE(self->input_value)->tp_name, -1);
    _UNICODE_WRITE_CHAR(writer, ']');
    Py_ReprLeave((PyObject*)self);
    return 0;
error:
    return -1;
}

static Py_ssize_t
validation_error_count_error(ValidationError* self)
{
    Py_ssize_t cnt = 0;
    do {
        cnt += 1;
        self = self->next;
    } while (self);
    return cnt;
}

static PyObject*
validation_error_repr(ValidationError* self)
{
    _PyUnicodeWriter writer;
    Py_ssize_t cnt;

    _PyUnicodeWriter_Init(&writer);
    writer.overallocate = 1;
    writer.min_length = 64;

    cnt = validation_error_count_error(self);
    _UNICODE_WRITE_SSIZE(&writer, cnt);
    _UNICODE_WRITE_STRING(&writer, " validation error for ", 22);
    if (_ContextManager_ReprModel(&writer, self->model) < 0) {
        goto error;
    }
    _UNICODE_WRITE_CHAR(&writer, '\n');

    do {
        if (validation_error_repr_nested(self, &writer) < 0) {
            goto error;
        }

        self = self->next;
        if (self) {
            _UNICODE_WRITE_STRING(&writer, "\n\n", 2);
        }
    } while (self);

    return _PyUnicodeWriter_Finish(&writer);
error:
    _PyUnicodeWriter_Dealloc(&writer);
    return NULL;
}

static PyObject*
validation_error_as_dict(ValidationError* self, ConvParams* params)
{
    PyObject* dict = _PyDict_NewPresized(4);
    if (PyDict_SetItem(dict, __type, self->type) < 0) {
        Py_DECREF(dict);
        return NULL;
    }
    if (PyDict_SetItem(dict, __loc, self->attrs) < 0) {
        Py_DECREF(dict);
        return NULL;
    }

    PyObject* input_value;
    if (params) {
        input_value = params->conv(self->input_value, params);
        if (!input_value) {
            Py_DECREF(dict);
            return NULL;
        }
    } else {
        input_value = Py_NewRef(self->input_value);
    }

    if (PyDict_SetItemStringDecrefVal(dict, __input, input_value) < 0) {
        Py_DECREF(dict);
        return NULL;
    }

    if (PyDict_SetItem(dict, __msg, self->msg) < 0) {
        Py_DECREF(dict);
        return NULL;
    }
    return dict;
}

static PyObject*
validation_error_as_list_nested(ValidationError* self, ConvParams* params)
{
    PyObject* list = PyList_New(0);
    if (list == NULL) {
        return NULL;
    }

    do {
        PyObject* dict = validation_error_as_dict(self, params);
        if (dict == NULL) {
            Py_DECREF(list);
            return NULL;
        }
        int r = PyList_Append(list, dict);
        Py_DECREF(dict);
        if (r < 0) {
            Py_DECREF(list);
            return NULL;
        }
        self = self->next;
    } while (self);
    return list;
}

static PyObject*
validation_error_as_list(ValidationError* self)
{
    return validation_error_as_list_nested(self, NULL);
}

inline PyObject*
_ValidationError_AsList(PyObject* self, ConvParams* params)
{
    return validation_error_as_list_nested((ValidationError*)self, params);
}

static PyObject*
validation_error_as_json(PyObject* self)
{
    return PyObject_AsJson(self, NULL);
}

static PyMethodDef validation_error_methods[] = {
    { "errors", (PyCFunction)validation_error_as_list, METH_NOARGS, NULL },
    { "as_json", (PyCFunction)validation_error_as_json, METH_NOARGS, NULL },
    { NULL }
};

static PyMemberDef validation_error_members[] = {
    { "msg", T_OBJECT, offsetof(ValidationError, msg), READONLY },
    { "loc", T_OBJECT, offsetof(ValidationError, attrs), READONLY },
    { "type", T_OBJECT, offsetof(ValidationError, type), READONLY },
    { "input_value",
      T_OBJECT,
      offsetof(ValidationError, input_value),
      READONLY },
    { NULL }
};

PyTypeObject _ValidationErrorType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_flags =
      Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASE_EXC_SUBCLASS,
    .tp_dealloc = (destructor)validation_error_dealloc,
    .tp_repr = (reprfunc)validation_error_repr,
    .tp_str = (reprfunc)validation_error_repr,
    .tp_name = "frost_typing.ValidationError",
    .tp_basicsize = sizeof(ValidationError),
    .tp_methods = validation_error_methods,
    .tp_members = validation_error_members,
};

static int
validation_error_get_activ(PyObject** res)
{
    PyObject *type, *activ, *traceback;
    PyErr_Fetch(&type, &activ, &traceback);
    if (!type) {
        *res = NULL;
        return 0;
    }

    if (PyErr_GivenExceptionMatches(type, ValidationErrorType)) {
        Py_XDECREF(traceback);
        Py_DECREF(type);
        *res = activ;
        return 1;
    }

    *res = NULL;
    if (PyErr_GivenExceptionMatches(type, FrostUserError)) {
        PyErr_Restore(type, activ, traceback);
        return -1;
    }
    Py_XDECREF(traceback);
    Py_XDECREF(activ);
    Py_DECREF(type);
    return 0;
}

static void
validation_error_set_nested(ValidationError* self, ValidationError** activ)
{
    ValidationError* current = *activ;
    if (current) {
        while (current->next) {
            current = current->next;
        }
        current->next = self;
    } else {
        *activ = self;
    }
}

static int
validation_error_set_nested_attr(ValidationError* self, PyObject* attr)
{
    if (!attr) {
        return 0;
    }

    for (ValidationError* ve = self; ve; ve = ve->next) {
        if (PyList_Insert(ve->attrs, 0, attr) < 0) {
            return -1;
        }
    }
    return 0;
}

static int
validation_error_create(PyObject* msg,
                        PyObject* attr,
                        PyObject* err_type,
                        PyObject* val,
                        PyObject* model,
                        ValidationError** err)
{
    ValidationError* activ;
    int r = validation_error_get_activ((PyObject**)&activ);
    if (r < 0) {
        return -1;
    }
    if (r) {
        if (validation_error_set_nested_attr(activ, attr) < 0) {
            Py_DECREF(activ);
            return -1;
        }
        validation_error_set_nested(activ, err);
        return 0;
    }

    ValidationError* self;
    self = validation_error_new(msg, attr, err_type, model, val);
    if (!self) {
        return -1;
    }
    validation_error_set_nested(self, err);
    return 0;
}

static int
validation_error_create_formatv(const char* msg,
                                PyObject* attr,
                                PyObject* err_type,
                                PyObject* val,
                                PyObject* model,
                                ValidationError** err,
                                va_list vargs)
{
    ValidationError* activ;
    int r = validation_error_get_activ((PyObject**)&activ);
    if (r < 0) {
        return -1;
    }
    if (r) {
        if (validation_error_set_nested_attr(activ, attr) < 0) {
            Py_DECREF(activ);
            return -1;
        }
        validation_error_set_nested(activ, err);
        return 0;
    }

    ValidationError* self;
    PyObject* s = PyUnicode_FromFormatV(msg, vargs);
    if (s == NULL) {
        return -1;
    }

    self = validation_error_new(s, attr, err_type, model, val);
    Py_DECREF(s);
    if (!self) {
        return -1;
    }
    validation_error_set_nested(self, err);
    return 0;
}

static int
validation_error_raise(PyObject* msg,
                       PyObject* attr,
                       PyObject* err_type,
                       PyObject* val,
                       PyObject* model)
{
    ValidationError* err = NULL;
    int r = validation_error_create(msg, attr, err_type, val, model, &err);
    if (r < 0) {
        return -1;
    }
    PyErr_SetObject(ValidationErrorType, (PyObject*)err);
    Py_DECREF(err);
    return 0;
}

int
ValidationError_RaiseFormat(const char* msg,
                            PyObject* attr,
                            PyObject* err_type,
                            PyObject* val,
                            PyObject* model,
                            ...)
{
    va_list vargs;
    ValidationError* err = NULL;
    va_start(vargs, model);
    int r = validation_error_create_formatv(
      msg, attr, err_type, val, model, &err, vargs);
    va_end(vargs);
    if (r < 0) {
        return -1;
    }

    PyErr_SetObject(ValidationErrorType, (PyObject*)err);
    Py_DECREF(err);
    return 0;
}

int
ValidationError_RaiseInvalidJson(PyObject* val, PyObject* model)
{
    PyObject *type, *activ, *traceback;
    PyErr_Fetch(&type, &activ, &traceback);
    if (!activ) {
        return validation_error_raise(
          __invalid_json, NULL, __json_invalid_type, val, model);
    }

    if (PyErr_GivenExceptionMatches(type, FrostUserError) ||
        PyErr_GivenExceptionMatches(type, PyExc_TypeError)) {
        PyErr_Restore(FrostUserError, activ, traceback);
        return -1;
    }

    int r = ValidationError_RaiseFormat(
      "Invalid JSON: %S", NULL, __json_invalid_type, val, model, activ);
    Py_XDECREF(traceback);
    Py_XDECREF(activ);
    Py_DECREF(type);
    return r;
}

inline int
ValidationError_Raise(PyObject* attr,
                      TypeAdapter* hint,
                      PyObject* val,
                      PyObject* model)
{
    return validation_error_raise(
      hint->err_msg, attr, (PyObject*)hint, val, model);
}

inline int
ValidationError_Create(PyObject* attr,
                       TypeAdapter* hint,
                       PyObject* val,
                       PyObject* model,
                       ValidationError** activ)
{
    return validation_error_create(
      hint->err_msg, attr, (PyObject*)hint, val, model, activ);
}

int
ValidationError_CreateAttrIdx(PyObject* attr,
                              Py_ssize_t ind,
                              TypeAdapter* hint,
                              PyObject* val,
                              PyObject* model,
                              ValidationError** activ)
{
    if (ValidationError_RaiseIndex(ind, hint, val, model) < 0) {
        return -1;
    }
    return ValidationError_Create(attr, hint, val, model, activ);
}

int
ValidationError_CreateMissing(PyObject* attr,
                              PyObject* val,
                              PyObject* model,
                              ValidationError** activ)
{
    return validation_error_create(
      __msg_missing, attr, __missing_type, val, model, activ);
}

int
ValidationError_RaiseIndex(Py_ssize_t ind,
                           TypeAdapter* hint,
                           PyObject* val,
                           PyObject* model)
{
    PyObject* index = PyLong_FromSsize_t(ind);
    if (index == NULL) {
        return -1;
    }
    int r = ValidationError_Raise(index, hint, val, model);
    Py_DECREF(index);
    return r;
}

int
ValidationError_IndexCreate(Py_ssize_t ind,
                            TypeAdapter* hint,
                            PyObject* val,
                            PyObject* model,
                            ValidationError** activ)
{
    PyObject* index = PyLong_FromSsize_t(ind);
    if (index == NULL) {
        return -1;
    }
    int r = ValidationError_Create(index, hint, val, model, activ);
    Py_DECREF(index);
    return r;
}

int
ValidationError_RaiseModelType(PyObject* model, PyObject* val)
{

    PyObject* err_type;
    if (PyType_Check(model)) {
        err_type = PyUnicode_FromString(_CAST(PyTypeObject*, model)->tp_name);
    } else {
        err_type = PyObject_Repr(model);
    }

    if (err_type == NULL) {
        return -1;
    }

    int r = ValidationError_RaiseFormat(
      "Input should be a valid %U", Long_Zero, err_type, val, model, err_type);
    Py_DECREF(err_type);
    return r;
}

void
ValidationError_RaiseWithModel(ValidationError* err, PyObject* model)
{
    ValidationError* self = err;
    do {
        Py_DECREF(err->model);
        err->model = Py_NewRef(model);
        err = err->next;
    } while (err);

    PyErr_SetObject(ValidationErrorType, (PyObject*)self);
    Py_DECREF(self);
}

int
ValidationError_ExceptionHandling(PyObject* model, PyObject* val)
{
    PyObject *type, *activ, *traceback;
    PyErr_Fetch(&type, &activ, &traceback);
    if (!type) {
        return 0;
    }

    if (PyErr_GivenExceptionMatches(type, ValidationErrorType)) {
        PyErr_Restore(type, activ, traceback);
        return 0;
    }

    if (PyErr_GivenExceptionMatches(type, FrostUserError)) {
        PyErr_Restore(type, activ, traceback);
        return -1;
    }

    if (!PyErr_GivenExceptionMatches(type, PyExc_ValueError)) {
        Py_XDECREF(traceback);
        Py_XDECREF(activ);
        Py_DECREF(type);
        return -1;
    }

    int r = ValidationError_RaiseFormat(
      "Value error, %S", NULL, __value_error, val, model, activ);
    Py_XDECREF(traceback);
    Py_XDECREF(activ);
    Py_DECREF(type);
    return r;
}

int
validation_error_setup(void)
{
    CREATE_VAR_INTERN___STING(loc);
    CREATE_VAR_INTERN___STING(msg);
    CREATE_VAR_INTERN___STING(type);
    CREATE_VAR_INTERN___STING(input);
    CREATE_VAR_INTERN___STING(value_error);

    __invalid_json = PyUnicode_FromString("Invalid JSON");
    if (__invalid_json == NULL) {
        return -1;
    }

    __msg_missing = PyUnicode_FromString("Field required");
    if (__msg_missing == NULL) {
        return -1;
    }

    __missing_type = PyUnicode_FromString("missing");
    if (__missing_type == NULL) {
        return -1;
    }

    __json_invalid_type = PyUnicode_FromString("json_invalid");
    if (__json_invalid_type == NULL) {
        return -1;
    }

    _ValidationErrorType.tp_base = (PyTypeObject*)PyExc_Exception;
    if (PyType_Ready(&_ValidationErrorType) < 0) {
        return -1;
    }

    FrostUserError =
      PyErr_NewException("frost_typing.FrostUserError", PyExc_TypeError, NULL);
    if (!FrostUserError) {
        return -1;
    }

    _ValidationErrorType.tp_new = NULL;
    ValidationErrorType = Py_NewRef((PyObject*)&_ValidationErrorType);
    return 0;
}

void
validation_error_free(void)
{
    Py_DECREF(__loc);
    Py_DECREF(__msg);
    Py_DECREF(__type);
    Py_DECREF(__input);
    Py_DECREF(__value_error);
    Py_DECREF(__msg_missing);
    Py_DECREF(__json_invalid_type);
    Py_DECREF(ValidationErrorType);
    Py_DECREF(&_ValidationErrorType);
    Py_DECREF(__missing_type);
}