"""
Simple example - demonstrates the simplest usage pattern.

In a new empty Python file, you can just do:
"""

# Step 1: Import and initialize (only once)
from qabbit_wrapper import init_comfy
from nodes import LoadImage, CLIPLoader

init_comfy("/scratch/e1351271/comfy/ComfyUI")

# Step 2: Use nodes directly
load_image = LoadImage()
image, mask = load_image.load_image(image="Images/humanobj/human/crop_man/commoner/5.jpg")
print(f"Loaded image shape: {image.shape}")

# Step 3: Use custom nodes
from qabbit_wrapper.custom_nodes import get_custom_node

# Import custom node classes
ImageResizeKJv2 = get_custom_node("ComfyUI-KJNodes", "nodes/image_nodes", "ImageResizeKJv2")
ImageBatchMulti = get_custom_node("ComfyUI-KJNodes", "nodes/image_nodes", "ImageBatchMulti")

# Use them
resize_node = ImageResizeKJv2()
batch_node = ImageBatchMulti()

print("Simple example completed!")

