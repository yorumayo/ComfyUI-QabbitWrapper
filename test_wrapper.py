"""
快速测试脚本 - 验证封装库是否正常工作
"""

print("=" * 60)
print("测试 ComfyUI Wrapper 封装库")
print("=" * 60)

# 测试 1: 导入核心模块
print("\n[测试 1] 导入核心模块...")
try:
    from qabbit_wrapper import init_comfy, get_comfy_root, set_comfy_root
    print("✅ 核心模块导入成功")
except Exception as e:
    print(f"❌ 核心模块导入失败: {e}")
    exit(1)

# 测试 2: 初始化 ComfyUI
print("\n[测试 2] 初始化 ComfyUI...")
try:
    init_comfy("/scratch/e1351271/comfy/ComfyUI")
    print("✅ ComfyUI 初始化成功")
except Exception as e:
    print(f"❌ ComfyUI 初始化失败: {e}")
    exit(1)

# 测试 3: 导入基础节点
print("\n[测试 3] 导入基础节点...")
try:
    from nodes import LoadImage, CLIPLoader
    print("✅ 基础节点导入成功")
    print(f"   - LoadImage: {LoadImage}")
    print(f"   - CLIPLoader: {CLIPLoader}")
except Exception as e:
    print(f"❌ 基础节点导入失败: {e}")
    exit(1)

# 测试 4: 导入 Custom Nodes 功能
print("\n[测试 4] 导入 Custom Nodes 功能...")
try:
    from qabbit_wrapper.custom_nodes import (
        CustomNodePackage,
        load_custom_node,
        get_custom_node,
        list_available_custom_nodes
    )
    print("✅ Custom Nodes 功能导入成功")
except Exception as e:
    print(f"❌ Custom Nodes 功能导入失败: {e}")
    exit(1)

# 测试 5: 列出可用的 custom nodes
print("\n[测试 5] 列出可用的 custom nodes...")
try:
    packages = list_available_custom_nodes()
    print(f"✅ 找到 {len(packages)} 个 custom node 包:")
    for pkg in packages[:5]:  # 只显示前5个
        print(f"   - {pkg}")
    if len(packages) > 5:
        print(f"   ... 还有 {len(packages) - 5} 个")
except Exception as e:
    print(f"⚠️  列出 custom nodes 失败: {e}")

# 测试 6: 加载 KJNodes 包
print("\n[测试 6] 加载 ComfyUI-KJNodes 包...")
try:
    kj = CustomNodePackage("ComfyUI-KJNodes")
    print("✅ ComfyUI-KJNodes 包加载成功")
except Exception as e:
    print(f"⚠️  ComfyUI-KJNodes 包加载失败: {e}")

# 测试 7: 从 KJNodes 导入节点类
print("\n[测试 7] 从 ComfyUI-KJNodes 导入节点类...")
try:
    kj = CustomNodePackage("ComfyUI-KJNodes")
    ImageResizeKJv2 = kj.get("nodes/image_nodes", "ImageResizeKJv2")
    print(f"✅ ImageResizeKJv2 导入成功: {ImageResizeKJv2}")
except Exception as e:
    print(f"⚠️  ImageResizeKJv2 导入失败: {e}")

# 测试 8: 加载 WanVideoWrapper 包
print("\n[测试 8] 加载 ComfyUI-WanVideoWrapper 包...")
try:
    wan = CustomNodePackage("ComfyUI-WanVideoWrapper")
    print("✅ ComfyUI-WanVideoWrapper 包加载成功")
except Exception as e:
    print(f"⚠️  ComfyUI-WanVideoWrapper 包加载失败: {e}")

# 测试 9: 从 WanVideoWrapper 导入节点类
print("\n[测试 9] 从 ComfyUI-WanVideoWrapper 导入节点类...")
try:
    wan = CustomNodePackage("ComfyUI-WanVideoWrapper")
    LoadWanVideoT5TextEncoder = wan.get("nodes_model_loading", "LoadWanVideoT5TextEncoder")
    print(f"✅ LoadWanVideoT5TextEncoder 导入成功: {LoadWanVideoT5TextEncoder}")
except Exception as e:
    print(f"⚠️  LoadWanVideoT5TextEncoder 导入失败: {e}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
print("\n如果所有测试都通过（✅），说明封装库工作正常。")
print("如果有警告（⚠️），可能是某些 custom nodes 不存在或有问题，但不影响基本功能。")

