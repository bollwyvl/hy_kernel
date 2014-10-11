import os
import shutil

join = os.path.join
pkgroot = os.path.dirname(__file__)

def setup_assets(kernel_dir=None, profile_dir=None, quiet=False):
    # Now write the kernelspec
    from IPython.kernel.kernelspec import KernelSpecManager
    from IPython.utils.path import ensure_dir_exists, locate_profile

    destdir = join(kernel_dir or KernelSpecManager().user_kernel_dir, 'hy')
    ensure_dir_exists(destdir)
    shutil.copy(join(pkgroot, "kernel.json"), destdir)
    if not quiet:
        print("Updated kernel.json in %s" % destdir)

    cmhydir = join(
      profile_dir or locate_profile(),
      'static',
      'components',
      'codemirror',
      'mode',
      'hy'
    )
    ensure_dir_exists(cmhydir)
    shutil.copy(join(pkgroot, "hy.js"), cmhydir)
    if not quiet:
        print("Installed hy.js to %s" % cmhydir)