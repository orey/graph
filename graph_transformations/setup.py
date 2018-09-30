import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="graph_transformations",
    version="0.1",
    author="Olivier Rey",
    author_email="rey.olivier@gmail.com",
    description="Graph transformations package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orey/graph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPL V3",
        "Operating System :: OS Independent",
    ],
)

