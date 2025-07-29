from setuptools import find_packages
from setuptools import setup

from app.__version__ import VERSION

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()


setup(
    name="special-octo-robot",
    version=VERSION,
    author="Jahan Chaware",
    author_email="sg550js@gmail.com",
    license="GNU GENERAL PUBLIC LICENSE",
    description="Creating my own version of what a CLI Task manager and To-do-list would look like",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geekNero/special-octo-robot.git",
    py_modules=["devcord", "app"],
    packages=find_packages(),
    install_requires=[requirements],
    python_requires=">=3.10",
    platforms=["Windows", "MacOS X", "Linux"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    entry_points={
        "console_scripts": [
            "devcord=devcord:cli",
        ],
    },
)
