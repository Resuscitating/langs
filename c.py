#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import builtins as __builtins__
import sys
import ctypes

sentinal = object()
last_vname = ""

typeinfo = {}
valstorage = sentinal
cstyle_vars = {}

# this is what will replace the globals of __main__
class __globals_overload__(dict):
    __slots__ = ()
    
    def __getitem__(self, vname):
        global typeinfo, valstorage, last_vname
        __getitem__ = {}.__class__.__getitem__
        if vname is last_vname and valstorage is not sentinal:
            if last_vname in typeinfo:
                type_candidate = typeinfo[last_vname]
                if type(valstorage) is type_candidate:
                   cstyle_vars[last_vname] = valstorage
                else:
                    err = False
                    try:
                        casted_value = type_candidate(valstorage)
                        if type(casted_value) is type_candidate:
                            cstyle_vars[last_vname] = casted_value
                        else:
                            raise TypeError
                    except:
                        err = True
                    if err:
                        valstorage = sentinal
                        raise TypeError(f"value '{valstorage}' cannot be cast into type '{type_candidate}'")
            else:
                valstorage = sentinal
                raise TypeError(f"cannot create variable '{last_vname}' without type information")
            valstorage = sentinal

        try:
            return cstyle_vars[vname]
        except:
            try:
                return __getitem__(self, vname)
            except:
                try:
                    return __builtins__.__getattribute__(vname)
                except:
                    pass
        raise NameError(f"{vname} is not defined")

    def __setitem__(self, vname, value):
        global typeinfo, valstorage, last_vname

        # make import not assign this module into __main__
        if type(value) is type(__builtins__) and value.__name__ == "c":
            return
        
        if valstorage is not sentinal:
            if last_vname in typeinfo:
                type_candidate = typeinfo[last_vname]
                if type(valstorage) is type_candidate:
                   cstyle_vars[last_vname] = valstorage
                else:
                    err = False
                    try:
                        casted_value = type_candidate(valstorage)
                        if type(casted_value) is type_candidate:
                            cstyle_vars[last_vname] = casted_value
                        else:
                            raise TypeError
                    except:
                        err = True
                    if err:
                        last_vname = vname
                        valstorage = value
                        raise TypeError(f"value '{valstorage}' cannot be cast into type '{type_candidate}'")
            else:
                last_vname = vname
                valstorage = value
                raise TypeError(f"cannot create variable '{last_vname}' without type information")
        last_vname = vname
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

    def __setitem__(self, vtype, vname):
        global typeinfo, valstorage
        if vname not in typeinfo:

            # find the type
            type_candidate = None
            try:
                if type(cstyle_vars[vtype]) is type:
                    type_candidate = cstyle_vars[vtype]
            except:
                try:
                    if type(__builtins__.__dict__[vtype]) is type:
                        type_candidate = __builtins__.__dict__[vtype]
                except:
                    pass
            if type_candidate is None:
                valstorage = sentinal
                raise TypeError(f"variable declaration for '{vtype}: {vname}' is not a valid. '{vtype}' is not a type.")

            # if the value has been stored, set the value
            if valstorage is not sentinal:
                if type(valstorage) is type_candidate:
                    cstyle_vars[vname] = valstorage
                else:
                    err = False
                    try:
                        casted_value = type_candidate(valstorage)
                        if type(casted_value) is type_candidate:
                            cstyle_vars[vname] = casted_value
                        else:
                            raise TypeError
                    except:
                        err = True
                    if err:
                        raise TypeError(f"value '{(valstorage, valstorage:=sentinal)[0]}' cannot be cast into type '{type_candidate}'")
            valstorage = sentinal
            typeinfo[vname] = type_candidate

        else:
            raise Exception("something has gone horrifically wrong- tell the author of this module so they can fix this bug!")


# hijack __annotations__
__import__("__main__").__annotations__ = __annotations_overload__()


