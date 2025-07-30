from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
with codecs.open(os.path.join(here, "LICENSE"), encoding="utf-8") as fh:
    license = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'Python bindings for cava audio visualizer'

# Setting up
setup(
    name="python-libcava",
    version=VERSION,
    author="LIZARD-OFFICIAL-77",
    author_email="<lizard.official.77@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=[
        'open-source',
        'foss',
        'cava',
        'linux',
        'fifo'
    ],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: POSIX :: Linux',
    ],
    license=license,
    project_urls={
        'Source Code': 'https://github.com/LIZARD-OFFICIAL-77/python-libcava/',  # GitHub link
        'Bug Tracker': 'https://github.com/LIZARD-OFFICIAL-77/python-libcava/issues',  # Link to issue tracker
    },
    url = "https://github.com/LIZARD-OFFICIAL-77/python-libcava/"
)