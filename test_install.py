"""
测试安装脚本 - 验证包是否可以正常安装和使用
"""

import sys
import subprocess

def test_install():
    """测试安装过程"""
    print("=" * 60)
    print("测试 comfy-wrapper 安装")
    print("=" * 60)
    
    # 测试 1: 检查 setup.py
    print("\n[测试 1] 检查 setup.py...")
    try:
        import setuptools
        print("✅ setuptools 可用")
    except ImportError:
        print("❌ setuptools 不可用，请安装: pip install setuptools wheel")
        return False
    
    # 测试 2: 验证包结构
    print("\n[测试 2] 验证包结构...")
    import os
    required_files = [
        "setup.py",
        "pyproject.toml",
        "qabbit_wrapper/__init__.py",
        "qabbit_wrapper/core.py",
        "qabbit_wrapper/nodes.py",
        "qabbit_wrapper/custom_nodes.py",
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少文件: {missing_files}")
        return False
    else:
        print("✅ 所有必需文件都存在")
    
    # 测试 3: 尝试导入（不安装的情况下）
    print("\n[测试 3] 尝试导入包（不安装）...")
    sys.path.insert(0, os.path.dirname(__file__))
    try:
        import qabbit_wrapper
        print("✅ 包可以导入（通过路径）")
    except Exception as e:
        print(f"⚠️  包导入失败（这是正常的，需要先安装）: {e}")
    
    # 测试 4: 检查是否可以构建
    print("\n[测试 4] 检查是否可以构建包...")
    try:
        result = subprocess.run(
            [sys.executable, "setup.py", "check"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ setup.py 检查通过")
        else:
            print(f"⚠️  setup.py 检查有警告: {result.stderr}")
    except Exception as e:
        print(f"⚠️  无法运行 setup.py check: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    print("\n如果所有测试都通过，可以运行以下命令安装：")
    print("  pip install -e .  # 开发模式")
    print("  或")
    print("  pip install .      # 普通安装")
    
    return True

if __name__ == "__main__":
    test_install()

