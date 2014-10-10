import json
import os.path
import sys
import shutil

from setuptools import setup
from setuptools.command.install import install

kernel_json = {
  "argv": [sys.executable, "-m", "hy_kernel", "-f", "{connection_file}"],
  "display_name": "Hy",
  "language": "hy",
  "codemirror_mode": "hy",
  "help_links": [
    {
      "text": "Hy Documentation",
      "link": "http://docs.hylang.org/"
    },
    {
      "text": "Hy Google Group",
      "link": "https://groups.google.com/forum/#!forum/hylang-discuss"
    },
    {
      "text": "Hy Github",
      "link": "https://github.com/hylang/hy"
    }
  ]
}

class install_with_kernelspec(install):
    def run(self):
        # Regular installation
        install.run(self)

        # Now write the kernelspec
        from IPython.kernel.kernelspec import KernelSpecManager
        from IPython.utils.path import ensure_dir_exists, locate_profile

        destdir = os.path.join(KernelSpecManager().user_kernel_dir, 'hy')
        ensure_dir_exists(destdir)

        with open(os.path.join(destdir, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)

        print("Updated kernel.json in %s" % destdir)

        cmhydir = os.path.join(
          locate_profile(),
          'static',
          'components',
          'codemirror',
          'mode',
          'hy'
        )
        ensure_dir_exists(cmhydir)
        shutil.copy("hy.js", cmhydir)
        print("Installed hy.js to %s" % cmhydir)

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
      py_modules=['hy_kernel'],
      cmdclass={'install': install_with_kernelspec},
      install_requires=['hy>=0.10.1'],
      classifiers = [
          'Framework :: IPython',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Lisp',
      ]
)
