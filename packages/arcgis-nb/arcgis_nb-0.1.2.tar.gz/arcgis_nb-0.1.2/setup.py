from setuptools import setup, find_packages

setup(
    name="arcgis_nb",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyproj",
        "pillow",
        "matplotlib",
        "numpy",
        "opencv-python",
        "laspy",
        "geopandas",
        "shapely",
        "lazrs",
    ],
    entry_points={
        "console_scripts": [
            "arcgis-nb=arcgis_nb.arcgis:main",
        ],
    },
    author="Amad Ud Din Gakkhar",
    author_email="amad.gakkhar@adept-techsolutions.com",
    description="A tool for extracting and processing LiDAR data for roofing projects in New Brunswick",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/artisanroofing/arcgis_nb",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    python_requires=">=3.7",
)
