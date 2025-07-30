from distutils.core import setup
from setuptools import find_packages

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(name='zcbot-resource-sdk',
      version='1.0.24',
      description='zcbot resource sdk for zsodata',
      long_description=long_description,
      author='zsodata',
      author_email='team@zso.io',
      url='http://www.zsodata.com',
      install_requires=['pymongo'],
      python_requires='>=3.8',
      license='BSD License',
      packages=find_packages(),
      platforms=['all'],
      include_package_data=True
      )
# zso@2022
