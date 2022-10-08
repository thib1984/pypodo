from setuptools import setup

setup(
    name="pypodo",
    version="5.2.0",
    description="pypodo is a todolist tool which works in your terminal. It has a mecanism of indexes and tags.",
    long_description="The complete description/installation/use/FAQ is available at : https://github.com/thib1984/pypodo#readme",
    long_description_content_type="text/markdown",
    url="https://github.com/thib1984/pypodo",
    author="thib1984",
    author_email="thibault.garcon@gmail.com",
    license="mit",
    packages=["pypodo"],
    install_requires=["termcolor","columnar","python-dateutil"],
    zip_safe=False,
    entry_points={
        "console_scripts": ["pypodo=pypodo.__init__:pypodo"],
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
