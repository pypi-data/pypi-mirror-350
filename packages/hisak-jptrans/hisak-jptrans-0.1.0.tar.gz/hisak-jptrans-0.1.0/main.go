package main

// #cgo pkg-config: python3
// #define PY_SSIZE_T_CLEAN
// #include <Python.h>
// int PyArg_ParseTupleAndKeywords_SetReplacement(PyObject*, PyObject*, char**, char*);
// int PyArg_ParseTupleAndKeywords_Encode(PyObject*, PyObject*, char**, Py_buffer*, int*);
// int PyArg_ParseTupleAndKeywords_Decode(PyObject*, PyObject*, char**, Py_buffer*);
import "C"

import (
	"bytes"
	"fmt"
	"io"
	"maps"
	"runtime/debug"
	"slices"
	"strings"
	"unsafe"

	"gitlab.com/HiSakDev/go-encoding/japanese"
	"golang.org/x/text/encoding"
	"golang.org/x/text/transform"
)

var (
	info    *debug.BuildInfo
	codecs  map[string]encoding.Encoding
	version string
)

func main() {}

func init() {
	info, _ = debug.ReadBuildInfo()
	codecs = make(map[string]encoding.Encoding)
	for _, enc := range japanese.All {
		if v, ok := enc.(fmt.Stringer); ok {
			if name := codecName(v.String()); name != "" {
				codecs[name] = enc
			}
		}
	}
}

func codecName(name string) string {
	return strings.ReplaceAll(strings.ReplaceAll(strings.ToLower(name), " ", ""), "-", "")
}

//export getVersion
func getVersion() *C.PyObject {
	d := C.CString(version)
	defer C.free(unsafe.Pointer(d))
	return C.PyUnicode_FromStringAndSize(d, C.Py_ssize_t(len(version)))
}

//export buildInfo
func buildInfo(_ *C.PyObject) *C.PyObject {
	var v string
	if info != nil {
		v = info.String()
	}
	d := C.CString(v)
	defer C.free(unsafe.Pointer(d))
	return C.PyUnicode_FromStringAndSize(d, C.Py_ssize_t(len(v)))
}

//export supportedCodecs
func supportedCodecs() *C.PyObject {
	keys := slices.Sorted(maps.Keys(codecs))
	d := C.CString(strings.Join(keys, "\n"))
	defer C.free(unsafe.Pointer(d))
	v := C.PyUnicode_FromString(d)
	defer C.Py_DecRef(v)
	return C.PyUnicode_Splitlines(v, C.int(0))
}

//export setReplacement
func setReplacement(_, args, kwargs *C.PyObject) *C.PyObject {
	var codec *C.char
	var data C.char
	if C.PyArg_ParseTupleAndKeywords_SetReplacement(args, kwargs, &codec, &data) == 0 {
		return nil
	}
	name := C.GoString(codec)
	if trans, ok := codecs[codecName(name)]; ok {
		japanese.SetReplacement(trans, byte(data))
		C.Py_IncRef(C.Py_None)
		return C.Py_None
	}
	msg := C.CString(fmt.Sprintf("unexpected codec: %v", name))
	defer C.free(unsafe.Pointer(msg))
	C.PyErr_SetString(C.PyExc_ValueError, msg)
	return nil
}

//export encode
func encode(_, args, kwargs *C.PyObject) *C.PyObject {
	var codec *C.char
	var data C.Py_buffer
	var replacement C.int
	defer C.PyBuffer_Release(&data)
	if C.PyArg_ParseTupleAndKeywords_Encode(args, kwargs, &codec, &data, &replacement) == 0 {
		return nil
	}

	name := C.GoString(codec)
	if trans, ok := codecs[codecName(name)]; ok {
		dst := new(bytes.Buffer)
		src := bytes.NewReader(C.GoBytes(data.buf, (C.int)(data.len)))
		enc := trans.NewEncoder()
		if replacement > 0 {
			enc = encoding.ReplaceUnsupported(enc)
		}
		t := transform.NewWriter(dst, enc)
		if _, err := io.Copy(t, src); err != nil {
			msg := C.CString(err.Error())
			defer C.free(unsafe.Pointer(msg))
			C.PyErr_SetString(C.PyExc_ValueError, msg)
			return nil
		}
		size := dst.Len()
		buf := C.CBytes(dst.Bytes())
		defer C.free(buf)
		return C.PyBytes_FromStringAndSize((*C.char)(buf), C.Py_ssize_t(size))
	}
	msg := C.CString(fmt.Sprintf("unexpected codec: %v", name))
	defer C.free(unsafe.Pointer(msg))
	C.PyErr_SetString(C.PyExc_ValueError, msg)
	return nil
}

//export decode
func decode(_, args, kwargs *C.PyObject) *C.PyObject {
	var codec *C.char
	var data C.Py_buffer
	defer C.PyBuffer_Release(&data)
	if C.PyArg_ParseTupleAndKeywords_Decode(args, kwargs, &codec, &data) == 0 {
		return nil
	}

	name := C.GoString(codec)
	if trans, ok := codecs[codecName(name)]; ok {
		dst := new(bytes.Buffer)
		src := bytes.NewReader(C.GoBytes(data.buf, (C.int)(data.len)))
		t := transform.NewReader(src, trans.NewDecoder())
		if _, err := io.Copy(dst, t); err != nil {
			msg := C.CString(err.Error())
			defer C.free(unsafe.Pointer(msg))
			C.PyErr_SetString(C.PyExc_ValueError, msg)
			return nil
		}
		size := dst.Len()
		buf := C.CBytes(dst.Bytes())
		defer C.free(buf)
		return C.PyUnicode_FromStringAndSize((*C.char)(buf), C.Py_ssize_t(size))
	}

	msg := C.CString(fmt.Sprintf("unexpected codec: %v", name))
	defer C.free(unsafe.Pointer(msg))
	C.PyErr_SetString(C.PyExc_ValueError, msg)
	return nil
}
