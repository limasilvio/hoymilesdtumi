import setuptools
from pathlib import Path

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hoymilesdtumi", 
    version="0.0.1",
    scripts=["bin/dtu_http_request""],
    author="Silvio Lima",
    author_email="dev.silvio@gmail.com",
    description="Hoymiles DTU-MI data wrapper for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sileandro/hoymilesdtumi",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        l.strip() for l in Path('requirements.txt').read_text('utf-8').splitlines()
    ],
)
