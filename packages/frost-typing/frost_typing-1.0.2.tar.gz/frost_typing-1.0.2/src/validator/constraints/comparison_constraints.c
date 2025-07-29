#include "validator/validator.h"

#include "structmember.h"

static PyObject *__greater_than, *__greater_than_equal, *__less_than,
  *__less_than_equal;

static PyObject*
comparison_constraints_repr(ComparisonConstraints* self)
{
    return PyUnicode_FromFormat("ComparisonConstraints(gt=%.100R, "
                                "ge=%.100R, lt=%.100R, le=%.100R)",
                                self->gt ? self->gt : Py_None,
                                self->ge ? self->ge : Py_None,
                                self->lt ? self->lt : Py_None,
                                self->le ? self->le : Py_None);
}

static PyObject*
comparison_constraints_new(PyTypeObject* type, PyObject* args, PyObject* kwargs)
{
    PyObject *gt, *ge, *lt, *le;
    gt = ge = lt = le = NULL;
    char* kwlist[] = { "gt", "ge", "lt", "le", NULL };
    if (!PyArg_ParseTupleAndKeywords(args,
                                     kwargs,
                                     "|OOOO:ComparisonConstraints.__new__",
                                     kwlist,
                                     &gt,
                                     &ge,
                                     &lt,
                                     &le)) {
        return NULL;
    }
    PyObject* self = type->tp_alloc(type, 0);
    if (self == NULL) {
        return NULL;
    }
    ComparisonConstraints* this = (ComparisonConstraints*)self;
    this->gt = Py_XNewRef(gt);
    this->ge = Py_XNewRef(ge);
    this->lt = Py_XNewRef(lt);
    this->le = Py_XNewRef(le);
    return self;
}

static void
comparison_constraints_dealloc(ComparisonConstraints* self)
{
    Py_XDECREF(self->gt);
    Py_XDECREF(self->ge);
    Py_XDECREF(self->lt);
    Py_XDECREF(self->le);
    Py_TYPE(self)->tp_free(self);
}

static PyMemberDef comparison_constraints_members[] = {
    { "gt", T_OBJECT, offsetof(ComparisonConstraints, gt), READONLY },
    { "ge", T_OBJECT, offsetof(ComparisonConstraints, ge), READONLY },
    { "lt", T_OBJECT, offsetof(ComparisonConstraints, lt), READONLY },
    { "le", T_OBJECT, offsetof(ComparisonConstraints, le), READONLY },
    { NULL }
};

PyTypeObject ComparisonConstraintsType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_basicsize = sizeof(ComparisonConstraints),
    .tp_dealloc = (destructor)comparison_constraints_dealloc,
    .tp_name = "frost_typing.ComparisonConstraints",
    .tp_repr = (reprfunc)comparison_constraints_repr,
    .tp_members = comparison_constraints_members,
    .tp_new = comparison_constraints_new,
    .tp_flags = Py_TPFLAGS_DEFAULT,
};

PyObject*
ComparisonConstraints_Converter(TypeAdapter* validator,
                                ValidateContext* ctx,
                                PyObject* val)
{
    val = TypeAdapter_Conversion((TypeAdapter*)validator->cls, ctx, val);
    if (!val) {
        return NULL;
    }

    int r;
    ComparisonConstraints* con = (ComparisonConstraints*)validator->args;
    if (con->gt) {
        r = PyObject_RichCompareBool(val, con->gt, Py_GT);
        if (r != 1) {
            ValidationError_RaiseFormat("Input should be greater than %R",
                                        NULL,
                                        __greater_than,
                                        val,
                                        ctx->model,
                                        con->gt);
            goto error;
        }
    }
    if (con->ge) {
        r = PyObject_RichCompareBool(val, con->ge, Py_GE);
        if (r != 1) {
            ValidationError_RaiseFormat("Input should be greater "
                                        "than or equal to %R",
                                        NULL,
                                        __greater_than_equal,
                                        val,
                                        ctx->model,
                                        con->ge);
            goto error;
        }
    }
    if (con->lt) {
        r = PyObject_RichCompareBool(val, con->lt, Py_LT);
        if (r != 1) {
            ValidationError_RaiseFormat("Input should be less than %R",
                                        NULL,
                                        __less_than,
                                        val,
                                        ctx->model,
                                        con->lt);
            goto error;
        }
    }
    if (con->le) {
        r = PyObject_RichCompareBool(val, con->le, Py_LE);
        if (r != 1) {
            ValidationError_RaiseFormat("Input should be less "
                                        "than or equal to %R",
                                        NULL,
                                        __less_than_equal,
                                        val,
                                        ctx->model,
                                        con->le);
            goto error;
        }
    }
    return val;

error:
    Py_DECREF(val);
    return NULL;
}

int
comparison_constraint_setup(void)
{
    __greater_than = PyUnicode_FromString("greater_than");
    if (__greater_than == NULL) {
        return -1;
    }
    __greater_than_equal = PyUnicode_FromString("greater_than_equal");
    if (__greater_than_equal == NULL) {
        return -1;
    }
    __less_than = PyUnicode_FromString("less_than");
    if (__less_than == NULL) {
        return -1;
    }
    __less_than_equal = PyUnicode_FromString("less_than_equal");
    if (__less_than_equal == NULL) {
        return -1;
    }
    return PyType_Ready(&ComparisonConstraintsType);
}

void
comparison_constraint_free(void)
{
    Py_DECREF(__greater_than);
    Py_DECREF(__greater_than_equal);
    Py_DECREF(&ComparisonConstraintsType);
}