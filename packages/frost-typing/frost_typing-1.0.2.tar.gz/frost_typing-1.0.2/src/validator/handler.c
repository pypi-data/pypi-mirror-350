#include "validator/validator.h"

static PyTypeObject HandlerType;

static void
handler_dealloc(Handler* self)
{
    Py_DECREF(self->ctx);
    Py_DECREF(self->model);
    Py_DECREF(self->cur_obj);
    Py_DECREF(self->type_adapter);
    Py_TYPE(self)->tp_free(self);
}

PyObject*
Handler_Create(ValidateContext* ctx, TypeAdapter* type_adapter)
{
    Handler* self = (Handler*)HandlerType.tp_alloc(&HandlerType, 0);
    if (!self) {
        return NULL;
    }

    self->flags = ctx->flags;
    self->model = Py_NewRef(ctx->model);
    self->cur_obj = Py_NewRef(ctx->cur_obj);
    self->ctx = (ContextManager*)Py_NewRef(ctx->ctx);
    self->type_adapter = (TypeAdapter*)Py_NewRef(type_adapter);
    return (PyObject*)self;
}

static PyObject*
handler_call(Handler* self, PyObject* args, PyObject* kwargs)
{
    if (!_PyArg_NoKeywords("Handler.__call__", kwargs)) {
        return NULL;
    }

    PyObject* val = Parse_OneArgs("Handler.__call__", args);
    if (!val) {
        return NULL;
    }

    ValidateContext ctx = ValidateContext_Create(
      self->ctx, self->cur_obj, self->model, self->flags);
    return TypeAdapter_Conversion(self->type_adapter, &ctx, val);
}

static PyTypeObject HandlerType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_dealloc = (destructor)handler_dealloc,
    .tp_call = (ternaryfunc)handler_call,
    .tp_name = "frost_typing.Handler",
    .tp_basicsize = sizeof(Handler),
};

int
handler_setup(void)
{
    return PyType_Ready(&HandlerType);
}

void
handler_free(void)
{
}