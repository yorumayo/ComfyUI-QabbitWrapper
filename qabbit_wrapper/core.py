"""
Core initialization module for ComfyUI wrapper.
Handles path setup, fake server creation, and basic ComfyUI initialization.
"""

import sys
import os
import importlib.util
from typing import Optional

# Global variable to track ComfyUI root path
_COMFY_ROOT: Optional[str] = None
_INITIALIZED: bool = False


def set_comfy_root(path: str) -> None:
    """Set the ComfyUI root directory path."""
    global _COMFY_ROOT
    _COMFY_ROOT = os.path.abspath(path)


def get_comfy_root() -> Optional[str]:
    """Get the current ComfyUI root directory path."""
    return _COMFY_ROOT


def _create_fake_server():
    """Create a fake server module to avoid import errors in nodes that require server."""
    # Create a fake PromptServer class
    class FakePromptServer:
        def __init__(self):
            self.last_node_id = None
            self.client_id = None
        
        def send_sync(self, *args, **kwargs):
            pass  # No-op for script usage
    
    # Create instance before creating the class attribute
    fake_prompt_server_instance = FakePromptServer()
    FakePromptServer.instance = fake_prompt_server_instance
    
    # Create fake server module
    class FakeServer:
        PromptServer = FakePromptServer
        BinaryEventTypes = type('BinaryEventTypes', (), {'PREVIEW_IMAGE': 1})()
    
    # Set up fake server before loading modules that might import it
    if 'server' not in sys.modules:
        sys.modules['server'] = FakeServer()
    
    return FakeServer


def init_comfy(comfy_root: Optional[str] = None) -> None:
    """
    Initialize ComfyUI environment.
    
    Args:
        comfy_root: Path to ComfyUI root directory. If None, will try to auto-detect
                    by looking for ComfyUI directory relative to this file.
    """
    global _COMFY_ROOT, _INITIALIZED
    
    if _INITIALIZED:
        return
    
    # Determine ComfyUI root path
    if comfy_root is None:
        if _COMFY_ROOT:
            comfy_root = _COMFY_ROOT
        else:
            # Try to auto-detect: look for ComfyUI directory relative to this file
            current_file = os.path.abspath(__file__)
            current_dir = os.path.dirname(current_file)
            # Go up to project root
            project_root = os.path.dirname(current_dir)
            
            # 1. Look inside project root (ComfyUI-QabbitWrapper/ComfyUI)
            potential_comfy = os.path.join(project_root, "ComfyUI")
            # 2. Look as a sibling (comfy/ComfyUI)
            potential_sibling = os.path.join(os.path.dirname(project_root), "ComfyUI")
            
            if os.path.exists(potential_comfy):
                comfy_root = potential_comfy
            elif os.path.exists(potential_sibling):
                comfy_root = potential_sibling
            else:
                raise ValueError(
                    "ComfyUI root directory not found. Please specify comfy_root parameter "
                    "or set COMFY_ROOT environment variable."
                )
    
    comfy_root = os.path.abspath(comfy_root)
    if not os.path.exists(comfy_root):
        raise ValueError(f"ComfyUI root directory does not exist: {comfy_root}")
    
    _COMFY_ROOT = comfy_root
    
    # Add ComfyUI to Python path
    if comfy_root not in sys.path:
        sys.path.insert(0, comfy_root)
    
    # Create fake server before importing any ComfyUI modules
    _create_fake_server()
    
    # Import essential ComfyUI modules
    try:
        import folder_paths
        import comfy.model_management as mm
        from comfy.cli_args import args
    except ImportError as e:
        raise ImportError(
            f"Failed to import ComfyUI modules. Make sure ComfyUI is properly installed at {comfy_root}. "
            f"Error: {e}"
        )
    
    _INITIALIZED = True
    print(f"ComfyUI initialized successfully from: {comfy_root}")


def ensure_initialized():
    """Ensure ComfyUI is initialized, raise error if not."""
    if not _INITIALIZED:
        raise RuntimeError(
            "ComfyUI not initialized. Please call init_comfy() first or set COMFY_ROOT environment variable."
        )

