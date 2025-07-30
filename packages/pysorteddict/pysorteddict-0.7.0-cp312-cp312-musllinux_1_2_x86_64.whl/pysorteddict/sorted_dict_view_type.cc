#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <map>
#include <utility>

#include "sorted_dict_type.hh"
#include "sorted_dict_utils.hh"
#include "sorted_dict_view_type.hh"

void SortedDictViewIterType::deinit(void)
{
    --this->sd->referring_iterators;
    Py_DECREF(this->sd);
}

std::pair<PyObject*, PyObject*> SortedDictViewIterType::next(void)
{
    static std::pair<PyObject* const, PyObject*> sentinel = { nullptr, nullptr };
    return this->it == this->sd->map->end() ? sentinel : *this->it++;
}

PyObject* SortedDictViewIterType::New(PyTypeObject* type, SortedDictType* sd)
{
    PyObject* self = type->tp_alloc(type, 0);  // 🆕
    if (self == nullptr)
    {
        return nullptr;
    }

    SortedDictViewIterType* sdvi = reinterpret_cast<SortedDictViewIterType*>(self);
    sdvi->sd = sd;
    sdvi->it = sdvi->sd->map->begin();
    Py_INCREF(sdvi->sd);
    ++sdvi->sd->referring_iterators;
    return self;
}

void SortedDictViewType::deinit(void)
{
    Py_DECREF(this->sd);
}

PyObject* SortedDictViewType::repr(char const* name, PyObject* ob)
{
    PyObjectWrapper ob_list(PySequence_List(ob));  // 🆕
    if (ob_list == nullptr)
    {
        return nullptr;
    }
    return PyUnicode_FromFormat("%s(%R)", name, ob_list.get());
}

Py_ssize_t SortedDictViewType::len(void)
{
    return this->sd->map->size();
}

PyObject* SortedDictViewType::iter(PyTypeObject* type)
{
    return SortedDictViewIterType::New(type, this->sd);
}

PyObject* SortedDictViewType::New(PyTypeObject* type, SortedDictType* sd)
{
    PyObject* self = type->tp_alloc(type, 0);  // 🆕
    if (self == nullptr)
    {
        return nullptr;
    }

    SortedDictViewType* sdv = reinterpret_cast<SortedDictViewType*>(self);
    sdv->sd = sd;
    Py_INCREF(sdv->sd);
    return self;
}
