# -*- coding:utf-8 -*-
import sys
sys.path.append('./src')
from distutils.core import setup
from baiduchannel import __version__

setup(name='baiduchannel',
      version=__version__,
      description='empty python project template',
      long_description=open("README.md").read(),
      author='fanhan',
      author_email='leavesfan@gmail.com',
      packages=['baiduchannel'],
      package_dir={'baiduchannel': 'src/baiduchannel'},
      package_data={'baiduchannel': ['stuff']},
      license="Public domain",
      platforms=["any"],
      url='https://github.com/fanhan/baiduchannel')
