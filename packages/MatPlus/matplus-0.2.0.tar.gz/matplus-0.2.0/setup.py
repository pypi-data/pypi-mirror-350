import os
import re
import setuptools

NAME = "MatPlus"
AUTHOR = "Dhyey Mavani, Liam Davis, Ryan Ji, Surya Rao, Weixin Lin"
AUTHOR_EMAIL = "davisliam123@gmail.com"
DESCRIPTION = "This package is for easy, convenient plotting in Python."
LICENSE = "MIT"
KEYWORDS = "Plotting Python Matplotlib"
URL = "https://github.com/ac-i2i-engineering/" + NAME
README = "PYPI_README.md"
CLASSIFIERS = [
    "Programming Language :: Cython",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
INSTALL_REQUIRES = ["matplotlib", "numpy", "pandas"]
ENTRY_POINTS = {}
SCRIPTS = []

HERE = os.path.dirname(__file__)


def read(file):
    with open(os.path.join(HERE, file), "r") as fh:
        return fh.read()


VERSION = re.search(
    r'__version__ = [\'"]([^\'"]*)[\'"]', read(NAME.replace("-", "_") + "/__init__.py")
).group(1)

LONG_DESCRIPTION = read(README)

if __name__ == "__main__":
    setuptools.setup(
        name=NAME,
        version=VERSION,
        packages=setuptools.find_packages(),
        author=AUTHOR,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        license=LICENSE,
        keywords=KEYWORDS,
        url=URL,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        entry_points=ENTRY_POINTS,
        scripts=SCRIPTS,
        include_package_data=True,
        python_requires=">=3.8",
    )
