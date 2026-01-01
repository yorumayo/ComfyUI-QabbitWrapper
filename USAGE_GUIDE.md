# ComfyUI Qabbit Wrapper 使用指南

## 概述

`qabbit_wrapper` 是一个封装库，让你可以在独立的 Python 脚本中直接使用 ComfyUI 的节点，无需启动完整的 ComfyUI 服务器。

## 目录结构

```
comfy/
├── qabbit_wrapper/          # 封装库主目录
│   ├── __init__.py         # 主入口
│   ├── core.py             # 核心初始化逻辑
│   ├── nodes.py            # 导出基础节点
│   ├── custom_nodes.py     # Custom nodes 加载器
│   ├── custom_nodes/
│   │   └── __init__.py     # Custom nodes 便捷接口
│   └── README.md           # 详细文档
├── example_simple.py        # 简单示例
├── example_usage.py        # 完整示例
└── example_refactored.py   # 重构示例（对比原 test.py）
```

## 快速开始

### 1. 最简单的用法

创建一个新的 Python 文件：

```python
# my_script.py
from qabbit_wrapper import init_comfy
from nodes import LoadImage

# 初始化（只需要一次）
init_comfy("/scratch/e1351271/comfy/ComfyUI")

# 使用节点
load_image = LoadImage()
image, mask = load_image.load_image(image="path/to/image.jpg")
print(f"Image shape: {image.shape}")
```

### 2. 使用 Custom Nodes

```python
from qabbit_wrapper import init_comfy
from qabbit_wrapper.custom_nodes import CustomNodePackage

init_comfy("/scratch/e1351271/comfy/ComfyUI")

# 创建包包装器
kj = CustomNodePackage("ComfyUI-KJNodes")

# 导入节点类
ImageResizeKJv2 = kj.get("nodes/image_nodes", "ImageResizeKJv2")
ImageBatchMulti = kj.get("nodes/image_nodes", "ImageBatchMulti")

# 使用节点
resize_node = ImageResizeKJv2()
batch_node = ImageBatchMulti()
```

### 3. 完整示例（重构 test.py）

参考 `example_refactored.py`，展示了如何将原来的 `test.py` 重构为使用封装库的版本。

**原来的方式（test.py）：**
```python
# 需要手动处理包名、路径、fake server 等
wanvideo_wrapper_path = os.path.join(COMFY_ROOT, "custom_nodes", "ComfyUI-WanVideoWrapper")
sys.path.insert(0, wanvideo_wrapper_path)
package_name = "ComfyUI_WanVideoWrapper"
parent_module = type(sys)(package_name)
# ... 很多复杂的代码
```

**使用封装库后：**
```python
from qabbit_wrapper import init_comfy
from qabbit_wrapper.custom_nodes import CustomNodePackage

init_comfy("/scratch/e1351271/comfy/ComfyUI")
wan = CustomNodePackage("ComfyUI-WanVideoWrapper")
LoadWanVideoT5TextEncoder = wan.get("nodes_model_loading", "LoadWanVideoT5TextEncoder")
```

## API 参考

### 核心 API

#### `init_comfy(comfy_root: Optional[str] = None)`

初始化 ComfyUI 环境。

**参数：**
- `comfy_root`: ComfyUI 根目录路径。如果为 None，会尝试：
  1. 使用之前设置的路径（通过 `set_comfy_root()`）
  2. 使用环境变量 `COMFY_ROOT`
  3. 自动检测（在当前目录的父目录中查找 ComfyUI）

**示例：**
```python
init_comfy("/path/to/ComfyUI")
# 或
import os
os.environ['COMFY_ROOT'] = "/path/to/ComfyUI"
init_comfy()  # 会自动使用环境变量
```

#### `get_comfy_root() -> Optional[str]`

获取当前 ComfyUI 根目录。

#### `set_comfy_root(path: str)`

设置 ComfyUI 根目录。

### Custom Nodes API

#### `load_custom_node(package_name: str) -> str`

加载一个 custom node 包。

**参数：**
- `package_name`: 包名，支持带连字符（如 "ComfyUI-KJNodes"）或下划线（如 "ComfyUI_KJNodes"）

**返回：**
- Python 可导入的包名（如 "ComfyUI_KJNodes"）

**示例：**
```python
from qabbit_wrapper.custom_nodes import load_custom_node
pkg_name = load_custom_node("ComfyUI-KJNodes")  # 返回 "ComfyUI_KJNodes"
```

#### `get_custom_node(package_name: str, module_path: str, class_name: str)`

从 custom node 包中获取一个节点类。

**参数：**
- `package_name`: 包名（如 "ComfyUI-KJNodes"）
- `module_path`: 模块路径，相对于包根目录，使用 "/" 分隔（如 "nodes/image_nodes"）
- `class_name`: 类名（如 "ImageResizeKJv2"）

**返回：**
- 导入的类

**示例：**
```python
from qabbit_wrapper.custom_nodes import get_custom_node
ImageResizeKJv2 = get_custom_node("ComfyUI-KJNodes", "nodes/image_nodes", "ImageResizeKJv2")
```

#### `CustomNodePackage(package_name: str)`

Custom node 包的包装器类，提供更便捷的访问方式。

**方法：**
- `get(module_path: str, class_name: str)`: 获取节点类
- `load_submodule(submodule_name: str, filename: str)`: 加载子模块

**示例：**
```python
from qabbit_wrapper.custom_nodes import CustomNodePackage

kj = CustomNodePackage("ComfyUI-KJNodes")
ImageResizeKJv2 = kj.get("nodes/image_nodes", "ImageResizeKJv2")
ImageBatchMulti = kj.get("nodes/image_nodes", "ImageBatchMulti")
```

