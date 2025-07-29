#include "validator/validator.h"
#include "field.h"
#include "stddef.h"
#include "validator/discriminator.h"
#include "weakref_cache.h"
#include "json/json.h"

static TypeAdapter *any_type_adapter, *none_type_adapter,
  *self_type_adapter = NULL;
static ContextManager* default_ctx;
static PyObject* _cash_validator;
PyObject* __frost_validate__;

static void
validator_dealloc(TypeAdapter* self)
{
    PyObject_ClearWeakRefs((PyObject*)self);
    Py_DECREF(self->cls);
    Py_XDECREF(self->args);
    Py_XDECREF(self->ob_str);
    Py_XDECREF(self->err_msg);
    Py_TYPE(self)->tp_free(self);
}

static PyObject*
type_adapter_vector_call(UNUSED PyObject* callable,
                         PyObject* const* args,
                         size_t nargsf,
                         PyObject* kwn)
{
    PyObject* hint = _VectorCall_GetOneArg("TypeAdapter", args, nargsf, kwn);
    return hint ? (PyObject*)ParseHint(hint, NULL) : NULL;
}

static PyObject*
validator_str(TypeAdapter* self)
{
    if (self->ob_str == NULL) {
        self->ob_str = PyObject_Repr((PyObject*)self);
        if (self->ob_str == NULL) {
            return NULL;
        }
    }
    return Py_NewRef(self->ob_str);
}

PyObject*
TypeAdapter_Base_Repr(TypeAdapter* self)
{
    if (self->ob_str) {
        return Py_NewRef(self->ob_str);
    }

    if (PyType_Check(self->cls)) {
        const char* name = _CAST(PyTypeObject*, self->cls)->tp_name;
        self->ob_str = PyUnicode_FromString(name);
    } else {
        self->ob_str = PyObject_Repr(self->cls);
    }
    return Py_XNewRef(self->ob_str);
}

static PyObject*
validator_repr(TypeAdapter* self)
{
    int r = Py_ReprEnter((PyObject*)self);
    if (r != 0) {
        if (r < 0) {
            return NULL;
        }
        return PyUnicode_FromFormat("%.100s(...)", Py_TYPE(self)->tp_name);
    }
    PyObject* res = self->ob_repr(self);
    Py_ReprLeave((PyObject*)self);
    return res;
}

static PyObject*
validator_call_conversion(TypeAdapter* self, PyObject* obj)
{
    ValidateContext vctx =
      ValidateContext_Create(default_ctx, self, self, FIELD_ALLOW_INF_NAN);
    PyObject* res = TypeAdapter_Conversion(self, &vctx, obj);
    if (!res) {
        ValidationError_Raise(NULL, self, obj, (PyObject*)self);
    }
    return res;
}

TypeAdapter*
TypeAdapter_Create(PyObject* cls,
                   PyObject* args,
                   PyObject* ob_str,
                   TypeAdapterRepr ob_repr,
                   Converter conv,
                   Inspector inspector)
{
    if (!ob_str && !ob_repr) {
        PyErr_BadArgument();
        return NULL;
    }

    if (!ob_repr) {
        ob_repr = TypeAdapter_Base_Repr;
    }

    TypeAdapter* self;
    self = (TypeAdapter*)TypeAdapterType.tp_alloc(&TypeAdapterType, 0);
    self->conv = conv;
    self->ob_repr = ob_repr;
    self->cls = Py_NewRef(cls);
    self->inspector = inspector;
    self->args = Py_XNewRef(args);
    self->ob_str = Py_XNewRef(ob_str);
    self->err_msg = PyUnicode_FromFormat("Input should be a valid %R", self);
    if (self->err_msg) {
        return self;
    }

    Py_DECREF(self);
    return NULL;
}

inline PyObject*
TypeAdapter_Conversion(TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    int r = self->inspector(self, val);
    if (r == 1) {
        return Py_NewRef(val);
    } else if (r < 0) {
        return NULL;
    }
    return self->conv(self, ctx, val);
}

static PyObject*
validator_subclasscheck(TypeAdapter* self, PyObject* obj)
{
    int r = PyObject_IsSubclass(obj, self->cls);
    if (r < 0) {
        return NULL;
    }
    return Py_NewRef(r ? Py_True : Py_False);
}

