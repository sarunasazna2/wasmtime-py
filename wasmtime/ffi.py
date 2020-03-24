from ctypes import *

dll = cdll.LoadLibrary("../wasmtime/target/release/libwasmtime.so")

WASM_I32 = c_uint8(0)
WASM_I64 = c_uint8(1)
WASM_F32 = c_uint8(2)
WASM_F64 = c_uint8(3)

WASM_CONST = c_uint8(0)
WASM_VAR = c_uint8(1)

class wasm_valtype_t(Structure):
    pass
P_wasm_valtype_t = POINTER(wasm_valtype_t)

class wasm_globaltype_t(Structure):
    pass
P_wasm_globaltype_t = POINTER(wasm_globaltype_t)

class wasm_functype_t(Structure):
    pass
P_wasm_functype_t = POINTER(wasm_functype_t)

class wasm_tabletype_t(Structure):
    pass
P_wasm_tabletype_t = POINTER(wasm_tabletype_t)

class wasm_memorytype_t(Structure):
    pass
P_wasm_memorytype_t = POINTER(wasm_memorytype_t)

class wasm_externtype_t(Structure):
    pass
P_wasm_externtype_t = POINTER(wasm_externtype_t)

class wasm_valtype_vec_t(Structure):
    _fields_ = [("size", c_size_t), ("data", POINTER(P_wasm_valtype_t))]

class wasm_limits_t(Structure):
    _fields_ = [("min", c_uint32), ("max", c_uint32)]