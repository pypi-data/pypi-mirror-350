#include "field.h"
#include "limits.h"
#include "meta_valid_model.h"
#include "valid_model.h"
#include "validator/validator.h"
#include "validator/validator_uuid.h"

static PyObject*
converter_bytes(UNUSED TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    if (ctx->flags & FIELD_STRICT) {
        return NULL;
    }
    if (PyUnicode_Check(val)) {
        return PyUnicode_AsUTF8String(val);
    }
    if (PyByteArray_Check(val)) {
        return PyBytes_FromObject(val);
    }
    return NULL;
}

static PyObject*
converter_bytearray(UNUSED TypeAdapter* self,
                    ValidateContext* ctx,
                    PyObject* val)
{
    if (ctx->flags & FIELD_STRICT) {
        return NULL;
    }

    if (PyUnicode_Check(val)) {
        val = PyUnicode_AsUTF8String(val);
        if (val == NULL) {
            return NULL;
        }
        PyObject* res = PyByteArray_FromObject(val);
        Py_DECREF(val);
        return res;
    }
    if (PyBytes_Check(val)) {
        return PyByteArray_FromObject(val);
    }
    return NULL;
}

static PyObject*
converter_primitive(TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    if (ctx->flags & FIELD_STRICT) {
        return NULL;
    }
    PyObject* res = PyObject_CallOneArg(self->cls, val);
    if (!res) {
        ValidationError_ExceptionHandling(ctx->model, val);
    }
    return res;
}

static PyObject*
converter_frost_validate(TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    PyObject* args[3] = { NULL, val, (PyObject*)ctx->ctx };
    PyObject* res = PyObject_Vectorcall(
      self->args, args + 1, 2 | PY_VECTORCALL_ARGUMENTS_OFFSET, NULL);
    if (!res) {
        ValidationError_ExceptionHandling(ctx->model, val);
    }
    return res;
}

static PyObject*
converter_frost_validate_valid_model(TypeAdapter* self,
                                     ValidateContext* ctx,
                                     PyObject* val)
{
    return _ValidModel_FrostValidate((PyTypeObject*)self->cls, val, ctx->ctx);
}

static PyObject*
converter_frost_validate_ctx_manager(TypeAdapter* self,
                                     ValidateContext* ctx,
                                     PyObject* val)
{
    return _ContextManager_FrostValidate(
      (ContextManager*)self->cls, val, ctx->ctx);
}

static PyObject*
converter_none(UNUSED TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    if (ctx->flags & FIELD_STRICT) {
        return NULL;
    }
    return EqString(val, "null", 4) == 1 ? Py_NewRef(Py_None) : NULL;
}

static PyObject*
converter_long(UNUSED TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    if (ctx->flags & FIELD_STRICT) {
        return NULL;
    }

    if (PyUnicode_Check(val)) {
        return PyLong_FromUnicodeObject(val, 10);
    }

    if (PyBytes_Check(val) || PyByteArray_Check(val)) {
        const char* s;
        if (PyBytes_Check(val)) {
            s = PyBytes_AS_STRING(val);
        } else {
            s = PyByteArray_AS_STRING(val);
        }

        char* end = NULL;
        PyObject* res = PyLong_FromString(s, &end, 10);
        if (!end || (res && end == s + Py_SIZE(val))) {
            return res;
        }
        Py_XDECREF(res);
        return NULL;
    }

    PyNumberMethods* m = Py_TYPE(val)->tp_as_number;
    if (m && m->nb_int) {
        PyObject* res = m->nb_int(val);
        if (!res || PyLong_CheckExact(res)) {
            return res;
        }
        Py_DECREF(res);
        return NULL;
    }

    if (PyUnicode_Check(val) || PyBytes_Check(val) || PyByteArray_Check(val)) {
        return PyFloat_FromString(val);
    }
    return NULL;
}

static PyObject*
converter_float_nested(UNUSED TypeAdapter* self,
                       ValidateContext* ctx,
                       PyObject* val)
{
    if (Py_IS_TYPE(val, &PyFloat_Type)) {
        return Py_NewRef(val);
    }

    if (ctx->flags & FIELD_STRICT) {
        return NULL;
    }

    if (PyUnicode_CheckExact(val)) {
        return PyFloat_FromString(val);
    }

    PyNumberMethods* m = Py_TYPE(val)->tp_as_number;
    if (m && m->nb_float) {
        PyObject* res = m->nb_float(val);
        if (!res || PyFloat_CheckExact(res)) {
            return res;
        }
        Py_DECREF(res);
    }
    return NULL;
}

