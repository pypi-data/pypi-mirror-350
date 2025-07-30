from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Calculator(Basic)'
LONG_DESCRIPTION = 'A package to perform basic operations'

# Setting up
setup(
    name="Calculator_Sujal",
    version=VERSION,
    author="Sujal Som",
    author_email="sujals@iitbhilai.ac.in",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'tutorial', 'calculator', 'sujalsom'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

