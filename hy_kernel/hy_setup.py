import os

join = os.path.join
pkgroot = os.path.dirname(__file__)


def setup_assets(user=False):
    # Now write the kernelspec
    from IPython.kernel.kernelspec import install_kernel_spec

    install_kernel_spec(join(pkgroot, 'assets'), 'hy', replace=True, user=user)


if __name__ == '__main__':
    setup_assets()
