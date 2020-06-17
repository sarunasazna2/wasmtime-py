from . import _ffi as ffi
from ctypes import *
from wasmtime import Store, GlobalType, Val, WasmtimeError


class Global:
    def __init__(self, store, ty, val):
        if not isinstance(store, Store):
            raise TypeError("expected a Store")
        if not isinstance(ty, GlobalType):
            raise TypeError("expected a GlobalType")
        val = Val.__convert__(ty.content, val)
        ptr = POINTER(ffi.wasm_global_t)()
        error = ffi.wasmtime_global_new(
            store.__ptr__,
            ty.__ptr__,
            byref(val.__raw__),
            byref(ptr))
        if error:
            raise WasmtimeError.__from_ptr__(error)
        self.__ptr__ = ptr
        self.__owner__ = None

    @classmethod
    def __from_ptr__(cls, ptr, owner):
        ty = cls.__new__(cls)
        if not isinstance(ptr, POINTER(ffi.wasm_global_t)):
            raise TypeError("wrong pointer type")
        ty.__ptr__ = ptr
        ty.__owner__ = owner
        return ty

    @property
    def type(self):
        """
        Gets the type of this global as a `GlobalType`
        """

        ptr = ffi.wasm_global_type(self.__ptr__)
        return GlobalType.__from_ptr__(ptr, None)

    @property
    def value(self):
        """
        Gets the current value of this global

        Returns a native python type
        """
        raw = ffi.wasm_val_t()
        ffi.wasm_global_get(self.__ptr__, byref(raw))
        return Val(raw).value

    @value.setter
    def value(self, val):
        """
        Sets the value of this global to a new value
        """
        val = Val.__convert__(self.type.content, val)
        error = ffi.wasmtime_global_set(self.__ptr__, byref(val.__raw__))
        if error:
            raise WasmtimeError.__from_ptr__(error)

    def _as_extern(self):
        return ffi.wasm_global_as_extern(self.__ptr__)

    def __del__(self):
        if hasattr(self, '__owner__') and self.__owner__ is None:
            ffi.wasm_global_delete(self.__ptr__)
