#include "utils_common.h"
#include "json/json.h"

#include "datetime.h"

#define INT_TO_CHAR(v) ((char)((v) + '0'))
#define _DateTime_HAS_TZINFO(o) (((_PyDateTime_BaseTZInfo*)o)->hastzinfo)
#define DateTime_DATE_GET_TZINFO(o)                                            \
    (_DateTime_HAS_TZINFO((o)) ? ((PyDateTime_DateTime*)(o))->tzinfo : NULL)

static void
write_buffer_date(WriteBuffer* buff, int year, int month, int day)
{
    unsigned char* s = buff->buffer + buff->size;
    for (int divisor = 1000; divisor > 0; divisor /= 10) {
        *s++ = INT_TO_CHAR(year / divisor % 10);
    }
    *s++ = '-';
    *s++ = INT_TO_CHAR(month / 10);
    *s++ = INT_TO_CHAR(month % 10);
    *s++ = '-';
    *s++ = INT_TO_CHAR(day / 10);
    *s++ = INT_TO_CHAR(day % 10);
    buff->size += 10;
}

static void
write_buffer_time(WriteBuffer* buff,
                  int hour,
                  int minute,
                  int second,
                  int microsecond)
{
    unsigned char* st = buff->buffer + buff->size;
    unsigned char* s = st;

    *s++ = INT_TO_CHAR(hour / 10);
    *s++ = INT_TO_CHAR(hour % 10);

    *s++ = ':';
    *s++ = INT_TO_CHAR(minute / 10);
    *s++ = INT_TO_CHAR(minute % 10);

    if (second || microsecond) {
        *s++ = ':';
        *s++ = INT_TO_CHAR(second / 10);
        *s++ = INT_TO_CHAR(second % 10);
    }
    if (microsecond) {
        *s++ = ':';
        for (int div = 100000; div > 0; div /= 10) {
            *s++ = INT_TO_CHAR(microsecond / div % 10);
        }
    }
    buff->size += s - st;
}

static PyObject*
tzinfo_get_offset(PyObject* tzinfo)
{
    PyObject* offset;
    offset = PyObject_CallMethod(tzinfo, "utcoffset", "O", Py_None);
    if (offset == Py_None || offset == NULL) {
        return offset;
    }

    if (PyDelta_Check(offset)) {
        PyDateTime_Delta* dt = (PyDateTime_Delta*)offset;
        if ((dt->days == -1 && dt->seconds == 0 && dt->microseconds < 1) ||
            dt->days < -1 || dt->days >= 1) {
            Py_DECREF(offset);
            return PyErr_Format(PyExc_ValueError,
                                "offset must be a timedelta"
                                " strictly between -timedelta(hour=24) and"
                                " timedelta(hour=24).");
        }
    } else {
        PyErr_Format(PyExc_TypeError,
                     "tzinfo.utcoffset() must return None or "
                     "timedelta, not '%.200s'",
                     Py_TYPE(offset)->tp_name);
        Py_DECREF(offset);
        return NULL;
    }
    return offset;
}

static int
format_tzoffset(WriteBuffer* buff, PyObject* tzinfo)
{
    PyObject* offset;
    offset = tzinfo_get_offset(tzinfo);
    if (offset == NULL) {
        return -1;
    }
    if (offset == Py_None) {
        return WriteBuffer_ConcatSize(buff, "+00:00", 5);
    }

    PyDateTime_Delta* dt = (PyDateTime_Delta*)offset;
    int hour, minute, second = dt->seconds;
    if (PyDateTime_DELTA_GET_DAYS(offset) < 0) {
        buff->buffer[buff->size++] = '-';
        second = 86400 - second;
    } else {
        buff->buffer[buff->size++] = '+';
        minute = second / 60;
    }
    minute = second / 60;
    hour = minute / 60;
    // second %= 60;
    minute %= 60;
    write_buffer_time(buff, hour, minute, 0, 0);
    Py_DECREF(offset);
    return 0;
}

int
_Date_AsJson(WriteBuffer* buff, PyObject* obj, UNUSED ConvParams* params)
{
    if (WriteBuffer_Resize(buff, buff->size + 12) < 0) {
        return -1;
    }
    buff->buffer[buff->size++] = '"';
    int year = PyDateTime_GET_YEAR(obj);
    unsigned char month = PyDateTime_GET_MONTH(obj);
    unsigned char day = PyDateTime_GET_DAY(obj);
    write_buffer_date(buff, year, month, day);
    buff->buffer[buff->size++] = '"';
    return 0;
}

int
_Time_AsJson(WriteBuffer* buff, PyObject* obj, UNUSED ConvParams* params)
{
    PyObject* tzinfo = DateTime_DATE_GET_TZINFO(obj);
    if (tzinfo && !PyTZInfo_Check(tzinfo)) {
        _RaiseInvalidType("time.tzinfo", "timezone", Py_TYPE(tzinfo)->tp_name);
        return -1;
    }
    if (WriteBuffer_Resize(buff, buff->size + (tzinfo ? 33 : 17)) < 0) {
        return -1;
    }
    buff->buffer[buff->size++] = '"';
    unsigned char hour = PyDateTime_TIME_GET_HOUR(obj);
    unsigned char minute = PyDateTime_TIME_GET_MINUTE(obj);
    unsigned char second = PyDateTime_TIME_GET_SECOND(obj);
    int microsecond = PyDateTime_TIME_GET_MICROSECOND(obj);
    write_buffer_time(buff, hour, minute, second, microsecond);
    if (tzinfo) {
        if (format_tzoffset(buff, tzinfo) < 0) {
            return -1;
        }
    }
    buff->buffer[buff->size++] = '"';
    return 0;
}

int
_Datetime_AsJson(WriteBuffer* buff, PyObject* obj, UNUSED ConvParams* params)
{
    PyObject* tzinfo = DateTime_DATE_GET_TZINFO(obj);
    if (tzinfo && !PyTZInfo_Check(tzinfo)) {
        _RaiseInvalidType(
          "datetime.tzinfo", "timezone", Py_TYPE(tzinfo)->tp_name);
        return -1;
    }
    if (WriteBuffer_Resize(buff, buff->size + (tzinfo ? 44 : 28)) < 0) {
        return -1;
    }

    buff->buffer[buff->size++] = '"';
    int year = PyDateTime_GET_YEAR(obj);
    unsigned char month = PyDateTime_GET_MONTH(obj);
    unsigned char day = PyDateTime_GET_DAY(obj);
    write_buffer_date(buff, year, month, day);

    buff->buffer[buff->size++] = 'T';

    int hour = PyDateTime_DATE_GET_HOUR(obj);
    int minute = PyDateTime_DATE_GET_MINUTE(obj);
    int second = PyDateTime_DATE_GET_SECOND(obj);
    int microsecond = PyDateTime_DATE_GET_MICROSECOND(obj);
    write_buffer_time(buff, hour, minute, second, microsecond);
    if (tzinfo) {
        if (format_tzoffset(buff, tzinfo) < 0) {
            return -1;
        }
    }
    buff->buffer[buff->size++] = '"';
    return 0;
}

int
json_date_time_setup(void)
{
    PyDateTime_IMPORT;
    return PyDateTimeAPI ? 0 : -1;
}

void
json_date_time_free(void)
{
}