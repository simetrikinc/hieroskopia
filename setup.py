import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hieroskopia",
    version="0.1.2",
    author="Simetrik Inc",
    author_email="opensource@simetrik.com",
    description="The hiereskopia package is a library to infer properties like date formats or numeric separators in pandas series of type object or string.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simetrikinc/hieroskopia",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
