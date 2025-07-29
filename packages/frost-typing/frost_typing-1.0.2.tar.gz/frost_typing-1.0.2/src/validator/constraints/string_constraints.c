#include "validator/validator.h"

#include "structmember.h"

#ifndef T_BOOL
#define T_BOOL Py_T_BOOL
#endif

static PyObject *_re_compile, *__string_pattern_mismatch;
PyObject *__string_too_short, *__string_too_long;

static PyObject*
string_constraint_new(PyTypeObject* type, PyObject* args, PyObject* kwargs)
{
    PyObject *strip_whitespace, *to_upper, *to_lower, *pattern;
    Py_ssize_t min_length, max_length;
    PyObject* pattern_string = NULL;
    strip_whitespace = to_upper = to_lower = Py_False;
    min_length = max_length = -1;
    pattern = NULL;

    char* kwlist[] = { "strip_whitespace", "to_upper", "to_lower", "min_length",
                       "max_length",       "pattern",  NULL };
    if (!PyArg_ParseTupleAndKeywords(args,
                                     kwargs,
                                     "|O!O!O!nnU:StringConstraints.__new__",
                                     kwlist,
                                     &PyBool_Type,
                                     &strip_whitespace,
                                     &PyBool_Type,
                                     &to_upper,
                                     &PyBool_Type,
                                     &to_lower,
                                     &min_length,
                                     &max_length,
                                     &pattern_string)) {
        return NULL;
    }

    if (to_upper == Py_True && to_lower == Py_True) {
        PyErr_SetString(PyExc_ValueError,
                        "to_upper and to_lower conflict with each other");
        return NULL;
    }

    if (pattern_string != NULL) {
        PyObject* tmp = PyObject_CallOneArg(_re_compile, pattern_string);
        if (tmp == NULL) {
            return NULL;
        }

        pattern = PyObject_GetAttrString(tmp, "match");
        Py_DECREF(tmp);
        if (pattern == NULL) {
            return NULL;
        }
    }
    StringConstraints* self = (StringConstraints*)type->tp_alloc(type, 0);
    if (self == NULL) {
        return NULL;
    }

    self->strip_whitespace = strip_whitespace == Py_True;
    self->pattern_string = Py_XNewRef(pattern_string);
    self->pattern = (PyMethodObject*)pattern;
    self->to_upper = to_upper == Py_True;
    self->to_lower = to_lower == Py_True;
    self->base.min_length = min_length;
    self->base.max_length = max_length;
    return (PyObject*)self;
}

static PyObject*
string_constraint_repr(StringConstraints* self)
{
    return PyUnicode_FromFormat("StringConstraints(strip_whitespace=%S, "
                                "to_upper=%S, to_lower=%S, "
                                "min_length=%zd, max_length=%.zd, "
                                "pattern=%R)",
                                self->strip_whitespace ? Py_True : Py_False,
                                self->to_upper ? Py_True : Py_False,
                                self->to_lower ? Py_True : Py_False,
                                self->base.min_length,
                                self->base.max_length,
                                self->pattern_string ? self->pattern_string
                                                     : Py_None);
}

static void
string_constraint_dealloc(StringConstraints* self)
{
    Py_XDECREF(self->pattern_string);
    Py_XDECREF(self->pattern);
    Py_TYPE(self)->tp_free(self);
}

static PyMemberDef string_constraint_members[] = {
    { "pattern",
      T_OBJECT,
      offsetof(StringConstraints, pattern_string),
      READONLY },
    { "strip_whitespace",
      T_BOOL,
      offsetof(StringConstraints, strip_whitespace),
      READONLY },
    { "to_upper", T_BOOL, offsetof(StringConstraints, to_upper), READONLY },
    { "to_lower", T_BOOL, offsetof(StringConstraints, to_lower), READONLY },
    { NULL }
};

PyTypeObject StringConstraintsType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_dealloc =
      (destructor)string_constraint_dealloc,
    .tp_name = "frost_typing.StringConstraints",
    .tp_repr = (reprfunc)string_constraint_repr,
    .tp_basicsize = sizeof(StringConstraints),
    .tp_members = string_constraint_members,
    .tp_new = string_constraint_new,
    .tp_flags = Py_TPFLAGS_DEFAULT,
};

