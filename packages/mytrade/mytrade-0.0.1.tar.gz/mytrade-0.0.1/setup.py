import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))


VERSION = '0.0.1'
DESCRIPTION = ''
LONG_DESCRIPTION = ''

# Setting up
setup(
    name="mytrade",
    version=VERSION,
    author="",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="",
    packages=find_packages(where='.', exclude=(), include=('*',)),
    include_package_data=True,
    install_requires=[

    ],
    keywords=['python', 'mytrade'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ],
    package_data={
        'mytrade': ['*'],
    },
)
