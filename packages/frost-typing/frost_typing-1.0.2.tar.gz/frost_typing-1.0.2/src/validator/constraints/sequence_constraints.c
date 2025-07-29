#include "validator/validator.h"

#include "structmember.h"

static PyObject*
sequence_constraint_new(PyTypeObject* type, PyObject* args, PyObject* kwargs)
{
    Py_ssize_t min_length, max_length;
    min_length = max_length = -1;
    char* kwlist[] = { "min_length", "max_length", NULL };
    if (!PyArg_ParseTupleAndKeywords(args,
                                     kwargs,
                                     "|nn:SequenceConstraints.__new__",
                                     kwlist,
                                     &min_length,
                                     &max_length)) {
        return NULL;
    }
    SequenceConstraints* self = (SequenceConstraints*)type->tp_alloc(type, 0);
    if (self == NULL) {
        return NULL;
    }
    self->min_length = min_length;
    self->max_length = max_length;
    return (PyObject*)self;
}

static PyObject*
sequence_constraint_repr(SequenceConstraints* self)
{
    return PyUnicode_FromFormat("SequenceConstraints(min_length"
                                "=%zd, max_length=%.zd)",
                                self->min_length,
                                self->max_length);
}

static void
sequence_constraint_dealloc(SequenceConstraints* self)
{
    Py_TYPE(self)->tp_free(self);
}

static PyMemberDef sequence_constraint_members[] = {
    { "max_length",
      T_PYSSIZET,
      offsetof(SequenceConstraints, max_length),
      READONLY },
    { "min_length",
      T_PYSSIZET,
      offsetof(SequenceConstraints, min_length),
      READONLY },
    { NULL }
};

PyTypeObject SequenceConstraintsType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_dealloc =
      (destructor)sequence_constraint_dealloc,
    .tp_name = "frost_typing.SequenceConstraints",
    .tp_repr = (reprfunc)sequence_constraint_repr,
    .tp_basicsize = sizeof(SequenceConstraints),
    .tp_members = sequence_constraint_members,
    .tp_new = sequence_constraint_new,
    .tp_flags = Py_TPFLAGS_DEFAULT,
};

int
sequence_constraint_setup(void)
{
    return PyType_Ready(&SequenceConstraintsType);
}

void
sequence_constraint_free(void)
{
    Py_DECREF(&SequenceConstraintsType);
}

int
_SequenceConstraints_CheckSize(TypeAdapter* validator,
                               ValidateContext* ctx,
                               PyObject* val)
{
    SequenceConstraints* con = (SequenceConstraints*)validator->args;
    Py_ssize_t length;
    if (con->min_length != -1 || con->max_length != -1) {
        length = PySequence_Length(val);
        if (length == -1) {
            return -1;
        }
        if (con->min_length != -1) {
            if (length < con->min_length) {
                ValidationError_RaiseFormat("Sequence should have at "
                                            "least %zu characters",
                                            NULL,
                                            __string_too_short,
                                            val,
                                            ctx->model,
                                            con->min_length);
                return -1;
            }
        }
        if (con->max_length != -1) {
            if (length > con->max_length) {
                ValidationError_RaiseFormat("Sequence should have at"
                                            " most %zu character",
                                            NULL,
                                            __string_too_long,
                                            val,
                                            ctx->model,
                                            con->max_length);
                return -1;
            }
        }
    }

    return 0;
}

PyObject*
SequenceConstraints_Converter(TypeAdapter* self,
                              ValidateContext* ctx,
                              PyObject* val)
{
    val = TypeAdapter_Conversion((TypeAdapter*)self->cls, ctx, val);
    if (!val) {
        return NULL;
    }

    if (_SequenceConstraints_CheckSize(self, ctx, val) < 0) {
        Py_DECREF(val);
        return NULL;
    }
    return val;
}