# 安装示例

## 快速安装

```bash
# 1. 进入项目目录
cd /scratch/e1351271/comfy

# 2. 安装包（开发模式）
pip install -e .
```

## 验证安装

```python
# test_install.py
from qabbit_wrapper import init_comfy
print("✅ qabbit_wrapper 安装成功！")
```

运行：
```bash
python test_install.py
```

## 使用示例

安装后，你可以在任何 Python 脚本中使用：

```python
# my_script.py
from qabbit_wrapper import init_comfy
from nodes import LoadImage

init_comfy("/scratch/e1351271/comfy/ComfyUI")

load_image = LoadImage()
image, mask = load_image.load_image(image="path/to/image.jpg")
print(f"Image shape: {image.shape}")
```

## 在不同环境中安装

### 在虚拟环境中安装

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装包
pip install -e .
```

### 在 Conda 环境中安装

```bash
# 创建 conda 环境
conda create -n qabbit_wrapper python=3.10
conda activate qabbit_wrapper

# 安装包
pip install -e .
```

## 卸载

```bash
pip uninstall comfyui-qabbit-wrapper
```

