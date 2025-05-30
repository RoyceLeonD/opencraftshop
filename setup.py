from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="opencraftshop",
    version="1.0.0",
    author="OpenCraftShop Contributors",
    author_email="support@opencraftshop.org",
    description="Programmatic woodworking and 3D model designer with optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/opencraftshop/opencraftshop",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "matplotlib>=3.6.0",
        "numpy-stl>=3.0.0",
        "click>=8.1.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "opencraftshop=main:design_furniture",
        ],
    },
)