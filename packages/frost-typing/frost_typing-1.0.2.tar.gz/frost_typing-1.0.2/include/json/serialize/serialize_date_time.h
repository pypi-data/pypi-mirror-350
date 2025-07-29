typedef struct WriteBuffer WriteBuffer;

extern int
_Date_AsJson(WriteBuffer*, PyObject*, ConvParams* params);
extern int
_Datetime_AsJson(WriteBuffer*, PyObject*, ConvParams* params);
extern int
_Time_AsJson(WriteBuffer*, PyObject*, ConvParams* params);
extern int
json_date_time_setup(void);
extern void
json_date_time_free(void);