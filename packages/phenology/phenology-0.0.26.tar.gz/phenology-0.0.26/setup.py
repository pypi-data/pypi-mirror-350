
import os
import sys
import setuptools

# Get the compatible .pyd files for python version
package_dir = os.path.join(os.getcwd(), "phenology")
if not os.path.exists(package_dir):
    package_dir = os.getcwd()
    print("Package directory not found. Using current directory instead.")
    
pyd_list = [os.path.join(root, file) for root, dirs, files in os.walk(package_dir)
            for file in files if file.endswith(".pyd") and f"cp{sys.version_info.major}{sys.version_info.minor}" in file]

# Get the content of the README.md file
with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

# Set up the package using setuptools
setuptools.setup(
    name = "phenology",
    version = "0.0.26",
    author = "Shen Pengju",
    author_email = "spjace@sina.com",
    description = "A small package for phenology analysis",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/spjace/phenology",
    packages = setuptools.find_packages(),
    install_requires=["geopandas", "joblib", "matplotlib", "numpy", "pandas", "pyproj", "scikit_learn", "scipy", "Shapely", "statsmodels", "tqdm", "xarray"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    package_data={"phenology": pyd_list},
)
