"""
重构后的 test.py 示例 - 展示如何使用封装库简化代码

这个示例展示了如何将原来的 test.py 重构为使用 qabbit_wrapper 的更简洁版本。
"""

from qabbit_wrapper import init_comfy
init_comfy("/scratch/e1351271/comfy/ComfyUI")

from qabbit_wrapper.nodes import LoadImage, CLIPLoader, CLIPVisionLoader
from qabbit_wrapper.custom_nodes import CustomNodePackage


# 创建 custom node 包包装器
kj = CustomNodePackage("ComfyUI-KJNodes")
wan = CustomNodePackage("ComfyUI-WanVideoWrapper")

# 导入所有需要的节点类（比原来的方式简洁多了）
# 基础节点
load_image_node = LoadImage()
clip_loader_node = CLIPLoader()
clip_vision_loader_node = CLIPVisionLoader()

# KJNodes
ImageResizeKJv2 = kj.get("nodes/image_nodes", "ImageResizeKJv2")
ImageBatchMulti = kj.get("nodes/image_nodes", "ImageBatchMulti")
MaskBatchMulti = kj.get("nodes/mask_nodes", "MaskBatchMulti")

# WanVideoWrapper
LoadWanVideoT5TextEncoder = wan.get("nodes_model_loading", "LoadWanVideoT5TextEncoder")
WanVideoVAELoader = wan.get("nodes_model_loading", "WanVideoVAELoader")
WanVideoModelLoader = wan.get("nodes_model_loading", "WanVideoModelLoader")
WanVideoLoraSelect = wan.get("nodes_model_loading", "WanVideoLoraSelect")
WanVideoBlockSwap = wan.get("nodes_model_loading", "WanVideoBlockSwap")
WanVideoVRAMManagement = wan.get("nodes_model_loading", "WanVideoVRAMManagement")
WanVideoTorchCompileSettings = wan.get("nodes_model_loading", "WanVideoTorchCompileSettings")

WanVideoTextEncode = wan.get("nodes", "WanVideoTextEncode")
WanVideoClipVisionEncode = wan.get("nodes", "WanVideoClipVisionEncode")
WanVideoImageToVideoEncode = wan.get("nodes", "WanVideoImageToVideoEncode")
WanVideoDecode = wan.get("nodes", "WanVideoDecode")
WanVideoSetBlockSwap = wan.get("nodes", "WanVideoSetBlockSwap")
WanVideoAddBindweaveEmbeds = wan.get("nodes", "WanVideoAddBindweaveEmbeds")
WanVideoEncodeLatentBatch = wan.get("nodes", "WanVideoEncodeLatentBatch")
TextImageEncodeQwenVL = wan.get("nodes", "TextImageEncodeQwenVL")

WanVideoSampler = wan.get("nodes_sampler", "WanVideoSampler")

# 创建节点实例
resize_node = ImageResizeKJv2()
image_batch_multi_node = ImageBatchMulti()
mask_batch_multi_node = MaskBatchMulti()

t5_loader_node = LoadWanVideoT5TextEncoder()
vae_loader_node = WanVideoVAELoader()
model_loader_node = WanVideoModelLoader()

print("所有节点已成功导入和实例化！")
print("现在可以使用这些节点了，就像在原来的 test.py 中一样。")

# 示例：加载图像
image_path = "Images/humanobj/human/crop_man/commoner/5.jpg"
image, mask = load_image_node.load_image(image=image_path)
print(f"加载的图像形状: {image.shape}")

