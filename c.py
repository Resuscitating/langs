#! /usr/bin/env python3

import builtins as __builtins__
import sys
import ctypes


sentinal = object()

typeinfo = {}
valstorage = sentinal
cstyle_vars = {}

# this is what will replace the globals of __main__
class __globals_overload__(dict):

    def __getitem__(self, item):
        __getitem__ = {}.__class__.__getitem__
        try:
            return __getitem__(cstyle_vars, item)
        except:
            try:
                return __getitem__(self, item)
            except:
                try:
                    return __builtins__.__getattribute__(item)
                except:
                    pass
        raise NameError(f"{item} is not defined")

    def __setitem__(self, item, value):
        global typeinfo, valstorage
        __setitem__ = {}.__class__.__setitem__
        # make import not assign this module into __main__
        if type(value) is type(__builtins__) and value.__name__ == "c":
            return;
        if item in typeinfo:
            if type(value) is typeinfo[item]:
                return __setitem__(cstyle_vars, item, value)
            else:
                try:
                    return __setitem__(cstyle_vars, item, typeinfo[item](value))
                except:
                    pass
            raise TypeError(f"variable '{item}' of type {typeinfo[item]} cannot be set to {value} (of type {type(value)})")
        else:
            valstorage = value


# find the __main__ frame
frame = sys._getframe()
while True:
    if "__name__" in frame.f_globals:
        if frame.f_globals["__name__"] == "__main__":
            break
    frame = frame.f_back

# hijack the globals object
ctypes.py_object.from_address(id(frame.f_globals) + 8).value = __globals_overload__


# this is what will replace the __annotations__ of __main__
class __annotations_overload__(dict):
    __slots__ = ()

    def __setitem__(self, item, value):
        global typeinfo, valstorage
        if value not in typeinfo:
            if item in __builtins__.__dict__ and type(__builtins__.__dict__[item]) is type:
                typeinfo[value] = __builtins__.__dict__[item]
                if valstorage != sentinal:
                    if type(valstorage) is typeinfo[value]:
                        cstyle_vars.__setitem__(value, valstorage)
                    else:
                        try:
                            cstyle_vars.__setitem__(value, typeinfo[value](valstorage))
                        except:
                            raise TypeError()
                valstorage = sentinal
            else:
                # user defined type??
                pass
        else:
            raise TypeError()


# hijack __annotations__
__import__("__main__").__annotations__ = __annotations_overload__()
