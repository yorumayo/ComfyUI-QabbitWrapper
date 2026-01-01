"""
Setup script for comfy-wrapper package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "qabbit_wrapper", "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

setup(
    name="comfyui-qabbit-wrapper",
    version="0.1.0",
    description="A simple wrapper to use ComfyUI nodes in standalone Python scripts (Qabbit Wrapper)",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="ComfyUI Qabbit Wrapper Contributors",
    license="MIT",
    python_requires=">=3.9",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    package_data={
        "qabbit_wrapper": ["README.md"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="comfyui qabbit wrapper nodes ai image-generation",
    project_urls={
        "Homepage": "https://github.com/yorumayo/ComfyUI-QabbitWrapper",
        "Documentation": "https://github.com/yorumayo/ComfyUI-QabbitWrapper#readme",
        "Repository": "https://github.com/yorumayo/ComfyUI-QabbitWrapper",
        "Issues": "https://github.com/yorumayo/ComfyUI-QabbitWrapper/issues",
    },
)

