import setuptools
import codecs
import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()
    
def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

with open("README.md", "r") as fh:
    long_description = fh.read()
    
with open('requirements.txt', 'r') as fr:
    requires = [line.strip() for line in fr.readlines()]
    
setuptools.setup(
    name="lkcom",
    version=get_version("lkcom/__init__.py"),
    author="Lukas Kontenis",
    author_email="dse.ssd@gmail.com",
    description="A Python library of useful routines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/lukaskontenis/lkcom/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requires,
    python_requires='>=3.6'
)
