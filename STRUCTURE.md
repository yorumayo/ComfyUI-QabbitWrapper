# ComfyUI-QabbitWrapper 目录结构

## 目录结构

```
ComfyUI-QabbitWrapper/
├── qabbit_wrapper/              # 主包目录
│   ├── __init__.py             # 包入口
│   ├── core.py                 # 核心初始化逻辑
│   ├── nodes.py                # 导出基础节点
│   ├── custom_nodes.py         # Custom nodes 加载器
│   ├── custom_nodes/           # Custom nodes 便捷接口
│   │   └── __init__.py
│   └── README.md               # API 文档
├── setup.py                     # 安装脚本（setuptools）
├── pyproject.toml              # 项目配置（现代 Python 包标准）
├── MANIFEST.in                  # 包含文件清单
├── LICENSE                      # MIT 许可证
├── README.md                    # 项目主 README
├── INSTALL.md                   # 安装指南
├── INSTALLATION_EXAMPLE.md      # 安装示例
├── USAGE_GUIDE.md               # 使用指南
├── SUMMARY.md                   # 总结文档
├── example_simple.py            # 简单示例
├── example_usage.py             # 完整示例
├── example_refactored.py        # 重构示例
├── test_wrapper.py              # 功能测试
└── test_install.py              # 安装测试
```

## 安装

```bash
cd ComfyUI-QabbitWrapper
pip install -e .  # 开发模式
# 或
pip install .     # 普通安装
```

## 使用

```python
from qabbit_wrapper import init_comfy
from nodes import LoadImage

init_comfy("/path/to/ComfyUI")
load_image = LoadImage()
```

## 包名说明

- **目录名**: `ComfyUI-QabbitWrapper` (带连字符，符合 ComfyUI custom nodes 命名规范)
- **Python 包名**: `qabbit_wrapper` (下划线，符合 Python 包命名规范)
- **pip 包名**: `comfyui-qabbit-wrapper` (小写，带连字符，符合 PyPI 命名规范)

## 文件说明

### 核心文件

- `qabbit_wrapper/`: 主包目录，包含所有核心功能
- `setup.py`: setuptools 安装脚本
- `pyproject.toml`: 现代 Python 项目配置文件

### 文档文件

- `README.md`: 项目主文档
- `INSTALL.md`: 详细安装指南
- `USAGE_GUIDE.md`: 使用指南
- `qabbit_wrapper/README.md`: API 文档

### 示例文件

- `example_simple.py`: 最简单的使用示例
- `example_usage.py`: 完整的使用示例
- `example_refactored.py`: 重构示例（展示如何简化原代码）

### 测试文件

- `test_wrapper.py`: 功能测试脚本
- `test_install.py`: 安装验证脚本

