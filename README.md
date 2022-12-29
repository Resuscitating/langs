# c-in-py
Abusing globals and annotations to make a C-like syntax for declaring variables possible in Python.

# Currently, all that this does is:
1. allow the syntax `type: name [= value];`, as in C
2. naively (in a way that could be broken easily if one desired) enforce type safety of variables
NOTE: 1 & 2 are only done for the global scope
