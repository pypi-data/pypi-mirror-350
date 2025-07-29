from setuptools import find_packages, setup

setup(
    name="visiondata",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "opencv-python>=4.8.0",
        "pandas>=2.0.0",
        "pillow>=10.0.0",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "pylint>=2.17.0",
        ],
    },
    python_requires=">=3.8",
    author="Intel Open Edge Platform",
    author_email="open-edge-platform@intel.com",
    description="Data management and processing tools for computer vision applications by Intel Open Edge Platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/intel/visionai",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    keywords="computer vision, data management, deep learning, machine learning",
    project_urls={
        "Bug Reports": "https://github.com/intel/visionai/issues",
        "Source": "https://github.com/intel/visionai",
    },
)
