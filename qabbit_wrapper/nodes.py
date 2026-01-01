"""
ComfyUI nodes module - exports all standard ComfyUI nodes.

This module automatically initializes ComfyUI and exports all nodes from ComfyUI's nodes.py.
"""

from .core import init_comfy, ensure_initialized

# Auto-initialize if not already initialized
try:
    ensure_initialized()
except RuntimeError:
    # Try to auto-initialize
    try:
        init_comfy()
    except Exception as e:
        import warnings
        warnings.warn(
            f"Failed to auto-initialize ComfyUI: {e}. "
            "Please call qabbit_wrapper.init_comfy() manually."
        )

# Import all nodes from ComfyUI
try:
    from nodes import *
except ImportError as e:
    raise ImportError(
        f"Failed to import ComfyUI nodes. Make sure ComfyUI is properly initialized. "
        f"Error: {e}"
    )