#### `list_available_custom_nodes() -> List[str]`

列出所有可用的 custom node 包。

**示例：**
```python
from qabbit_wrapper.custom_nodes import list_available_custom_nodes
packages = list_available_custom_nodes()
print(packages)  # ['ComfyUI-KJNodes', 'ComfyUI-WanVideoWrapper', ...]
```

## 常见用法模式

### 模式 1：基础节点使用

```python
from qabbit_wrapper import init_comfy
from nodes import LoadImage, CLIPLoader, CLIPVisionLoader

init_comfy("/path/to/ComfyUI")

load_image = LoadImage()
clip_loader = CLIPLoader()
clip_vision_loader = CLIPVisionLoader()
```

### 模式 2：单个 Custom Node 包

```python
from qabbit_wrapper import init_comfy
from qabbit_wrapper.custom_nodes import get_custom_node

init_comfy("/path/to/ComfyUI")

# 导入需要的类
ImageResizeKJv2 = get_custom_node("ComfyUI-KJNodes", "nodes/image_nodes", "ImageResizeKJv2")
ImageBatchMulti = get_custom_node("ComfyUI-KJNodes", "nodes/image_nodes", "ImageBatchMulti")

# 使用
resize_node = ImageResizeKJv2()
batch_node = ImageBatchMulti()
```

### 模式 3：多个 Custom Node 包（推荐）

```python
from qabbit_wrapper import init_comfy
from qabbit_wrapper.custom_nodes import CustomNodePackage

init_comfy("/path/to/ComfyUI")

# 创建包包装器
kj = CustomNodePackage("ComfyUI-KJNodes")
wan = CustomNodePackage("ComfyUI-WanVideoWrapper")

# 从不同包导入节点
ImageResizeKJv2 = kj.get("nodes/image_nodes", "ImageResizeKJv2")
LoadWanVideoT5TextEncoder = wan.get("nodes_model_loading", "LoadWanVideoT5TextEncoder")
```

### 模式 4：批量导入（适合大型项目）

```python
from qabbit_wrapper import init_comfy
from qabbit_wrapper.custom_nodes import CustomNodePackage

init_comfy("/path/to/ComfyUI")

# 创建包包装器
kj = CustomNodePackage("ComfyUI-KJNodes")
wan = CustomNodePackage("ComfyUI-WanVideoWrapper")

# 批量导入所有需要的节点
KJ_NODES = {
    'ImageResizeKJv2': kj.get("nodes/image_nodes", "ImageResizeKJv2"),
    'ImageBatchMulti': kj.get("nodes/image_nodes", "ImageBatchMulti"),
    'MaskBatchMulti': kj.get("nodes/mask_nodes", "MaskBatchMulti"),
}

WAN_NODES = {
    'LoadWanVideoT5TextEncoder': wan.get("nodes_model_loading", "LoadWanVideoT5TextEncoder"),
    'WanVideoVAELoader': wan.get("nodes_model_loading", "WanVideoVAELoader"),
    'WanVideoModelLoader': wan.get("nodes_model_loading", "WanVideoModelLoader"),
    # ... 更多节点
}

# 使用
resize_node = KJ_NODES['ImageResizeKJv2']()
t5_loader = WAN_NODES['LoadWanVideoT5TextEncoder']()
```

## 如何找到 Custom Node 的路径和类名

1. **找到包名**：查看 `ComfyUI/custom_nodes/` 目录下的文件夹名
   - 例如：`ComfyUI-KJNodes`、`ComfyUI-WanVideoWrapper`

2. **找到模块路径**：
   - 查看包内的文件结构
   - 例如：`ComfyUI-KJNodes/nodes/image_nodes.py` → 模块路径为 `nodes/image_nodes`

3. **找到类名**：
   - 打开对应的 Python 文件
   - 查找类定义（如 `class ImageResizeKJv2:`）

**示例：**
```
ComfyUI-KJNodes/
├── nodes/
│   ├── image_nodes.py      # 模块路径: nodes/image_nodes
│   │   └── class ImageResizeKJv2  # 类名: ImageResizeKJv2
│   └── mask_nodes.py       # 模块路径: nodes/mask_nodes
│       └── class MaskBatchMulti   # 类名: MaskBatchMulti
```

## 注意事项

1. **初始化顺序**：必须在使用任何节点之前调用 `init_comfy()`
2. **包名格式**：支持带连字符（`ComfyUI-KJNodes`）或下划线（`ComfyUI_KJNodes`）
3. **模块路径**：使用 "/" 分隔，相对于包根目录
4. **相对导入**：Custom nodes 中的相对导入会自动处理
5. **Server 模块**：库会自动创建假的 server 模块，避免导入错误

## 故障排除

### 问题：找不到包

**错误：** `FileNotFoundError: Custom node package not found: ...`

**解决：**
1. 检查包名是否正确
2. 检查包是否存在于 `ComfyUI/custom_nodes/` 目录
3. 使用 `list_available_custom_nodes()` 查看可用包列表

### 问题：找不到类

**错误：** `AttributeError: Class ... not found in module ...`

**解决：**
1. 检查模块路径是否正确
2. 检查类名是否正确（区分大小写）
3. 打开源文件确认类是否存在

### 问题：导入错误

**错误：** `ImportError: Failed to import module ...`

**解决：**
1. 检查模块路径格式（使用 "/" 分隔）
2. 检查文件是否存在
3. 查看源文件的依赖是否满足

## 更多示例

查看以下文件获取更多示例：
- `example_simple.py`: 最简单的使用示例
- `example_usage.py`: 完整的使用示例
- `example_refactored.py`: 重构示例（对比原 test.py）

