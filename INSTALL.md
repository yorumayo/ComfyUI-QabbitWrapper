# 安装指南

## 安装方式

### 方式 1：从源码安装（推荐）

```bash
# 进入项目目录
cd /scratch/e1351271/comfy

# 安装包（开发模式，修改代码后无需重新安装）
pip install -e .

# 或安装为普通包
pip install .
```

### 方式 2：从本地目录安装

```bash
pip install /scratch/e1351271/comfy
```

### 方式 3：使用 pip 从 Git 仓库安装（如果已推送到 Git）

```bash
pip install git+https://github.com/yourusername/comfyui-qabbit-wrapper.git
```

### 方式 4：使用 pip 从本地 Git 仓库安装

```bash
pip install git+file:///scratch/e1351271/comfy
```

## 验证安装

安装完成后，可以运行以下命令验证：

```python
python -c "from qabbit_wrapper import init_comfy; print('安装成功！')"
```

或运行测试脚本：

```bash
python test_wrapper.py
```

## 卸载

```bash
pip uninstall comfyui-qabbit-wrapper
```

## 开发模式

如果你要修改代码，建议使用开发模式安装：

```bash
pip install -e .
```

这样修改代码后无需重新安装，更改会立即生效。

## 依赖

这个包本身不包含 ComfyUI，你需要：

1. 安装 ComfyUI（克隆或下载到本地）
2. 在使用时通过 `init_comfy()` 指定 ComfyUI 的路径

或者设置环境变量：

```bash
export COMFY_ROOT=/path/to/ComfyUI
```

## 常见问题

### Q: 安装后导入失败？

A: 确保你使用的是正确的 Python 环境。可以使用 `which python` 和 `pip show comfyui-qabbit-wrapper` 检查。

### Q: 如何更新包？

A: 如果使用开发模式（`pip install -e .`），直接修改代码即可。如果是普通安装，需要重新运行 `pip install .`。

### Q: 可以在虚拟环境中安装吗？

A: 可以，推荐使用虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
pip install -e .
```

