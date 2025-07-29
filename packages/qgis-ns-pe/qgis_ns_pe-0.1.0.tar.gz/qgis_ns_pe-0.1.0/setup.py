from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qgis-ns-pe",
    version="0.1.0",
    author="Amad Gakkhar",
    author_email="amad.gakkhar@adept-techsolutions.com",
    description="A CLI tool for processing LiDAR data from Nova Scotia and PEI using QGIS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amadgakkhar/qgis-ns-pe",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyproj>=3.0.0",
        "requests>=2.25.1",
        "laspy>=2.0.0",
        "numpy>=1.20.0",
        "matplotlib>=3.3.0",
        "lazrs>=0.1.0",
    ],
    entry_points={
        "console_scripts": [
            "qgis-ns-pe=qgis_ns_pe.cli:main",
        ],
    },
)
