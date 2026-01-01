"""
Convenient imports for custom nodes.

This module provides easy access to custom nodes from various packages.

Usage:
    # After loading a custom node package
    from qabbit_wrapper.custom_nodes import KJNodes, WanVideoWrapper
    
    # Or use the loader directly
    from qabbit_wrapper.custom_nodes import get_custom_node
    ImageResizeKJv2 = get_custom_node("ComfyUI-KJNodes", "nodes/image_nodes", "ImageResizeKJv2")
"""

from ..custom_nodes_logic import (
    load_custom_node,
    get_custom_node,
    list_available_custom_nodes,
    get_loader,
    CustomNodeLoader
)


__all__ = [
    'load_custom_node',
    'get_custom_node',
    'list_available_custom_nodes',
    'get_loader',
    'CustomNodeLoader',
    'load_nodes',
]




class CustomNodePackage:
    """
    A convenient wrapper for accessing nodes from a custom node package.
    
    Usage:
        kj = CustomNodePackage("ComfyUI-KJNodes")
        ImageResizeKJv2 = kj.get("nodes/image_nodes", "ImageResizeKJv2")
    """
    
    def __init__(self, package_name: str):
        """
        Initialize a custom node package wrapper.
        
        Args:
            package_name: Name of the package (e.g., "ComfyUI-KJNodes")
        """
        self.package_name = package_name
        self.python_package_name = load_custom_node(package_name)
        self._loader = get_loader()
    
    def get(self, module_path: str, class_name: str):
        """
        Get a node class from this package.
        
        Args:
            module_path: Path to the module relative to package root (e.g., "nodes/image_nodes")
            class_name: Name of the class to import
            
        Returns:
            The imported class
        """
        return self._loader.import_from_custom_node(
            self.package_name,
            module_path,
            class_name
        )
    
    def load_submodule(self, submodule_name: str, filename: str):
        """
        Load a submodule from this package.
        
        Args:
            submodule_name: Name of the submodule (e.g., "image_nodes")
            filename: Filename of the submodule (e.g., "image_nodes.py")
            
        Returns:
            Loaded module
        """
        return self._loader.load_submodule(
            self.python_package_name,
            submodule_name,
            filename
        )


# Pre-configured package wrappers for common packages
def _create_package_wrapper(package_name: str):
    """Create a package wrapper class dynamically."""
    class PackageWrapper:
        def __init__(self):
            self._package = CustomNodePackage(package_name)
        
        def get(self, module_path: str, class_name: str):
            return self._package.get(module_path, class_name)
        
        def load_submodule(self, submodule_name: str, filename: str):
            return self._package.load_submodule(submodule_name, filename)
    
    return PackageWrapper()


# Lazy-loading package wrappers
_KJNodes = None
_WanVideoWrapper = None


def _get_KJNodes():
    """Get KJNodes package wrapper."""
    global _KJNodes
    if _KJNodes is None:
        _KJNodes = CustomNodePackage("ComfyUI-KJNodes")
    return _KJNodes


def _get_WanVideoWrapper():
    """Get WanVideoWrapper package wrapper."""
    global _WanVideoWrapper
    if _WanVideoWrapper is None:
        _WanVideoWrapper = CustomNodePackage("ComfyUI-WanVideoWrapper")
    return _WanVideoWrapper


# Export CustomNodePackage
__all__.append('CustomNodePackage')

# Convenience functions for common packages
def get_KJNodes():
    """Get KJNodes package wrapper."""
    return CustomNodePackage("ComfyUI-KJNodes")


def get_WanVideoWrapper():
    """Get WanVideoWrapper package wrapper."""
    return CustomNodePackage("ComfyUI-WanVideoWrapper")


def load_nodes(config):
    """
    Load multiple nodes based on a configuration dictionary or JSON file.
    
    Args:
        config (dict or str): Path to a JSON file or a dictionary mapping 
                             package names to module/class mappings.
        
    Returns:
        dict: Mapping of class names to node classes.
    """
    if isinstance(config, str):
        import json
        with open(config, 'r') as f:
            config = json.load(f)
            
    loaded_nodes = {}
    for package_name, modules in config.items():
        pkg = CustomNodePackage(package_name)
        for module_path, class_names in modules.items():
            if isinstance(class_names, str):
                class_names = [class_names]
            for class_name in class_names:
                loaded_nodes[class_name] = pkg.get(module_path, class_name)
                
    return loaded_nodes

