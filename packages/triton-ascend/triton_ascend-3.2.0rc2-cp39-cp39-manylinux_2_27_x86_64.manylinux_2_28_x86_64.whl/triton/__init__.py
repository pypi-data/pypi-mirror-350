
import sys
from .triton_patch.language import _utils as ascend_utils
sys.modules['triton.language._utils'] = ascend_utils
from .triton_patch.compiler import compiler as ascend_compiler
sys.modules['triton.compiler.compiler'] = ascend_compiler
from .triton_patch.compiler import code_generator as ascend_code_generator
sys.modules['triton.compiler.code_generator'] = ascend_code_generator
from .triton_patch.compiler import errors as ascend_errors
sys.modules['triton.compiler.errors'] = ascend_errors
from .triton_patch.runtime import autotuner as ascend_autotuner
sys.modules['triton.runtime.autotuner'] = ascend_autotuner
from .triton_patch import testing as ascend_testing
sys.modules['triton.testing'] = ascend_testing


"""isort:skip_file"""
__version__ = '3.2.0'

# ---------------------------------------
# Note: import order is significant here.

# submodules
from .runtime import (
    autotune,
    Config,
    heuristics,
    JITFunction,
    KernelInterface,
    reinterpret,
    TensorWrapper,
    OutOfResources,
    InterpreterError,
    MockTensor,
)
from .runtime.jit import jit
from .compiler import compile, CompilationError
from .errors import TritonError

from . import language
from . import testing
from . import tools

__all__ = [
    "autotune",
    "cdiv",
    "CompilationError",
    "compile",
    "Config",
    "heuristics",
    "impl",
    "InterpreterError",
    "jit",
    "JITFunction",
    "KernelInterface",
    "language",
    "MockTensor",
    "next_power_of_2",
    "ops",
    "OutOfResources",
    "reinterpret",
    "runtime",
    "TensorWrapper",
    "TritonError",
    "testing",
    "tools",
]

# -------------------------------------
# misc. utilities that  don't fit well
# into any specific module
# -------------------------------------


def cdiv(x: int, y: int):
    return (x + y - 1) // y


def next_power_of_2(n: int):
    """Return the smallest power of 2 greater than or equal to n"""
    n -= 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    n |= n >> 32
    n += 1
    return n


from .triton_patch.language.core import dot, gather, insert, subview
from .triton_patch.language.standard import flip, sigmoid, softmax
from .triton_patch.language.math import umulhi, exp, exp2, log, log2, cos, sin, sqrt, sqrt_rn, rsqrt, div_rn, erf, tanh, floor, ceil
from . import language

language.dot = dot
language.flip = flip
language.sigmoid = sigmoid
language.softmax = softmax
language.gather = gather
language.insert = insert
language.subview = subview

# from .triton_patch.language.core import dtype, pointer_type, block_type, function_type
# language.core.dtype = dtype
# language.core.pointer_type = pointer_type
# language.core.block_type = block_type
# language.core.function_type = function_type

from .triton_patch.language.semantic import arange, floordiv, atom_red_typechecking_impl,         atomic_max, atomic_min, maximum, minimum
language.semantic.arange = arange
language.semantic.floordiv = floordiv
language.semantic.atom_red_typechecking_impl = atom_red_typechecking_impl
language.semantic.atomic_max = atomic_max
language.semantic.atomic_min = atomic_min
language.semantic.maximum = maximum
language.semantic.minimum = minimum

language.umulhi = umulhi
language.exp = exp
language.exp2 = exp2
language.log = log
language.log2 = log2
language.cos = cos
language.sin = sin
language.sqrt = sqrt
language.sqrt_rn = sqrt_rn
language.rsqrt = rsqrt
language.div_rn = div_rn
language.erf = erf
language.tanh = tanh
language.floor = floor
language.ceil = ceil
language.math.umulhi = umulhi
language.math.exp = exp
language.math.exp2 = exp2
language.math.log = log
language.math.log2 = log2
language.math.cos = cos
language.math.sin = sin
language.math.sqrt = sqrt
language.math.sqrt_rn = sqrt_rn
language.math.rsqrt = rsqrt
language.math.div_rn = div_rn
language.math.erf = erf
language.math.tanh = tanh
language.math.floor = floor
language.math.ceil = ceil
