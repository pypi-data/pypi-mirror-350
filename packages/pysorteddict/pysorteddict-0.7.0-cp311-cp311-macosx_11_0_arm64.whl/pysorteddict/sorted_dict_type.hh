#ifndef SORTED_DICT_TYPE_HH_
#define SORTED_DICT_TYPE_HH_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <map>

#include "sorted_dict_key_compare.hh"

struct SortedDictType
{
public:
    PyObject_HEAD;

private:
    // Pointer to an object on the heap. Can't be the object itself, because
    // this container will be allocated a definite amount of space, which won't
    // allow the object to grow.
    std::map<PyObject*, PyObject*, SortedDictKeyCompare>* map;

    // The type of each key.
    PyTypeObject* key_type;

    // How many iterators hold a reference to this sorted dictionary.
    Py_ssize_t referring_iterators;

private:
    bool is_key_good(PyObject*);
    bool are_key_type_and_key_value_pair_good(PyObject*, PyObject*);
    bool is_modifiable(void);

public:
    void deinit(void);
    PyObject* repr(void);
    int contains(PyObject*);
    Py_ssize_t len(void);
    PyObject* getitem(PyObject*);
    int setitem(PyObject*, PyObject*);
    PyObject* clear(void);
    PyObject* copy(void);
    PyObject* items(void);
    PyObject* keys(PyTypeObject*);
    PyObject* values(void);
    PyObject* get_key_type(void);
    int init(PyObject*, PyObject*);
    static PyObject* New(PyTypeObject*, PyObject*, PyObject*);

    friend class SortedDictViewIterType;
    friend class SortedDictViewType;
};

#endif
