from setuptools import setup, find_packages

setup(
    name="ImageTopoDec",
    version="1.0.6",
    description="Python wrapper for the Barcode library.",
    author="Art A",
    author_email="your.email@example.com",
    url="https://github.com/Noremos/Barcode",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license=open("LICENSE").read(),
    classifiers=[
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.11",
    install_requires=[
        "numpy",
        "matplotlib",
    ],
    package_data={
        "ImageTopoDec": [
            "libbarpy.so",
            "libbarpy.pyi",
            "libbarpy.pyd"
        ],
    },
    has_ext_modules = lambda: True,
)
