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
    shutil.copy(join(pkgroot, "assets", "kernel.json"), destdir)
    shutil.copy(join(pkgroot, "assets", "logo-32x32.png"), destdir)
    shutil.copy(join(pkgroot, "assets", "logo-64x64.png"), destdir)
    if not quiet:
        print("Updated kernel.json and logos in %s" % destdir)

    try:
        profile_dir = profile_dir or locate_profile()
    except Exception as err:
        print(err)
        print(
            "Couldn't find a profile, probably... run\n"
            "\tpython -m hy_kernel.hy_setup\n"
            "manually."
        )
        return

    cmhydir = join(
        profile_dir,
        'static',
        'components',
        'codemirror',
        'mode',
        'hy'
    )
    ensure_dir_exists(cmhydir)
    shutil.copy(join(pkgroot, "assets", "hy.js"), cmhydir)
    if not quiet:
        print("Installed hy.js to %s" % cmhydir)


def hy_setup():
    setup_assets()


if __name__ == "__main__":
    hy_setup()
