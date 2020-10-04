from setuptools import setup

setup(name='pytodolist',
      version='0.2.0',
      description='pytodo is a todolist program who works with a .todo file at the root of the home directory',
      url='https://github.com/thib1984/pytdodo',
      author='thib1984',
      author_email='thibault.garcon@gmail.com',
      packages=['pytodolist'],
      zip_safe=False,
      entry_points = {
          'console_scripts': ['pytodo=pytodolist.__pytodolist__:pytodo'],
      }
)
