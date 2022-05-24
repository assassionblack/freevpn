from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
  name='freevpn',
  packages=['freevpn'],
  version='1.0',
  python_requires='>=3.6',
  license='GPLv3',
  description='download free configuration for openvpn from freevpn.me',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='assassion',
  author_email='assassionblack666@gmail.com',
  keywords=['freevpn', 'openvpn configuration', 'openvpn free'],
  install_requires=['wget', 'bs4', 'beautifulsoup4', 'requests'],
  classifiers=[
    'Development Status :: 1 - Testing',
    'Topic :: openvpn :: configuration',
    'License :: GNU license :: GPLv3'
  ],
)
