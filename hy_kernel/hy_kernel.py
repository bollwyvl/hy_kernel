import ast

from IPython.kernel.zmq.ipkernel import IPythonKernel

import astor

from hy.lex import tokenize, LexException
from hy.compiler import hy_compile, HyTypeError
from hy.completer import PATH


class HyKernel(IPythonKernel):
    implementation = 'hy'
    implementation_version = '0.1'
    language = 'hy'
    language_version = '0.10.1'
    banner = 'Hy is a wonderful dialect of Lisp that’s embedded in Python.'

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
        except (HyTypeError, LexException):
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

        for p in PATH:
            p = filter(lambda x: isinstance(x, str), p.keys())
            p = [x.replace("_", "-") for x in p]
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
