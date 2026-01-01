"""
重构后的 test.py 示例 - 展示如何使用封装库简化代码

这个示例展示了如何将原来的 test.py 重构为使用 qabbit_wrapper 的更简洁版本。
"""

import os
from qabbit_wrapper import init_comfy
init_comfy("/scratch/e1351271/comfy/ComfyUI")

from qabbit_wrapper.nodes import LoadImage, CLIPLoader, CLIPVisionLoader
from qabbit_wrapper.custom_nodes import load_nodes


# 通过配置文件批量加载节点（更整洁的方式）
config_path = os.path.join(os.path.dirname(__file__), "nodes_config.json")
nodes = load_nodes(config_path)

# 将加载的节点类放入全局命名空间
globals().update(nodes)


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

