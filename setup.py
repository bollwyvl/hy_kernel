from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop


# should be loaded below
__version__ = None

with open('hy_kernel/version.py') as version:
    exec(version.read())


with open('README.md') as f:
    readme = f.read()


def proxy_cmd(_cmd):
    class Proxied(_cmd):
        def run(self):
            _cmd.run(self)
            from hy_kernel import setup_assets
            setup_assets(True)
    return Proxied


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
        'IPython>=3.0.0',
        'hy>=0.10.1',
    ],
    tests_require=[
        'coverage',
        'nose',
    ],
    cmdclass={
        'install': proxy_cmd(_install),
        'develop': proxy_cmd(_develop)
    },
    classifiers=[
        'Framework :: IPython',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Programming Language :: Lisp',
    ],
    test_suite='nose.collector',
)
