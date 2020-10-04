from setuptools import setup

setup(name='pytodo',
      version='0.1.0',
      description='pytodo is a todolist program who works with a .todo file at the root of the home directory',
      url='https://github.com/thib1984/pytdodo',
      author='thib1984',
      author_email='thibault.garcon@gmail.com',
      packages=['pytodo'],
      zip_safe=False,
      entry_points = {
          'console_scripts': ['pytodo-list=pytodo.__pytodo__:list','pytodo-add=pytodo.__pytodo__:add','pytodo-del=pytodo.__pytodo__:delete','pytodo-clear=pytodo.__pytodo__:clear','pytodo=pytodo.__pytodo__:help','pytodo-untag=pytodo.__pytodo__:untag','pytodo-tag=pytodo.__pytodo__:tag'],
      }
)
