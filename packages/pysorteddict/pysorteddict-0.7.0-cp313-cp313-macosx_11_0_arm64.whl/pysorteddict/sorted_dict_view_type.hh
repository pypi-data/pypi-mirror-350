#ifndef SORTED_DICT_VIEW_TYPE_HH_
#define SORTED_DICT_VIEW_TYPE_HH_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <map>
#include <utility>

#include "sorted_dict_key_compare.hh"
#include "sorted_dict_type.hh"

struct SortedDictViewIterType
{
public:
    PyObject_HEAD;

protected:
    SortedDictType* sd;
    std::map<PyObject*, PyObject*, SortedDictKeyCompare>::iterator it;

public:
    void deinit(void);
    std::pair<PyObject*, PyObject*> next(void);
    static PyObject* New(PyTypeObject*, SortedDictType*);
};

struct SortedDictViewType
{
public:
    PyObject_HEAD;

protected:
    SortedDictType* sd;

public:
    void deinit(void);
    static PyObject* repr(char const* name, PyObject*);
    Py_ssize_t len(void);
    PyObject* iter(PyTypeObject*);
    static PyObject* New(PyTypeObject*, SortedDictType*);
};

#endif
