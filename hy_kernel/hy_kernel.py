'''
A simple Hy (hylang) kernel for IPython.
'''
import ast

from IPython.kernel.zmq.ipkernel import IPythonKernel
from IPython.utils.py3compat import PY3

import astor

from hy.version import __version__ as hy_version

from hy.macros import _hy_macros, load_macros

from hy.lex import tokenize
from hy.compiler import hy_compile, _compile_table
from hy.core import language

from .version import __version__


class HyKernel(IPythonKernel):
    '''
    This may not be the recommended way to create a kernel, but seems to bring
    the most features along for free.

    Seeking a better solution!
    '''
    implementation = 'hy'
    implementation_version = __version__
    language = 'hy'
    language_version = hy_version
    banner = 'Hy is a wonderful dialect of Lisp that’s embedded in Python.'
    language_info = {
        'name': 'hy',
        'mimetype': 'text/x-hylang',
        'codemirror_mode': {
            'name': 'hy'
        },
        # TODO: port CM to pygments?
        'pygments_lexer': 'ipython3'
    }

    def __init__(self, *args, **kwargs):
        '''
        Create the hy environment
        '''
        super(HyKernel, self).__init__(*args, **kwargs)
        [load_macros(m) for m in ['hy.core', 'hy.macros']]

    def _forward_input(self, *args, **kwargs):
        """Forward raw_input and getpass to the current frontend.

        via input_request
        """
        super(HyKernel, self)._forward_input(*args, **kwargs)

        if PY3:
            language.input = self.raw_input
        else:
            language.raw_input = self.raw_input
            language.input = lambda prompt='': eval(self.raw_input(prompt))

    def do_execute(self, code, *args, **kwargs):
        '''
        Generate python code, and have IPythonKernel run it, or show why we
        couldn't have python code.
        '''
        try:
            tokens = tokenize(code)
            _ast = hy_compile(tokens, '__console__', root=ast.Interactive)
            _ast_for_print = ast.Module()
            _ast_for_print.body = _ast.body
            code = astor.codegen.to_source(_ast_for_print)
        except Exception as err:
            if (not hasattr(err, 'source')) or not err.source:
                err.source = code
            # shell will find the last exception
            self.shell.showsyntaxerror()
            # an empty code cell is basically a no-op
            code = ''
        return super(HyKernel, self).do_execute(code, *args, **kwargs)

    def do_complete(self, code, cursor_pos):
        # let IPython do the heavy lifting for variables, etc.
        txt, matches = self.shell.complete('', code, cursor_pos)

        # mangle underscores into dashes
        matches = [match.replace('_', '-') for match in matches]

        for p in list(_hy_macros.values()) + [_compile_table]:
            p = filter(lambda x: isinstance(x, str), p.keys())
            p = [x.replace('_', '-') for x in p]
            matches.extend([
                x for x in p
                if x.startswith(txt) and x not in matches
            ])

        return {
            'matches': matches,
            'cursor_end': cursor_pos,
            'cursor_start': cursor_pos - len(txt),
            'metadata': {},
            'status': 'ok'
        }


if __name__ == '__main__':
    from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=HyKernel)
