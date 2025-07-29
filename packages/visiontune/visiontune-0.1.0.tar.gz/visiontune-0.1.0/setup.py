from setuptools import find_packages, setup

setup(
    name="visiontune",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.8",
    author="Intel Open Edge Platform",
    author_email="open-edge-platform@intel.com",
    description="Tuning tools for computer vision models by Intel Open Edge Platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/intel/visionai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    keywords="computer vision, tuning, deep learning, machine learning",
    project_urls={
        "Bug Reports": "https://github.com/intel/visionai/issues",
        "Source": "https://github.com/intel/visionai",
    },
)
