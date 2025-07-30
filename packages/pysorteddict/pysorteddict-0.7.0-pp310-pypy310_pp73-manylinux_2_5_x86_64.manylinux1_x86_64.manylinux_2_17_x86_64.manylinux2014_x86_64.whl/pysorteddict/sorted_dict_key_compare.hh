#ifndef SORTED_DICT_KEY_COMPARE_HH_
#define SORTED_DICT_KEY_COMPARE_HH_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

/**
 * C++-style comparison implementation for Python objects.
 */
struct SortedDictKeyCompare
{
    bool operator()(PyObject* a, PyObject* b) const
    {
        // There must exist a total order on the set of possible keys. (Else,
        // this comparison may error out.) Hence, only instances of the type
        // of the first key inserted may be used as keys. (Instances of types
        // derived from that type are not allowed, because comparisons between
        // them can be customised to error out. Check the code to see how this
        // is enforced.) With these precautions, this comparison should always
        // work.
        return PyObject_RichCompareBool(a, b, Py_LT) == 1;
    }
};

#endif
