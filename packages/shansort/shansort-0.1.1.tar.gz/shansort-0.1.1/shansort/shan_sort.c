#include <Python.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define RADIX 256  // 8 bits per pass
#define BITS_PER_PASS 8

// Stable counting sort for one radix pass (8 bits)
static void counting_sort_pass(uint64_t* arr, uint64_t* temp, size_t n, int pass) {
    size_t count[RADIX] = {0};

    for (size_t i = 0; i < n; i++) {
        uint8_t digit = (arr[i] >> (pass * BITS_PER_PASS)) & 0xFF;
        count[digit]++;
    }

    size_t offsets[RADIX];
    offsets[0] = 0;
    for (int i = 1; i < RADIX; i++) {
        offsets[i] = offsets[i - 1] + count[i - 1];
    }

    for (size_t i = 0; i < n; i++) {
        uint8_t digit = (arr[i] >> (pass * BITS_PER_PASS)) & 0xFF;
        temp[offsets[digit]++] = arr[i];
    }

    memcpy(arr, temp, n * sizeof(uint64_t));
}

static void shan_sort_internal(uint64_t* arr, size_t n, int bits) {
    uint64_t* temp = (uint64_t*) malloc(n * sizeof(uint64_t));
    if (!temp) return;

    int passes = (bits + BITS_PER_PASS - 1) / BITS_PER_PASS;

    for (int pass = 0; pass < passes; pass++) {
        counting_sort_pass(arr, temp, n, pass);
    }

    free(temp);
}

static PyObject* py_shan_sort(PyObject* self, PyObject* args) {
    PyObject* input_list;
    if (!PyArg_ParseTuple(args, "O", &input_list)) {
        return NULL;
    }
    if (!PyList_Check(input_list)) {
        PyErr_SetString(PyExc_TypeError, "Input must be a list");
        return NULL;
    }

    Py_ssize_t n = PyList_Size(input_list);
    if (n == 0) {
        return PyList_New(0);
    }

    int64_t min_val = INT64_MAX;
    int64_t max_val = INT64_MIN;

    for (Py_ssize_t i = 0; i < n; i++) {
        PyObject* item = PyList_GetItem(input_list, i);
        int64_t val = PyLong_AsLongLong(item);
        if (val == -1 && PyErr_Occurred()) {
            return NULL;
        }
        if (val < min_val) min_val = val;
        if (val > max_val) max_val = val;
    }

    uint64_t offset = (min_val < 0) ? (uint64_t)(-min_val) : 0;

    uint64_t* arr = (uint64_t*) malloc(n * sizeof(uint64_t));
    if (!arr) {
        PyErr_SetString(PyExc_MemoryError, "Could not allocate memory");
        return NULL;
    }

    for (Py_ssize_t i = 0; i < n; i++) {
        PyObject* item = PyList_GetItem(input_list, i);
        int64_t val = PyLong_AsLongLong(item);
        arr[i] = (uint64_t)(val + offset);
    }

    uint64_t max_adjusted = (uint64_t)(max_val + offset);
    int bits = 0;
    while (max_adjusted > 0) {
        bits++;
        max_adjusted >>= 1;
    }
    if (bits == 0) bits = 1;

    shan_sort_internal(arr, n, bits);

    PyObject* out_list = PyList_New(n);
    if (!out_list) {
        free(arr);
        return NULL;
    }
    for (Py_ssize_t i = 0; i < n; i++) {
        int64_t val = (int64_t)(arr[i] - offset);
        PyObject* val_obj = PyLong_FromLongLong(val);
        PyList_SetItem(out_list, i, val_obj);
    }

    free(arr);
    return out_list;
}

static PyMethodDef ShanSortMethods[] = {
    {"shan_sort", py_shan_sort, METH_VARARGS, "Stable ShanSort radix sort for 64-bit integers."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef shansortmodule = {
    PyModuleDef_HEAD_INIT,
    "shan_sort",
    "Stable ShanSort radix sort module implemented in C.",
    -1,
    ShanSortMethods
};

PyMODINIT_FUNC PyInit_shan_sort(void) {
    return PyModule_Create(&shansortmodule);
}
