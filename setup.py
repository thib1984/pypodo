from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pypodo',
      version='2.0.0',
      description='pypodo is a todolist tool which works with a .todo file positionned the root of the home directory : use pypodo to run it.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/thib1984/pypodo',
      author='thib1984',
      author_email='thibault.garcon@gmail.com',
      license='mit',
      packages=['pypodo'],
      install_requires=["colorama", "termcolor"],
      zip_safe=False,
      entry_points={
          'console_scripts': ['pypodo=pypodo.__pypodo__:pypodo'],
      }
      )
