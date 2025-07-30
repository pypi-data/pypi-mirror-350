from setuptools import setup, find_packages  # Make sure to import find_packages

setup(
    name="terrakio_core",
    version="0.2.2",
    author="Yupeng Chao",
    author_email="yupeng@haizea.com.au",
    description="Core components for Terrakio API clients",
    url="https://github.com/HaizeaAnalytics/terrakio-python-api",
    packages = find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "pyyaml>=5.1",
        "xarray>=2023.1.0",
        "shapely>=2.0.0",
        "geopandas>=0.13.0",
    ],
    metadata_version='2.2'
) 