static PyObject*
validator_instancecheck(TypeAdapter* self, PyObject* obj)
{
    int r = self->inspector(self, obj);
    if (r < 0) {
        return NULL;
    }
    return Py_NewRef(r ? Py_True : Py_False);
}

static PyObject*
validator_from_json(TypeAdapter* self, PyObject* obj)
{
    PyObject* val = JsonParse(obj);
    if (!val) {
        ValidationError_RaiseInvalidJson(obj, (PyObject*)self);
        return NULL;
    }

    PyObject* res = validator_call_conversion(self, val);
    Py_DECREF(val);
    return res;
}

static PyMethodDef type_adapter_methods[] = {
    { "from_json", (PyCFunction)validator_from_json, METH_O, NULL },
    { "validate", (PyCFunction)validator_call_conversion, METH_O, NULL },
    { "__instancecheck__", (PyCFunction)validator_instancecheck, METH_O, NULL },
    { "__subclasscheck__", (PyCFunction)validator_subclasscheck, METH_O, NULL },
    { 0 }
};

PyTypeObject TypeAdapterType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_vectorcall = (vectorcallfunc)type_adapter_vector_call,
    .tp_weaklistoffset = offsetof(TypeAdapter, tp_weaklist),
    .tp_dealloc = (destructor)validator_dealloc,
    .tp_repr = (reprfunc)validator_repr,
    .tp_name = "frost_typing.TypeAdapter",
    .tp_basicsize = sizeof(TypeAdapter),
    .tp_str = (reprfunc)validator_str,
    .tp_methods = type_adapter_methods,
};

PyObject*
Not_Converter(UNUSED TypeAdapter* self,
              UNUSED ValidateContext* ctx,
              UNUSED PyObject* val)
{
    return NULL;
}

static PyObject*
converter_deferred_parse(TypeAdapter* self, ValidateContext* ctx, PyObject* val)
{
    PyObject* hint = PyTyping_Eval(self->cls, (PyTypeObject*)self->args);
    if (!hint) {
        return NULL;
    }

    TypeAdapter* new_validator = ParseHint(hint, self->args);
    Py_DECREF(hint);
    if (new_validator == NULL) {
        return NULL;
    }
    Py_DECREF(self->cls);
    Py_XDECREF(self->args);
    Py_XDECREF(self->ob_str);

    self->cls = Py_XNewRef(new_validator->cls);
    self->args = Py_XNewRef(new_validator->args);
    self->ob_str = Py_XNewRef(new_validator->ob_str);
    self->inspector = new_validator->inspector;
    self->ob_repr = new_validator->ob_repr;
    self->conv = new_validator->conv;
    Py_DECREF(new_validator);
    return TypeAdapter_Conversion(self, ctx, val);
}

int
Inspector_IsInstance(TypeAdapter* self, PyObject* val)
{
    return PyObject_IsInstance(val, self->cls);
}

int
Inspector_IsInstanceTypeAdapter(TypeAdapter* self, PyObject* val)
{
    if (PyTuple_Check(self->cls)) {
        Py_ssize_t size = PyTuple_GET_SIZE(self->cls);
        TypeAdapter** validators = (TypeAdapter**)TUPLE_ITEMS(self->cls);
        for (Py_ssize_t i = 0; i != size; i++) {
            self = validators[i];
            int r = self->inspector(self, val);
            if (r) {
                return r;
            }
        }
        return 0;
    }
    self = _CAST(TypeAdapter*, self->cls);
    return self->inspector(self, val);
}

int
Inspector_IsSubclass(TypeAdapter* self, PyObject* val)
{
    if (!PyType_Check(val)) {
        return 0;
    }
    return PyObject_IsSubclass(val, self->cls);
}

int
Inspector_Any(UNUSED TypeAdapter* self, UNUSED PyObject* val)
{
    return 1;
}

int
Inspector_No(UNUSED TypeAdapter* self, UNUSED PyObject* val)
{
    return 0;
}

int
Inspector_IsType(TypeAdapter* self, PyObject* val)
{
    return Py_IS_TYPE(val, (PyTypeObject*)self->cls);
}

