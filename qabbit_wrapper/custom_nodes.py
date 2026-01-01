"""
Custom nodes loader module - handles loading custom nodes from ComfyUI custom_nodes directory.

This module provides utilities to load custom nodes, especially those with hyphens in their names
(e.g., ComfyUI-KJNodes, ComfyUI-WanVideoWrapper).
"""

import sys
import os
import importlib.util
from typing import Optional, Dict, Any, List
from .core import get_comfy_root, ensure_initialized


class CustomNodeLoader:
    """Loader for custom nodes with support for hyphenated package names."""
    
    def __init__(self, comfy_root: Optional[str] = None):
        """
        Initialize custom node loader.
        
        Args:
            comfy_root: Path to ComfyUI root. If None, uses get_comfy_root().
        """
        ensure_initialized()
        self.comfy_root = comfy_root or get_comfy_root()
        self.custom_nodes_path = os.path.join(self.comfy_root, "custom_nodes")
        self._loaded_modules: Dict[str, Any] = {}
        self._loaded_packages: Dict[str, Any] = {}
    
    def _create_package_alias(self, package_name: str, package_path: str) -> str:
        """
        Create a Python-importable alias for a package with hyphens.
        
        Args:
            package_name: Original package name (e.g., "ComfyUI-KJNodes")
            package_path: Path to the package directory
            
        Returns:
            Python-importable package name (e.g., "ComfyUI_KJNodes")
        """
        # Replace hyphens with underscores for Python import
        python_package_name = package_name.replace("-", "_")
        
        if python_package_name in self._loaded_packages:
            return python_package_name
        
        # Create parent package module
        parent_module = type(sys)(python_package_name)
        parent_module.__path__ = [package_path]
        parent_module.__file__ = os.path.join(package_path, "__init__.py")
        sys.modules[python_package_name] = parent_module
        self._loaded_packages[python_package_name] = parent_module
        
        return python_package_name
    
    def load_submodule(self, package_name: str, submodule_name: str, filename: str) -> Any:
        """
        Load a submodule from a custom node package.
        
        Args:
            package_name: Python-importable package name (e.g., "ComfyUI_KJNodes")
            submodule_name: Name of the submodule (e.g., "image_nodes")
            filename: Filename of the submodule (e.g., "image_nodes.py")
            
        Returns:
            Loaded module
        """
        # Get package path from loaded packages
        if package_name not in self._loaded_packages:
            raise ValueError(f"Package {package_name} not found or not loaded. Please load it first using load_custom_node_package().")
        
        package_module = self._loaded_packages[package_name]
        if not hasattr(package_module, '__path__') or not package_module.__path__:
            raise ValueError(f"Package {package_name} does not have a valid path")
        
        package_path = package_module.__path__[0]
        
        filepath = os.path.join(package_path, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Submodule file not found: {filepath}")
        
        full_module_name = f"{package_name}.{submodule_name}"
        
        # Check if already loaded
        if full_module_name in sys.modules:
            return sys.modules[full_module_name]
        
        # Load the submodule
        spec = importlib.util.spec_from_file_location(full_module_name, filepath)
        module = importlib.util.module_from_spec(spec)
        module.__package__ = package_name
        module.__name__ = full_module_name
        sys.modules[full_module_name] = module
        spec.loader.exec_module(module)
        
        self._loaded_modules[full_module_name] = module
        return module
    
    def load_custom_node_package(self, package_name: str) -> str:
        """
        Load a custom node package by name.
        
        Args:
            package_name: Name of the package (e.g., "ComfyUI-KJNodes" or "ComfyUI_KJNodes")
            
        Returns:
            Python-importable package name
        """
        # Normalize package name (handle both hyphen and underscore)
        if "-" in package_name:
            python_package_name = package_name.replace("-", "_")
            original_name = package_name
        else:
            python_package_name = package_name
            # Try to find original name with hyphen
            potential_original = package_name.replace("_", "-")
            if os.path.exists(os.path.join(self.custom_nodes_path, potential_original)):
                original_name = potential_original
            else:
                original_name = package_name
        
        # Check if already loaded
        if python_package_name in self._loaded_packages:
            return python_package_name
        
        # Find package directory
        package_path = os.path.join(self.custom_nodes_path, original_name)
        if not os.path.exists(package_path):
            raise FileNotFoundError(
                f"Custom node package not found: {original_name} "
                f"(searched in {self.custom_nodes_path})"
            )
        
        # Create package alias
        self._create_package_alias(original_name, package_path)
        
        return python_package_name
    
    def import_from_custom_node(self, package_name: str, module_path: str, class_name: str):
        """
        Import a class from a custom node package.
        
        Args:
            package_name: Name of the package (e.g., "ComfyUI-KJNodes")
            module_path: Path to the module relative to package root (e.g., "nodes/image_nodes")
            class_name: Name of the class to import
            
        Returns:
            The imported class
        """
        python_package_name = self.load_custom_node_package(package_name)
        
        # Convert module path to Python import path
        if "/" in module_path:
            module_parts = module_path.split("/")
        else:
            module_parts = [module_path]
        
        # Remove .py extension if present
        if module_parts[-1].endswith(".py"):
            module_parts[-1] = module_parts[-1][:-3]
        
        full_module_name = f"{python_package_name}.{'.'.join(module_parts)}"
        
        # Try to load the module
        try:
            if full_module_name in sys.modules:
                module = sys.modules[full_module_name]
            else:
                # Load submodule
                package_path = self._loaded_packages[python_package_name].__path__[0]
                module_file = os.path.join(package_path, *module_parts) + ".py"
                
                if not os.path.exists(module_file):
                    raise FileNotFoundError(f"Module file not found: {module_file}")
                
                spec = importlib.util.spec_from_file_location(full_module_name, module_file)
                module = importlib.util.module_from_spec(spec)
                module.__package__ = python_package_name
                module.__name__ = full_module_name
                sys.modules[full_module_name] = module
                spec.loader.exec_module(module)
        except Exception as e:
            raise ImportError(
                f"Failed to import module {full_module_name} from package {package_name}: {e}"
            )
        
        # Import the class
        if not hasattr(module, class_name):
            raise AttributeError(
                f"Class {class_name} not found in module {full_module_name}"
            )
        
        return getattr(module, class_name)


# Global loader instance
_loader: Optional[CustomNodeLoader] = None


def get_loader() -> CustomNodeLoader:
    """Get or create the global custom node loader."""
    global _loader
    if _loader is None:
        _loader = CustomNodeLoader()
    return _loader


def load_custom_node(package_name: str) -> str:
    """
    Load a custom node package.
    
    Args:
        package_name: Name of the package (e.g., "ComfyUI-KJNodes")
        
    Returns:
        Python-importable package name
        
    Example:
        >>> load_custom_node("ComfyUI-KJNodes")
        'ComfyUI_KJNodes'
    """
    return get_loader().load_custom_node_package(package_name)


def get_custom_node(package_name: str, module_path: str, class_name: str):
    """
    Get a node class from a custom node package.
    
    Args:
        package_name: Name of the package (e.g., "ComfyUI-KJNodes")
        module_path: Path to the module relative to package root (e.g., "nodes/image_nodes")
        class_name: Name of the class to import
        
    Returns:
        The imported class
        
    Example:
        >>> ImageResizeKJv2 = get_custom_node("ComfyUI-KJNodes", "nodes/image_nodes", "ImageResizeKJv2")
        >>> resize_node = ImageResizeKJv2()
    """
    return get_loader().import_from_custom_node(package_name, module_path, class_name)


def list_available_custom_nodes() -> List[str]:
    """
    List all available custom node packages.
    
    Returns:
        List of package names
    """
    ensure_initialized()
    comfy_root = get_comfy_root()
    custom_nodes_path = os.path.join(comfy_root, "custom_nodes")
    
    if not os.path.exists(custom_nodes_path):
        return []
    
    packages = []
    for item in os.listdir(custom_nodes_path):
        item_path = os.path.join(custom_nodes_path, item)
        if os.path.isdir(item_path) and not item.startswith("__"):
            packages.append(item)
    
    return sorted(packages)

