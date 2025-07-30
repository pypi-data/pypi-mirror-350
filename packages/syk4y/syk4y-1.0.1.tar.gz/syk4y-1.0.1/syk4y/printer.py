from typing import Any

try:
    import torch # type: ignore[import]
except ImportError:
    torch = None

try:
    import numpy as np # type: ignore[import]
except ImportError:
    np = None

def inspect(var: Any, indent: int = 0, prefix: str = "Variable") -> None:
    """
    Recursively prints the structure of a variable, including tensors, lists, tuples, or dicts.
    Works without requiring torch or numpy.

    Args:
        var: The variable to analyze (tensor, list, tuple, dict, or nested combinations)
        indent: Current indentation level for formatting (default: 0)
        prefix: Label for the current variable (default: "Variable")
    """
    indent_str = "  " * indent

    # Handle None
    if var is None:
        print(f"{indent_str}{prefix}: None")
        return

    # Get type name
    type_name = type(var).__name__

    # Handle PyTorch Tensor
    if torch is not None and isinstance(var, torch.Tensor):
        shape = tuple(var.shape)
        dtype = str(var.dtype)
        print(f"{indent_str}{prefix}: Tensor(shape={shape}, dtype={dtype})")

    # Handle NumPy Array
    elif np is not None and isinstance(var, np.ndarray):
        shape = tuple(var.shape)
        dtype = str(var.dtype)
        print(f"{indent_str}{prefix}: NumPy Array(shape={shape}, dtype={dtype})")

    # Handle List
    elif isinstance(var, list):
        print(f"{indent_str}{prefix}: List(length={len(var)})")
        for i, item in enumerate(var):
            inspect(item, indent + 1, f"[{i}]")

    # Handle Tuple
    elif isinstance(var, tuple):
        print(f"{indent_str}{prefix}: Tuple(length={len(var)})")
        for i, item in enumerate(var):
            inspect(item, indent + 1, f"[{i}]")

    # Handle Dictionary
    elif isinstance(var, dict):
        print(f"{indent_str}{prefix}: Dict(keys={len(var)})")
        for key, value in var.items():
            inspect(value, indent + 1, f"[{key}]")

    # Handle other types (scalars, strings, etc.) or unknown tensor/array types
    else:
        # If it's an unknown tensor-like object, try to get shape and dtype
        shape = getattr(var, "shape", None)
        dtype = getattr(var, "dtype", None)
        if shape is not None and dtype is not None:
            print(f"{indent_str}{prefix}: {type_name}(shape={tuple(shape)}, dtype={str(dtype)})")
        else:
            print(f"{indent_str}{prefix}: {type_name}({var})")