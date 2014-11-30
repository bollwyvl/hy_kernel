import sys

from setuptools import setup, find_packages
from setuptools.command.install import install as _install

exec open('hy_kernel/version.py')

class install(_install):
    def run(self):
        # Regular installation
        _install.run(self)

        from hy_kernel import setup_assets
        setup_assets()

with open('README.md') as f:
    readme = f.read()

svem_flag = '--single-version-externally-managed'
if svem_flag in sys.argv:
    # Die, setuptools, die.
    sys.argv.remove(svem_flag)

setup(
    name='hy_kernel',
    version=__version__,
    description='A hy kernel for IPython',
    long_description=readme,
    author='Nicholas Bollweg',
    author_email='nick.bollweg@gmail.com',
    url='https://github.com/bollwyvl/hy_kernel',
    packages=find_packages(exclude=('tests', 'notebooks')),
    include_package_data=True,
    install_requires=[
        'IPython==3.0.0-dev',
        'hy>=0.10.1',
        'jsonpointer',
        'jsonschema',
        'requests',
        'pygments',
        'mistune',
        'tornado',
        'jinja2',
        'sphinx',
        'pyzmq',
        'mock',
    ],
    dependency_links=[
        "git+git://github.com/ipython/ipython.git#egg=IPython-3.0.0-dev"
    ],
    classifiers = [
        'Framework :: IPython',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Programming Language :: Lisp',
    ],
    test_suite='nose.collector',
)
