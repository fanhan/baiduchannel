# -*- coding:utf-8 -*-
import sys
sys.path.append('./src')
from distutils.core import setup
from bdchannel import __version__

setup(name='bdchannel',
      version=__version__,
      description='empty python project template',
      long_description=open("README.md").read(),
      author='fanhan',
      author_email='leavesfan@gmail.com',
      packages=['bdchannel'],
      package_dir={'bdchannel': 'src/bdchannel'},
      package_data={'bdchannel': ['stuff']},
      license="Public domain",
      platforms=["any"],
      url='https://github.com/fanhan/baiduchannel')
