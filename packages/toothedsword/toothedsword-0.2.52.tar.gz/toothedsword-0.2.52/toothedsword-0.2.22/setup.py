
from setuptools import setup, find_packages

setup(
    name="toothedsword",
    version="0.2.22",
    description="nothing",
    packages=find_packages(),
    python_requires=">=3.6",
    include_package_data=True,

    package_data={
        "toothedsword": ["base/*.json", 
                         "tctb/*.json", 
                         "font/*", 
                         "ningxia/*.json"],
                 },
    install_requires=[
        #"numpy>=1.12.0",
        #"pyproj>=1.0.6",
        #"matplotlib>=1.0.0",
        #"opencv-python>=3.0.0",
        #"rioxarray>=0.0.1",
        #"geopandas>=0.1.0",
    ],  
)

