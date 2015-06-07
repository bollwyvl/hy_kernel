import os

join = os.path.join
pkgroot = os.path.dirname(__file__)


def setup_assets(user=False, ipython_dir=None):
    # Now write the kernelspec
    from IPython.kernel.kernelspec import (
        KernelSpecManager,
        install_kernel_spec,
    )

    if ipython_dir is None:
        install = install_kernel_spec
    else:
        ksm = KernelSpecManager(ipython_dir=ipython_dir)
        install = ksm.install_kernel_spec

    install(
        join(pkgroot, 'assets'),
        'hy',
        replace=True,
        user=user
    )


if __name__ == '__main__':
    setup_assets()  # pragma: no cover
