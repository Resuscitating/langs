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
    __slots__ = ()
    
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
            return

        # if the variable has already been declared, assign to it
        if item in typeinfo:
            if type(value) is typeinfo[item]:
                return __setitem__(cstyle_vars, item, value)
            else:
                err = False
                try:
                    casted_value = typeinfo[item](value)
                    if type(casted_value) is typeinfo[item]:
                        cstyle_vars.__setitem__(item, casted_value)
                    else:
                        raise TypeError
                except:
                    err = True
                if err:
                    raise TypeError(f"value '{value}' cannot be cast into type '{typeinfo[item]}'")

        # store the value so that when __annotations_overload__.__setitem__
        # gets called, it can use the value to set the variable
        else:
            valstorage = value


def get_main_frame():
    frame = sys._getframe()
    while True:
        if "__name__" in frame.f_globals and frame.f_globals["__name__"] == "__main__":
            break
        frame = frame.f_back
    return frame

# hijack the globals object
ctypes.py_object.from_address(id(get_main_frame().f_globals) + 8).value = __globals_overload__


# this is what will replace the __annotations__ of __main__
class __annotations_overload__(dict):
    __slots__ = ()

    def __setitem__(self, item, value):
        global typeinfo, valstorage
        if value not in typeinfo:

            # find the type
            type_candidate = None
            if item in cstyle_vars:
                if type(cstyle_vars[item]) is type:
                    type_candidate = cstyle_vars[item]
                    print("user defined")
            if type_candidate is None and item in __builtins__.__dict__:
                if type(__builtins__.__dict__[item]) is type:
                    type_candidate = __builtins__.__dict__[item]
                    print("builtin")
            if type_candidate is None:
                TypeError(f"variable declaration for '{item}: {value}' is not a valid. '{item}' is not a type.")

            # if the value has been stored, set the value
            if valstorage is not sentinal:
                if type(valstorage) is type_candidate:
                    cstyle_vars[value] = valstorage
                else:
                    err = False
                    try:
                        casted_value = type_candidate(valstorage)
                        if type(casted_value) is type_candidate:
                            cstyle_vars[value] = casted_value
                        else:
                            raise TypeError
                    except:
                        err = True
                    if err:
                        raise TypeError(f"value '{valstorage}' cannot be cast into type '{type_candidate}'")
                valstorage = sentinal
            typeinfo[value] = type_candidate

        else:
            raise Exception("something has gone horrifically wrong- tell the author of this module so they can fix this bug!")


# hijack __annotations__
__import__("__main__").__annotations__ = __annotations_overload__()