int
string_constraint_setup(void)
{
    __string_pattern_mismatch = PyUnicode_FromString("string_pattern_mismatch");
    if (__string_pattern_mismatch == NULL) {
        return -1;
    }
    __string_too_long = PyUnicode_FromString("string_too_long");
    if (__string_too_long == NULL) {
        return -1;
    }

    __string_too_short = PyUnicode_FromString("string_too_short");
    if (__string_too_short == NULL) {
        return -1;
    }

    PyObject* re = PyImport_ImportModule("re");
    if (re == NULL) {
        return -1;
    }

    _re_compile = PyObject_GetAttrString(re, "compile");
    Py_DECREF(re);
    if (_re_compile == NULL) {
        return -1;
    }

    StringConstraintsType.tp_base = &SequenceConstraintsType;
    SequenceConstraintsType.tp_flags |= Py_TPFLAGS_BASETYPE;
    int r = PyType_Ready(&StringConstraintsType);
    SequenceConstraintsType.tp_flags &= ~Py_TPFLAGS_BASETYPE;
    return r;
}

void
string_constraint_free(void)
{
    Py_DECREF(_re_compile);
    Py_DECREF(__string_too_long);
    Py_DECREF(__string_too_short);
    Py_DECREF(&StringConstraintsType);
    Py_DECREF(__string_pattern_mismatch);
}

static inline int
unicode_map(int kind,
            const void* data,
            const void* res,
            Py_ssize_t length,
            Py_UCS4 (*conv)(Py_UCS4))
{
    Py_ssize_t i;
    for (i = 0; i < length; i++) {
        Py_UCS4 c = PyUnicode_READ(kind, data, i);
        PyUnicode_WRITE(kind, res, i, conv(c));
    }
    return 0;
}

static inline void
unicode_strip_whitespace(int kind,
                         Py_ssize_t length,
                         const void* data,
                         Py_ssize_t* st_ind,
                         Py_ssize_t* end_ind)
{
    Py_ssize_t st_i = 0, end_i = length, i = 0;
    for (; i < length; i++) {
        Py_UCS4 ch = PyUnicode_READ(kind, data, i);
        if (ch != ' ') {
            break;
        }
        st_i++;
    }

    for (Py_ssize_t j = length - 1; j > i; j--) {
        Py_UCS4 ch = PyUnicode_READ(kind, data, j);
        if (ch != ' ') {
            break;
        }
        end_i--;
    }
    *st_ind = st_i;
    *end_ind = end_i;
}

static PyObject*
str_trim_and_to_case(StringConstraints* con, PyObject* str)
{
    if (!con->to_lower && !con->to_upper && !con->strip_whitespace) {
        return Py_NewRef(str);
    }

    int kind = PyUnicode_KIND(str);
    void* data = PyUnicode_DATA(str);
    Py_ssize_t length = PyUnicode_GET_LENGTH(str);
    if (con->strip_whitespace) {
        Py_ssize_t st_ind, end_ind;
        unicode_strip_whitespace(kind, length, data, &st_ind, &end_ind);
        if (st_ind != 0 || end_ind != length) {
            data = ((char*)data) + st_ind * kind;
            length = end_ind - st_ind;
        } else if (!con->to_lower && !con->to_upper) {
            return Py_NewRef(str);
        }
    }

    PyObject* res = PyUnicode_New(length, PyUnicode_MAX_CHAR_VALUE(str));
    if (!res) {
        return NULL;
    }

    if (con->to_lower) {
        unicode_map(
          kind, data, PyUnicode_DATA(res), length, _PyUnicode_ToLowercase);
    } else if (con->to_upper) {
        unicode_map(
          kind, data, PyUnicode_DATA(res), length, _PyUnicode_ToUppercase);
    } else {
        memcpy(PyUnicode_DATA(res), data, length * kind);
    }
    return res;
}

PyObject*
StringConstraints_Converter(TypeAdapter* self,
                            ValidateContext* ctx,
                            PyObject* val)
{
    PyObject* tmp = TypeAdapter_Conversion((TypeAdapter*)self->cls, ctx, val);
    if (!tmp) {
        return NULL;
    }

    if (!PyUnicode_Check(tmp)) {
        Py_DECREF(tmp);
        return NULL;
    }

    StringConstraints* con = (StringConstraints*)self->args;
    PyObject* str = str_trim_and_to_case(con, tmp);
    Py_DECREF(tmp);
    if (!str) {
        return NULL;
    }

    if (_SequenceConstraints_CheckSize(self, ctx, str) < 0) {
        goto error;
    }

    if (con->pattern) {
        PyObject* pattern = PyObject_CallOneArg((PyObject*)con->pattern, str);
        if (!pattern) {
            goto error;
        }
        if (pattern == Py_None) {
            ValidationError_RaiseFormat("String should match pattern '%U'",
                                        NULL,
                                        __string_pattern_mismatch,
                                        str,
                                        ctx->model,
                                        con->pattern_string);
            Py_DECREF(pattern);
            goto error;
        }
        Py_DECREF(pattern);
    }

    val = TypeAdapter_Conversion((TypeAdapter*)self->cls, ctx, str);
    Py_DECREF(str);
    return val;

error:
    Py_DECREF(str);
    return NULL;
}