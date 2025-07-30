import setuptools
import os
import re

from setuptools import find_packages, setup

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

with open('requirements.txt','r',encoding='utf-8') as fh:
    install_requires = fh.readlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def get_version():
    init = open(os.path.join(ROOT, 'tihan', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)

setuptools.setup(
    name = "tihan_sdv",
    version = get_version(),
    description="Software Defined Vehicle in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author= "Arindam Chakraborty",
    packages=[
        "tihan.sdv.visualizer",
        "tihan.sdv.securetransfer",
        "tihan.sdv.compression"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    install_requires=install_requires,
    python_requires=">=3.8",
    setup_requires=["wheel"],
    license="Apache License 2.0"

)