PyObject*
TypeAdapter_MapParseHintTuple(PyObject* args, PyObject* tp)
{
    PyObject* res = PyTuple_New(PyTuple_GET_SIZE(args));
    if (!res) {
        return NULL;
    }

    for (Py_ssize_t i = 0; i < PyTuple_GET_SIZE(args); i++) {
        TypeAdapter* val = ParseHint(PyTuple_GET_ITEM(args, i), tp);
        if (!val) {
            Py_DECREF(res);
            return NULL;
        }
        PyTuple_SET_ITEM(res, i, (PyObject*)val);
    }
    return res;
}

static inline TypeAdapter*
type_adapter_create_required(PyObject* hint, PyObject* tp)
{
    PyObject* type_args = PyTyping_Get_Args(hint);
    if (type_args == NULL) {
        return NULL;
    }
    if (PyTuple_GET_SIZE(type_args) != 1) {
        PyErr_Format(PyExc_ValueError,
                     "%.100S accepts only a single type. Got %.100S.",
                     hint,
                     type_args);
        Py_DECREF(type_args);
        return NULL;
    }
    TypeAdapter* res = ParseHint(PyTuple_GET_ITEM(type_args, 0), tp);
    Py_DECREF(type_args);
    return res;
}

static inline TypeAdapter*
type_adapter_create_annotated(PyObject* hint, PyObject* tp, PyObject* origin)
{
    TypeAdapter* res = ParseHint(origin, tp);
    if (!res) {
        return NULL;
    }

    PyObject* metadata = PyTyping_Get_Metadata(hint);
    if (!metadata) {
        Py_DECREF(res);
        return NULL;
    }

    for (Py_ssize_t i = 0; i < PyTuple_GET_SIZE(metadata); i++) {
        PyObject* tmp = PyTuple_GET_ITEM(metadata, i);
        if (Discriminator_Check(tmp)) {
            TypeAdapter* r =
              TypeAdapter_Create_Discriminator(res, (Discriminator*)tmp, tp);
            Py_DECREF(res);
            if (!r) {
                goto error;
            }
            res = r;
        } else if (IsConstraints(tmp)) {
            TypeAdapter* r = TypeAdapter_Create_Constraints(res, tmp);
            Py_DECREF(res);
            if (!r) {
                goto error;
            }
            res = r;
        }
    }
    Py_DECREF(metadata);
    return res;

error:
    Py_DECREF(metadata);
    return NULL;
}

static TypeAdapter*
_parse_hint(PyObject* hint, PyObject* tp)
{
    if (PyTyping_Is_TypedDict(hint)) {
        return TypeAdapter_Create_TypedDict(hint, tp);
    } else if (PyType_Check(hint)) {
        return TypeAdapter_Create_Primitive(hint);
    } else if (Py_IS_TYPE(hint, (PyTypeObject*)PyTypeVar)) {
        return TypeAdapter_Create_TypeVar(hint);
    }

    PyObject* origin = PyTyping_Get_Origin(hint);
    if (origin) {
        TypeAdapter* res = (TypeAdapter*)Py_None;
        if (origin == PyUnion) {
            res = TypeAdapter_Create_Union(hint, tp);
        } else if (origin == PyLiteral) {
            res = TypeAdapter_Create_Literal(hint);
        } else if (origin == (PyObject*)&PyType_Type) {
            res = TypeAdapter_Create_UnionType(hint, tp);
        } else if (origin == PyRequired || origin == PyNotRequired) {
            res = type_adapter_create_required(hint, tp);
        } else if (Py_IS_TYPE(hint, (PyTypeObject*)Py_AnnotatedAlias)) {
            res = type_adapter_create_annotated(hint, tp, origin);
        } else if (origin == AbcCallable) {
            Py_INCREF(TypeAdapter_AbcCallable);
            res = TypeAdapter_AbcCallable;
        } else if (origin == AbcHashable) {
            res = (TypeAdapter*)Py_NewRef(TypeAdapter_AbcHashable);
        } else if (origin == AbcByteString) {
            res = (TypeAdapter*)Py_NewRef(TypeAdapter_AbcByteString);
        } else if (Py_IS_TYPE(hint, (PyTypeObject*)PyGenericAlias) ||
                   Py_IS_TYPE(hint, (PyTypeObject*)_GenericAlias)) {
            res = TypeAdapter_CreateCollection(hint, tp, origin);
        } else if (origin == AbcIterable) {
            res = _TypeAdapter_CreateIterable(AbcIterable, tp, NULL);
        } else if (origin == AbcGenerator) {
            res = _TypeAdapter_CreateIterable(AbcGenerator, tp, NULL);
        } else if (origin == AbcSequence) {
            res = _TypeAdapter_CreateSequence(tp, NULL);
        }

        Py_DECREF(origin);
        if (!res || res != (TypeAdapter*)Py_None) {
            return res;
        }
    }

    PyErr_Format(FrostUserError, "Unsupported annotation: '%S'", hint);
    return NULL;
}

