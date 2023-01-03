# c-in-py
Abusing globals and annotations to make a C-like syntax for declaring variables possible in Python.


# Currently, what this does is:
1. allow the syntax `type: name [= value];`, as in C
2. naively (in a way that could be broken easily if one desired) enforce type safety of variables

NOTE: 1 & 2 are only done for the global scope


# How to use:
At the top of your `__main__` file, or when you first start up Python in interactive mode, use the following:
```py
from __future__ import annotations
import c
```


# Planned features:

The following are features that I am actively working on implementing:
1. Declaring user-defined type variables
2. C-style function overloading/calling
3. C-style typecasting (will be implemented using chilaxan's fishhook)
4. pointers
#
The following are features that I want to add but am not currently working on (the reasons for not working on them vary, but the most common one is a lack of feasibility):
1. a preprocessor that runs when c.py is imported (for running files only, not interactive mode)
2. structs
3. unions
4. an emulation of the C standard library 
5. interoperability with my `asm` project (https://github.com/Resuscitating/asm)
