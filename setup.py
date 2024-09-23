from setuptools import setup, find_packages
from os import path

working_dir = path.abspath(path.dirname(__file__))

with open(path.join(working_dir, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='stackspot',
	version='0.0.1',
	author='Guilherme Reginaldo Ruella',
	author_email='potentii@gmail.com',
	description='Stackspot API bindings for Python',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/Potentii/stackspot-python',
	packages=find_packages(),
	install_requires=['requests==2.32.3'],
)