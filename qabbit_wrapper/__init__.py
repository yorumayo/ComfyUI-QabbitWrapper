"""
ComfyUI Qabbit Wrapper - A simple wrapper to use ComfyUI nodes in standalone Python scripts.

Usage:
    from qabbit_wrapper import init_comfy
    from nodes import LoadImage, CLIPLoader
    
    # Initialize ComfyUI (only need to call once)
    init_comfy()
    
    # Now you can use nodes
    load_image = LoadImage()
    image, mask = load_image.load_image(image="path/to/image.jpg")
"""

from .core import init_comfy, get_comfy_root, set_comfy_root
from .nodes import *
# Import from custom_nodes submodule (directory takes precedence over file)
from .custom_nodes import CustomNodePackage, load_custom_node, get_custom_node

__all__ = [
    'init_comfy',
    'get_comfy_root',
    'set_comfy_root',
    'load_custom_node',
    'get_custom_node',
    'CustomNodePackage',
]

# Auto-initialize if COMFY_ROOT environment variable is set
import os
if os.environ.get('COMFY_ROOT'):
    init_comfy(os.environ.get('COMFY_ROOT'))

