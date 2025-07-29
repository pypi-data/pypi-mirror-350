#include "convector.h"
#include "data_model.h"
#include "field.h"
#include "meta_model.h"
#include "utils_common.h"
#include "json/json.h"

static int
meta_model_as_json_call_override(WriteBuffer* buff,
                                 PyObject* obj,
                                 ConvParams* params,
                                 PyObject* as_json)
{
    if (!as_json) {
        PyErr_Format(PyExc_TypeError,
                     "The '__as_json__' method is not defined for '%.100s'",
                     Py_TYPE(obj)->tp_name);
        return -1;
    }

    if (_Encode_Enter(buff) < 0) {
        return -1;
    }

    PyObject* json = PyObject_CallOneArg(as_json, obj);
    if (!json) {
        return -1;
    }
    int r = _PyObject_AsJson(buff, json, params);
    _Encode_Leave(buff);
    Py_DECREF(json);
    return r;
}

static int
meta_model_as_json(WriteBuffer* buff,
                   PyObject* obj,
                   ConvParams* params,
                   PyObject* include,
                   PyObject* exclude)
{
    PyTypeObject* tp = Py_TYPE(obj);
    PyObject* as_json = _CAST_META(tp)->__as_json__;
    if (as_json != DataModelType.__as_json__) {
        return meta_model_as_json_call_override(buff, obj, params, as_json);
    }

    if (_Encode_Enter(buff) < 0) {
        return -1;
    }

    PyObject *val, **slots;
    Py_ssize_t cnt = 0;

    slots = DATA_MODEL_GET_SLOTS(obj);
    BUFFER_CONCAT_CHAR(buff, '{');
    SchemaForeach(schema, tp, slots++)
    {
        if (!IS_FIELD_JSON(schema->field->flags)) {
            continue;
        }

        if (exclude && exclude != Py_None) {
            int r = PySet_Contains(exclude, schema->name);
            if (r < 0) {
                return -1;
            }
            if (r) {
                continue;
            }
        }

        if (include && include != Py_None) {
            int r = PySet_Contains(include, schema->name);
            if (r < 0) {
                return -1;
            }
            if (!r) {
                continue;
            }
        }

        val = *slots;
        if (!val) {
            int r = _Schema_GetValue(schema, obj, slots, params->exclude_unset);
            if (r < 0) {
                return -1;
            } else if (!r) {
                continue;
            }
            val = *slots;
        }

        if (params->exclude_none && val == Py_None) {
            continue;
        }

        if (cnt) {
            BUFFER_CONCAT_CHAR(buff, ',');
        }

        cnt++;
        if (params->by_alias &&
            IF_FIELD_CHECK(schema->field, FIELD_SERIALIZATION_ALIAS)) {
            PyObject* name = Field_GET_SERIALIZATION_ALIAS(schema->field);
            if (_Unicode_AsJson(buff, name, params) < 0) {
                return -1;
            }
        } else if (_Unicode_FastAsJson(buff, schema->name) < 0) {
            return -1;
        }

        BUFFER_CONCAT_CHAR(buff, ':');
        PyObject* serializer = Field_GET_SERIALIZER(schema->field);
        if (!serializer) {
            if (_PyObject_AsJson(buff, val, params) < 0) {
                return -1;
            }
            continue;
        }

        PyObject* const args[2] = { obj, val };
        PyObject* tmp = PyObject_Vectorcall(serializer, args, 2, NULL);
        if (tmp == NULL) {
            return -1;
        }

        int r = _PyObject_AsJson(buff, tmp, params);
        Py_DECREF(tmp);
        if (r < 0) {
            return -1;
        }
    }

    _Encode_Leave(buff);
    return WriteBuffer_ConcatChar(buff, '}');
}

int
_MetaModel_AsJson(WriteBuffer* buff, PyObject* obj, ConvParams* params)
{
    return meta_model_as_json(buff, obj, params, NULL, NULL);
}

PyObject*
_MetaModel_AsJsonCall(PyObject* obj, PyObject* kwargs)
{
    char* kwlist[] = { "include",       "exclude",      "by_alias",
                       "exclude_unset", "exclude_none", NULL };
    ConvParams params = ConvParams_Create(NULL);
    PyObject *include = NULL, *exclude = NULL;
    if (kwargs && !PyArg_ParseTupleAndKeywords(VoidTuple,
                                               kwargs,
                                               "|OOppp:as_json",
                                               kwlist,
                                               &include,
                                               &exclude,
                                               &params.by_alias,
                                               &params.exclude_unset,
                                               &params.exclude_none)) {
        return NULL;
    }

    if (Convector_ValidateInclue(include, exclude) < 0) {
        return NULL;
    }

    WriteBuffer buff = WriteBuffer_Create(512);
    if (!buff.buffer) {
        return PyErr_NoMemory();
    }

    if (meta_model_as_json(&buff, obj, &params, include, exclude) < 0) {
        WriteBuffer_Free(&buff);
        return NULL;
    }

    PyObject* res =
      PyBytes_FromStringAndSize((const char*)buff.buffer, buff.size);
    WriteBuffer_Free(&buff);
    return res;
}