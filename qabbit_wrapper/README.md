# ComfyUI Qabbit Wrapper

一个简单易用的 ComfyUI 封装库，让你可以在独立的 Python 脚本中直接使用 ComfyUI 的节点，无需启动完整的 ComfyUI 服务器。

## 特性

- ✅ 简单导入：`from nodes import LoadImage, CLIPLoader` 即可使用
- ✅ 自动处理带连字符的包名（如 `ComfyUI-KJNodes`）
- ✅ 支持所有 ComfyUI 基础节点
- ✅ 支持所有 custom_nodes
- ✅ 自动初始化 ComfyUI 环境
- ✅ 创建假的 server 模块避免导入错误

## 安装

### 方式 1：从源码安装（推荐）

```bash
# 进入项目目录
cd /path/to/comfy

# 安装包（开发模式，修改代码后无需重新安装）
pip install -e .

# 或安装为普通包
pip install .
```

### 方式 2：从本地目录安装

```bash
pip install /path/to/comfy
```

详细安装说明请查看项目根目录的 [INSTALL.md](../INSTALL.md)。

## 快速开始

### 方法 1：最简单的用法

```python
# 在一个新的空 Python 文件中
from qabbit_wrapper import init_comfy
from nodes import LoadImage, CLIPLoader

# 初始化 ComfyUI（只需要调用一次）
init_comfy("/path/to/ComfyUI")

# 现在可以直接使用节点了
load_image = LoadImage()
image, mask = load_image.load_image(image="path/to/image.jpg")
print(f"Image shape: {image.shape}")
```

### 方法 2：使用环境变量

```bash
export COMFY_ROOT=/path/to/ComfyUI
```

```python
# Python 文件会自动初始化
from nodes import LoadImage
load_image = LoadImage()
```

### 方法 3：使用 Custom Nodes

```python
from qabbit_wrapper import init_comfy
from qabbit_wrapper.custom_nodes import get_custom_node, CustomNodePackage

init_comfy("/path/to/ComfyUI")

# 方法 3a: 直接导入
ImageResizeKJv2 = get_custom_node("ComfyUI-KJNodes", "nodes/image_nodes", "ImageResizeKJv2")
resize_node = ImageResizeKJv2()

# 方法 3b: 使用包装器（推荐）
kj = CustomNodePackage("ComfyUI-KJNodes")
ImageBatchMulti = kj.get("nodes/image_nodes", "ImageBatchMulti")
MaskBatchMulti = kj.get("nodes/mask_nodes", "MaskBatchMulti")

# 使用节点
batch_node = ImageBatchMulti()
mask_node = MaskBatchMulti()
```

### 方法 4：完整示例（参考 test.py）

```python
from qabbit_wrapper import init_comfy
from nodes import LoadImage, CLIPLoader, CLIPVisionLoader
from qabbit_wrapper.custom_nodes import CustomNodePackage

# 初始化
init_comfy("/path/to/ComfyUI")

# 加载基础节点
load_image_node = LoadImage()
clip_loader_node = CLIPLoader()

# 加载 custom nodes
kj = CustomNodePackage("ComfyUI-KJNodes")
wan = CustomNodePackage("ComfyUI-WanVideoWrapper")

# 导入需要的类
ImageResizeKJv2 = kj.get("nodes/image_nodes", "ImageResizeKJv2")
ImageBatchMulti = kj.get("nodes/image_nodes", "ImageBatchMulti")
LoadWanVideoT5TextEncoder = wan.get("nodes_model_loading", "LoadWanVideoT5TextEncoder")
WanVideoVAELoader = wan.get("nodes_model_loading", "WanVideoVAELoader")

# 使用节点
resize_node = ImageResizeKJv2()
t5_loader = LoadWanVideoT5TextEncoder()
```

## API 文档

### 核心函数

#### `init_comfy(comfy_root: Optional[str] = None)`

初始化 ComfyUI 环境。

- `comfy_root`: ComfyUI 根目录路径。如果为 None，会尝试自动检测或使用环境变量 `COMFY_ROOT`。

#### `get_comfy_root() -> Optional[str]`

获取当前 ComfyUI 根目录路径。

#### `set_comfy_root(path: str)`

设置 ComfyUI 根目录路径。

### Custom Nodes API

#### `load_custom_node(package_name: str) -> str`

加载一个 custom node 包。

- `package_name`: 包名（如 "ComfyUI-KJNodes"）
- 返回: Python 可导入的包名（如 "ComfyUI_KJNodes"）

#### `get_custom_node(package_name: str, module_path: str, class_name: str)`

从 custom node 包中获取一个节点类。

- `package_name`: 包名（如 "ComfyUI-KJNodes"）
- `module_path`: 模块路径，相对于包根目录（如 "nodes/image_nodes"）
- `class_name`: 类名（如 "ImageResizeKJv2"）
- 返回: 导入的类

#### `list_available_custom_nodes() -> List[str]`

列出所有可用的 custom node 包。

#### `CustomNodePackage(package_name: str)`

Custom node 包的包装器类，提供便捷的访问方式。

**方法：**
- `get(module_path: str, class_name: str)`: 获取节点类
- `load_submodule(submodule_name: str, filename: str)`: 加载子模块

## 示例文件

- `example_simple.py`: 最简单的使用示例
- `example_usage.py`: 完整的使用示例，展示各种用法

## 注意事项

1. **初始化顺序**：在使用任何节点之前，必须先调用 `init_comfy()`
2. **包名处理**：带连字符的包名（如 `ComfyUI-KJNodes`）会自动转换为 Python 可导入的形式（`ComfyUI_KJNodes`）
3. **相对导入**：custom nodes 中的相对导入会自动处理
4. **Server 模块**：库会自动创建假的 server 模块，避免导入错误

## 常见问题

### Q: 如何找到 custom node 中的类名？

A: 查看 custom node 的源代码文件，找到类定义。例如，`ComfyUI-KJNodes/nodes/image_nodes.py` 中的 `ImageResizeKJv2` 类。

### Q: 如何知道模块路径？

A: 模块路径是相对于 custom node 包根目录的路径。例如，如果文件在 `ComfyUI-KJNodes/nodes/image_nodes.py`，模块路径就是 `nodes/image_nodes`。

### Q: 支持哪些 ComfyUI 版本？

A: 支持 ComfyUI 的最新版本。如果遇到兼容性问题，请检查 ComfyUI 的更新日志。

## 许可证

与 ComfyUI 相同的许可证。

