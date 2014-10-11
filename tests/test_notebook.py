import os
import re
import sys
import time

from glob import glob

from hy_kernel.setup import setup

from IPython.testing import iptestcontroller

join = os.path.join

test_root = os.path.dirname(__file__)

tests = glob(join(test_root, 'test_*.coffee')) + \
    glob(join(test_root, 'test_*.js'))

class JSController(iptestcontroller.JSController):
    def __init__(self, section, xunit=True, engine='phantomjs'):
        '''Create new test runner.'''
        iptestcontroller.TestController.__init__(self)

        self.engine = engine
        self.section = section
        self.xunit = xunit
        self.slimer_failure = re.compile('^FAIL.*', flags=re.MULTILINE)

        # get the test dir for utils
        ip_test_dir = iptestcontroller.get_js_test_dir()

        extras = [
            '--includes=%s' % join(ip_test_dir, 'util.js'),
            '--engine=%s' % self.engine
        ]

        self.cmd = ['casperjs', 'test'] + extras + tests

    def setup(self):
        # let the super set up the temporary ipython dir
        super(JSController, self).setup()
        # install the assets
        setup(
            kernel_dir=join(self.ipydir.name, 'kernels'),
            profile_dir=join(self.ipydir.name, 'profile', 'default'),
            quiet=True
        )


def main():
    controller = JSController('hy')
    exitcode = 1
    try:
        controller.setup()
        controller.launch(buffer_output=False)
        exitcode = controller.wait()
    except Exception as err:
        print(err)
        exitcode = 1
    finally:
        controller.cleanup()
    return exitcode

if __name__ == '__main__':
    sys.exit(main())