static inline PyObject*
float_check_allow_inf_nan(ValidateContext* ctx, PyObject* val)
{
    if (!(ctx->flags & FIELD_ALLOW_INF_NAN)) {
        double d = PyFloat_AS_DOUBLE(val);
        if (!isfinite(d)) {
            return NULL;
        }
    }
    return Py_NewRef(val);
}

static PyObject*
converter_float(TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    PyObject* res = converter_float_nested(self, ctx, val);
    if (!res) {
        return NULL;
    }

    val = float_check_allow_inf_nan(ctx, res);
    Py_DECREF(res);
    return val;
}

static PyObject*
converter_enum(TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    return ctx->flags & FIELD_STRICT
             ? NULL
             : Py_XNewRef(PyDict_GetItemWithError(self->args, val));
}

static inline TypeAdapter*
validator_create_enum(PyObject* hint)
{
    PyObject* args = PyTyping_Get__value2member_map_(hint);
    if (!args) {
        return NULL;
    }
    TypeAdapter* res = TypeAdapter_Create(
      hint,
      args,
      NULL,
      TypeAdapter_Base_Repr,
      converter_enum,
      PyObject_HasAttr(hint, __instancecheck__) ? Inspector_IsType
                                                : Inspector_IsInstance);
    Py_DECREF(args);
    return res;
}

static inline TypeAdapter*
validator_create_frost_validate(PyObject* hint)
{
    PyObject* args = PyObject_GetAttr(hint, __frost_validate__);
    if (!args) {
        return NULL;
    }

    if (!PyCallable_Check(args)) {
        _RaiseInvalidType(
          "__frost_validate__", "callable", Py_TYPE(args)->tp_name);
        Py_DECREF(args);
        return NULL;
    }

    TypeAdapter* res = TypeAdapter_Create(hint,
                                          args,
                                          NULL,
                                          TypeAdapter_Base_Repr,
                                          converter_frost_validate,
                                          Inspector_No);
    Py_DECREF(args);
    return res;
}

TypeAdapter*
TypeAdapter_Create_Primitive(PyObject* hint)
{
    if (((PyTypeObject*)hint) == &PyUnicode_Type) {
        return TypeAdapter_Create_Str(hint);
    } else if (((PyTypeObject*)hint) == &PyBool_Type) {
        return TypeAdapter_Create_Bool(hint);
    } else if (((PyTypeObject*)hint) == PyNone_Type) {
        return TypeAdapter_Create(hint,
                                  NULL,
                                  NULL,
                                  TypeAdapter_Base_Repr,
                                  converter_none,
                                  Inspector_IsType);
    } else if (ContextManager_Check(hint)) {
        return TypeAdapter_Create(hint,
                                  NULL,
                                  NULL,
                                  TypeAdapter_Base_Repr,
                                  converter_frost_validate_ctx_manager,
                                  Inspector_No);
    } else if (PyType_Check(hint) && MetaValid_IS_SUBCLASS(hint) &&
               ValidModelType.__frost_validate__ ==
                 _CAST(MetaValidModel*, hint)->__frost_validate__) {
        return TypeAdapter_Create(hint,
                                  NULL,
                                  NULL,
                                  TypeAdapter_Base_Repr,
                                  converter_frost_validate_valid_model,
                                  Inspector_No);
    } else if (PyObject_HasAttr(hint, __frost_validate__)) {
        return validator_create_frost_validate(hint);
    } else if (PyType_Check(hint)) {
        if (PyType_IsSubtype((PyTypeObject*)hint, (PyTypeObject*)PyEnumType)) {
            return validator_create_enum(hint);
        }
        if (PyType_IsSubtype((PyTypeObject*)hint, PyUuidType)) {
            return TypeAdapter_Create_Uuid(hint);
        }
    }

    Converter conv;
    PyTypeObject* type = (PyTypeObject*)hint;
    Inspector insp =
      PyType_Check(hint) && PyObject_HasAttr(hint, __instancecheck__)
        ? Inspector_IsType
        : Inspector_IsInstance;

    if (type == &PyBytes_Type) {
        conv = converter_bytes;
    } else if (type == &PyByteArray_Type) {
        conv = converter_bytearray;
    } else if (type == &PyFloat_Type) {
        conv = converter_float;
        insp = Inspector_No;
    } else if (type == &PyLong_Type) {
        conv = converter_long;
    } else {
        conv = converter_primitive;
    }

    return TypeAdapter_Create(
      hint, NULL, NULL, TypeAdapter_Base_Repr, conv, insp);
}

int
validator_primitive_setup(void)
{
    if (validator_uuid_setup() < 0) {
        return -1;
    }
    return date_time_setup();
}

void
validator_primitive_free(void)
{
    validator_uuid_free();
    date_time_free();
}