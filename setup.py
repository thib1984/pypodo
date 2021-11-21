from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pypodo",
    version="4.1.0",
    description="pypodo is a todolist tool which works with a .todo file at the root of the home directory. It has a mecanism of indexes and tags.",
    long_description="The complete description/installation/use/FAQ is available at : https://github.com/thib1984/pypodo#readme",
    long_description_content_type="text/markdown",
    url="https://github.com/thib1984/pypodo",
    author="thib1984",
    author_email="thibault.garcon@gmail.com",
    license="mit",
    packages=["pypodo"],
    install_requires=["setuptools", "termcolor","columnar"],
    zip_safe=False,
    entry_points={
        "console_scripts": ["pypodo=pypodo.__init__:pypodo"],
    },
)
