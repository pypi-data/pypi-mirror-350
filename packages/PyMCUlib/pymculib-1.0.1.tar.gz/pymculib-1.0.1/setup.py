from setuptools import setup, find_packages

setup(
    name="PyMCUlib",
    version="1.0.1",
    description="Material Color Utilities Python Library",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Wenkang Li",
    author_email="support@deepblue.cc",
    url="https://github.com/wenkang-deepblue/material-color-utilities-python",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "numpy",
        "pillow",
    ],
    python_requires=">=3.12.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Multimedia :: Graphics",
    ],
)
