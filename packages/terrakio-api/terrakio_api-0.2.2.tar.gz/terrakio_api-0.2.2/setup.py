from setuptools import setup

setup(
    name="terrakio_api",
    version="0.2.2",
    author="Yupeng Chao",
    author_email="yupeng@haizea.com.au",
    description="A client library for Terrakio's WCS API service",
    url="https://github.com/HaizeaAnalytics/terrakio-python-api",
    packages=["terrakio_api"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.7",
    install_requires=[
        "terrakio-core>=0.1.0",
        "requests>=2.25.0",
        "pyyaml>=5.1",
        "xarray>=2023.1.0",
        "netcdf4>=1.6.0",
        "pandas>=1.5.0",
        "numpy>=1.22.0",
        "scipy>=1.8.0",
        "shapely>=2.0.0",
    ],
    metadata_version='2.2'
) 