import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shellio",
    version="1.0.1",
    author="Mateusz Zębala",
    author_email="mateusz.zebala.pl@gmail.com",
    description="ShellIO is a Python interface for interacting with Unix-like shells",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mateuszzebala/shellio",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
      "Programming Language :: Python :: 3.11",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      "Environment :: Console",
      "Topic :: Terminals",
      "Topic :: Software Development :: Libraries",
      "Intended Audience :: Developers",
    ],
    include_package_data=True,
)
