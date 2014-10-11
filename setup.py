import json
import os.path
import sys
import shutil

from setuptools import setup, find_packages
from setuptools.command.install import install

class install_with_kernelspec(install):
    def run(self):
        # Regular installation
        install.run(self)
        
        from hy_kernel import setup_assets
        setup_assets()

with open('README.md') as f:
    readme = f.read()

svem_flag = '--single-version-externally-managed'
if svem_flag in sys.argv:
    # Die, setuptools, die.
    sys.argv.remove(svem_flag)

setup(name='hy_kernel',
      version='0.1',
      description='A hy kernel for IPython',
      long_description=readme,
      author='Nicholas Bollweg',
      author_email='nick.bollweg@gmail.com',
      url='https://github.com/bollwyvl/hy_kernel',
      packages=find_packages(exclude=('tests', 'notebooks')),
      cmdclass={'install': install_with_kernelspec},
      install_requires=['hy>=0.10.1'],
      classifiers = [
          'Framework :: IPython',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Lisp',
      ]
)
