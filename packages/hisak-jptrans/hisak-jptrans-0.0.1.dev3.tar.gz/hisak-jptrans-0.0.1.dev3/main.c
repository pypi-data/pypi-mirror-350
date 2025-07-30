#define PY_SSIZE_T_CLEAN
#include <Python.h>

#define INIT_MODULE(m) PyInit_##m

PyObject* getVersion();
PyObject* buildInfo();
PyObject* supportedCodecs();
PyObject* setReplacement();
PyObject* encode(PyObject*, PyObject*);
PyObject* decode(PyObject*, PyObject*);

int PyArg_ParseTupleAndKeywords_SetReplacement(PyObject* args, PyObject* kwargs,
                                               char** codec, char* data) {
  static char* kwlist[] = {"codec", "char", NULL};
  return PyArg_ParseTupleAndKeywords(args, kwargs, "sc", kwlist, codec, data);
}

int PyArg_ParseTupleAndKeywords_Encode(PyObject* args, PyObject* kwargs,
                                       char** codec, Py_buffer* data,
                                       int* replacement) {
  static char* kwlist[] = {"codec", "data", "replacement", NULL};
  return PyArg_ParseTupleAndKeywords(args, kwargs, "ss*|p", kwlist, codec, data,
                                     replacement);
}

int PyArg_ParseTupleAndKeywords_Decode(PyObject* args, PyObject* kwargs,
                                       char** codec, Py_buffer* data) {
  static char* kwlist[] = {"codec", "data", NULL};
  return PyArg_ParseTupleAndKeywords(args, kwargs, "sy*", kwlist, codec, data);
}

static PyMethodDef jpTransMethods[] = {
    {"build_info", (PyCFunction)buildInfo, METH_NOARGS,
     PyDoc_STR("build information")},
    {"supported_codecs", (PyCFunction)supportedCodecs, METH_NOARGS,
     PyDoc_STR("supported japanese codecs")},
    {"set_replacement", (PyCFunction)setReplacement,
     METH_VARARGS | METH_KEYWORDS, PyDoc_STR("set replacement character")},
    {"encode", (PyCFunction)encode, METH_VARARGS | METH_KEYWORDS,
     PyDoc_STR("japanese codec encode")},
    {"decode", (PyCFunction)decode, METH_VARARGS | METH_KEYWORDS,
     PyDoc_STR("japanese codec decode")},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef jpTransModule = {PyModuleDef_HEAD_INIT, "_jptrans",
                                           PyDoc_STR("japanese transformer"),
                                           -1, jpTransMethods};

PyMODINIT_FUNC INIT_MODULE(_jptrans)(void) {
  PyObject *mod, *obj;

  mod = PyModule_Create(&jpTransModule);
  if (mod == NULL) {
    return NULL;
  }

  obj = getVersion();
  if (PyModule_AddObject(mod, "__version__", obj) < 0) {
    Py_XDECREF(obj);
    Py_DECREF(mod);
    return NULL;
  }

  obj =
      Py_BuildValue("[ssssss]", "__version__", "build_info", "supported_codecs",
                    "set_replacement", "encode", "decode");
  if (PyModule_AddObject(mod, "__all__", obj) < 0) {
    Py_XDECREF(obj);
    Py_DECREF(mod);
    return NULL;
  }

  return mod;
}