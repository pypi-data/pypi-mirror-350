from setuptools import find_packages, setup

setup(
    name="visiontemplate",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add your package dependencies here
    ],
    author="Intel Open Edge Platform",
    author_email="open-edge-platform@intel.com",
    description="A toolkit for computer vision tasks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/open-edge-platform/visiontemplate",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires=">=3.8",
    license="Apache-2.0",
)
