from setuptools import setup

setup(name='pytodo',
      version='0.1.0',
      description='pytodo',
      url='https://github.com/thib1984/pytdodo',
      author='thib1984',
      author_email='thibault.garcon@gmail.com',
      license='MIT',
      packages=['pytodo'],
      zip_safe=False,
      entry_points = {
          'console_scripts': ['pytodo-list=pytodo.__pytodo__:list','pytodo-add=pytodo.__pytodo__:add','pytodo-del=pytodo.__pytodo__:delete','pytodo-clear=pytodo.__pytodo__:clear'],
      }
)
