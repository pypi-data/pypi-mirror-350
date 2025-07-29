# Doxystub

## What is it ?

This package generates stubs (`.pyi` file) for a python module created with Boost Python, leveraging *doxygen* documentation.

## Setting up

### Requirement

*doxystub* needs to know the mapping between C++ and Python classes. To that end, you should wrap your calls to `class_` as follow:

```c
// doxystub.h
#pragma once

#include <boost/python.hpp>

/**
 * This wrapper adds a __cxx_class__ method on the exposed class, allowing to retrieve the original
 * C++ type of the object from Python.
 */
template <class W, class X1 = boost::python::detail::not_specified, class X2 = boost::python::detail::not_specified,
          class X3 = boost::python::detail::not_specified, typename... Args>
boost::python::class_<W, X1, X2, X3> class__(Args... args)
{
  return boost::python::class_<W, X1, X2>(args...).def(
      "__cxx_class__", +[]() { return boost::core::demangle(typeid(W).name()); });
}
```

Simply keep the above snippet in a header file, and use `class__` instead of `class_` to expose your classes. 
This will provide the `__cxx_class__` method, used by *doxystub* to retrieve the mapping with C++ types.

### Usage

You can install *doxystub* using pip:

```
pip install doxystub
```

And then use it as follows:

```
doxystub -m my_module -d path/to/doxygen -o my_module.pyi
```

### In CMakeLists.txt

The following snippet can be used to trigger stubs generation at the end of your build

```cmake
add_custom_command(
    TARGET my_module POST_BUILD
    COMMAND doxystub
        --module my_module
        --doxygen_directory "${CMAKE_CURRENT_SOURCE_DIR}"
        --output "${CMAKE_BINARY_DIR}/${PYTHON_SITELIB}/my_module.pyi"
    WORKING_DIRECTORY "${CMAKE_BINARY_DIR}/${PYTHON_SITELIB}"
    COMMENT "Generating stubs..."
)
```

## Behaviour and remarks

### General process

*doxystub* will try, for each method, to find a method with corresponding name from *doxygen* parsing.

### Custom methods and variables

If you define custom methods and variables, that doesn't exist in *doxygen*, you can specify the arguments types and the docstring manually. *doxystub* will parse the Boost.Python docstring to try to extract information:

```c
class_<Something>("Something", init<>())
    .def("my_method", +[](Something &s, int j) { return 42; }, args("self", "j"), "A custom method")
    .add_property("my_property", +[]() { return 123; }, "My property [int]")
    ;
```

Note that type of non-doxygen properties is unknown. It can be overridden using `[type]` at the end of your description.