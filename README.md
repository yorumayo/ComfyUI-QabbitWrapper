# ComfyUI-QabbitWrapper

一个简单易用的 ComfyUI 封装库，让你可以在独立的 Python 脚本中直接使用 ComfyUI 的节点，无需启动完整的 ComfyUI 服务器。

## 特性

- ✅ 简单导入：`from nodes import LoadImage, CLIPLoader` 即可使用
- ✅ 自动处理带连字符的包名（如 `ComfyUI-KJNodes`）
- ✅ 支持所有 ComfyUI 基础节点
- ✅ 支持所有 custom_nodes
- ✅ 自动初始化 ComfyUI 环境
- ✅ 创建假的 server 模块避免导入错误
- ✅ 可安装的 Python 包

## 安装

### 方式 1：从源码安装（推荐）

```bash
# 进入项目目录
cd ComfyUI-QabbitWrapper

# 安装包（开发模式，修改代码后无需重新安装）
pip install -e .

# 或安装为普通包
pip install .
```

### 方式 2：从本地目录安装

```bash
pip install /path/to/ComfyUI-QabbitWrapper
```

详细安装说明请查看 [INSTALL.md](INSTALL.md)。

## 快速开始

```python
from qabbit_wrapper import init_comfy
from nodes import LoadImage, CLIPLoader

# 初始化 ComfyUI（只需要调用一次）
init_comfy("/path/to/ComfyUI")

# 现在可以直接使用节点了
load_image = LoadImage()
image, mask = load_image.load_image(image="path/to/image.jpg")
```

## 使用 Custom Nodes

```python
from qabbit_wrapper import init_comfy
from qabbit_wrapper.custom_nodes import CustomNodePackage

init_comfy("/path/to/ComfyUI")

# 创建包包装器
kj = CustomNodePackage("ComfyUI-KJNodes")
ImageResizeKJv2 = kj.get("nodes/image_nodes", "ImageResizeKJv2")

# 使用节点
resize_node = ImageResizeKJv2()
```

## 文档

- [使用指南](USAGE_GUIDE.md) - 完整的使用指南和示例
- [API 文档](qabbit_wrapper/README.md) - 详细的 API 文档
- [安装指南](INSTALL.md) - 详细的安装说明
- [目录结构](STRUCTURE.md) - 项目结构说明

## 示例

- [简单示例](example_simple.py) - 最简单的使用示例
- [完整示例](example_usage.py) - 完整的使用示例
- [重构示例](example_refactored.py) - 展示如何简化原代码

## 许可证

MIT License