TypeAdapter*
ParseHint(PyObject* hint, PyObject* meta)
{
    if (DateTime_Is_TimeType((PyTypeObject*)hint)) {
        return (TypeAdapter*)Py_NewRef(TypeAdapterTime);
    } else if (DateTime_Is_DateType((PyTypeObject*)hint)) {
        return (TypeAdapter*)Py_NewRef(TypeAdapterDate);
    } else if (DateTime_Is_DateTimeType((PyTypeObject*)hint)) {
        return (TypeAdapter*)Py_NewRef(TypeAdapterDateTime);
    } else if (hint == Py_None || Py_TYPE(hint) == PyNone_Type) {
        return (TypeAdapter*)Py_NewRef(none_type_adapter);
    } else if (hint == PyAny) {
        return (TypeAdapter*)Py_NewRef(any_type_adapter);
    } else if (hint == PySelf) {
        return (TypeAdapter*)Py_XNewRef(self_type_adapter);
    } else if (ContextManager_Check(hint)) {
        return TypeAdapter_Create_Primitive(hint);
    } else if (PyUnicode_Check(hint)) {
        return TypeAdapter_Create(hint,
                                  meta,
                                  hint,
                                  TypeAdapter_Base_Repr,
                                  converter_deferred_parse,
                                  Inspector_No);
    } else if (Py_IS_TYPE(hint, (PyTypeObject*)PyForwardRef)) {
        PyObject* tmp =
          PyTyping_Evaluate_Forward_Ref(hint, (PyTypeObject*)meta);
        if (!tmp) {
            return NULL;
        }
        TypeAdapter* res = ParseHint(tmp, meta);
        Py_DECREF(tmp);
        return res;
    }

    TypeAdapter* res =
      (TypeAdapter*)WeakrefCache_GetItem(_cash_validator, hint);
    if (res) {
        return (TypeAdapter*)Py_NewRef(res);
    }

    res = _parse_hint(hint, meta);
    if (res) {
        if (WeakrefCache_SetItem(_cash_validator, hint, (PyObject*)res) < 0) {
            Py_DECREF(res);
            return NULL;
        }
    }
    return res;
}

TypeAdapter*
ParseHintAndName(PyObject* hint, PyObject* type, PyObject* name)
{
    return TypeAdapter_Create_FieldValidator(hint, type, name);
}

int
validator_setup(void)
{
    if (PyType_Ready(&TypeAdapterType) < 0) {
        return -1;
    }

    if (validator_primitive_setup() < 0 || validator_collection_setup() < 0 ||
        validator_literal_setup() < 0 || handler_setup() < 0 ||
        abc_setup() < 0) {
        return -1;
    }

    CREATE_VAR_INTERN_STING(__frost_validate__);

    _cash_validator = PyObject_CallNoArgs((PyObject*)&WeakrefCacheType);
    if (!_cash_validator) {
        return -1;
    }

    any_type_adapter = TypeAdapter_Create(
      PyAny, NULL, NULL, TypeAdapter_Base_Repr, Not_Converter, Inspector_Any);
    if (!any_type_adapter) {
        return -1;
    }

    none_type_adapter = TypeAdapter_Create_Primitive((PyObject*)PyNone_Type);
    if (!none_type_adapter) {
        return -1;
    }

    default_ctx = ContextManager_CREATE(&TypeAdapterType);
    return default_ctx ? 0 : -1;
}

void
validator_free(void)
{
    validator_primitive_free();
    validator_collection_free();
    validator_literal_free();
    handler_free();
    abc_free();

    Py_DECREF(__frost_validate__);
    Py_XDECREF(self_type_adapter);
    Py_DECREF(none_type_adapter);
    Py_DECREF(any_type_adapter);
    Py_DECREF(_cash_validator);
    Py_DECREF(default_ctx);
}
