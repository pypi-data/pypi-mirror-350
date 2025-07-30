# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="RcToolBox",  # pypi package name, should be unique
    version="1.0",  # version number, should follow semantic versioning (MAJOR.MINOR.PATCH)
    keywords=[
        "pip",
        "RcToolBox",
    ],  # keywords for the package, used for searching on PyPI
    description="RC personal ToolBox",  # description of the package, displayed on PyPI
    long_description="RC personal ToolBox",
    license="MIT",  # license of the package, should be a valid SPDX license identifier
    url="",  # PyPI project URL, can be empty if not applicable
    author="RC",  # author of the package, can be a name or an organization
    author_email="yilingyaomeng@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "numpy==1.26.4",
        "PyYAML==6.0.2",
        "SimpleITK==2.4.0",
        "pathos==0.3.4",
        "pandas==2.2.3",
        "openpyxl==3.1.5",
    ],
    # list of dependencies, can be empty if no dependencies
)
