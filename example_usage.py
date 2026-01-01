"""
Example usage of ComfyUI wrapper.

This demonstrates how to use ComfyUI nodes in a standalone Python script.
"""

# Method 1: Simple import (auto-initializes if COMFY_ROOT is set)
from qabbit_wrapper import init_comfy
from nodes import LoadImage, CLIPLoader, CLIPVisionLoader

# Initialize ComfyUI (only need to call once)
# If COMFY_ROOT environment variable is set, this is optional
init_comfy("/scratch/e1351271/comfy/ComfyUI")

# Now you can use nodes directly
print("Loading image node...")
load_image_node = LoadImage()
image, mask = load_image_node.load_image(image="Images/humanobj/human/crop_man/commoner/5.jpg")
print(f"Image shape: {image.shape}")

# Method 2: Using custom nodes
from qabbit_wrapper.custom_nodes import get_custom_node, CustomNodePackage

# Option 2a: Direct import using get_custom_node
print("\nLoading custom node using get_custom_node...")
ImageResizeKJv2 = get_custom_node("ComfyUI-KJNodes", "nodes/image_nodes", "ImageResizeKJv2")
resize_node = ImageResizeKJv2()
print(f"Resize node created: {resize_node}")

# Option 2b: Using CustomNodePackage wrapper
print("\nLoading custom node using CustomNodePackage...")
kj = CustomNodePackage("ComfyUI-KJNodes")
ImageBatchMulti = kj.get("nodes/image_nodes", "ImageBatchMulti")
MaskBatchMulti = kj.get("nodes/mask_nodes", "MaskBatchMulti")
print(f"ImageBatchMulti: {ImageBatchMulti}")
print(f"MaskBatchMulti: {MaskBatchMulti}")

# Option 2c: Using WanVideoWrapper nodes
print("\nLoading WanVideoWrapper nodes...")
wan = CustomNodePackage("ComfyUI-WanVideoWrapper")
LoadWanVideoT5TextEncoder = wan.get("nodes_model_loading", "LoadWanVideoT5TextEncoder")
WanVideoVAELoader = wan.get("nodes_model_loading", "WanVideoVAELoader")
print(f"LoadWanVideoT5TextEncoder: {LoadWanVideoT5TextEncoder}")
print(f"WanVideoVAELoader: {WanVideoVAELoader}")

# Method 3: List available custom nodes
from qabbit_wrapper.custom_nodes import list_available_custom_nodes
print("\nAvailable custom nodes:")
for pkg in list_available_custom_nodes():
    print(f"  - {pkg}")

print("\nAll examples completed successfully!")

