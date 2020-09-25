import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hieroskopia_pkg-simetrik",
    version="0.0.1",
    author="Simetrik",
    author_email="opensource@simetrik.com",
    description="The hiereskopia package its a library to infer properties from dates and numeric data types like formats or separators from samples through regular patterns in a pandas series.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
