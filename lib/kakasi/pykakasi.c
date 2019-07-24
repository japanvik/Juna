#include <Python.h>
#include "libkakasi.h"

static PyObject *pykakasi_Error;

static PyObject *pykakasi_init(PyObject *self, PyObject *args)
{
	PyObject *list;
	int i, list_sz, ret;
	char **argv_p;

	if(!PyArg_ParseTuple(args, "O!", &PyList_Type, &list)){
		return NULL;
	}

	list_sz = PyList_Size(list);
	argv_p = (char **)calloc(list_sz + 1, sizeof(char *));
	argv_p[0] = "kakasi";
	for(i = 0; i < list_sz; i++){
		argv_p[i+1] = PyString_AsString(PyList_GetItem(list, i));
	}
	kakasi_close_kanwadict();
	ret = kakasi_getopt_argv(list_sz + 1, argv_p);
	free(argv_p);

	return Py_BuildValue("i", ret);
}

static PyObject *pykakasi_execute(PyObject *self, PyObject *args)
{
	PyObject *ret_val;
	char *input, *output;

	if(!PyArg_ParseTuple(args, "s", &input)){
		return NULL;
	}

	output = kakasi_do(input);

	ret_val = Py_BuildValue("s", output);
	kakasi_free(output);

	return ret_val;
}

static PyMethodDef pykakasi_Methods[] = {
	{"init", pykakasi_init, METH_VARARGS},
	{"execute", pykakasi_execute, METH_VARARGS},
	{NULL, NULL}
};

PyMODINIT_FUNC initpykakasi(void)
{
	PyObject *m, *d;

	m = Py_InitModule("pykakasi", pykakasi_Methods);
	d = PyModule_GetDict(m);
	pykakasi_Error = PyErr_NewException("pykakasi.error", NULL, NULL);
	PyDict_SetItemString(d, "error", pykakasi_Error);
}

