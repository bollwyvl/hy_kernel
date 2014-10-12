import ast
import sys
import traceback

from IPython.kernel.zmq.ipkernel import IPythonKernel

import astor

from hy.lex import tokenize
from hy.compiler import hy_compile


class HyKernel(IPythonKernel):
    implementation = 'hy'
    implementation_version = '0.1'
    language = 'hy'
    language_version = '0.10.1'
    banner = 'Hy is a wonderful dialect of Lisp that’s embedded in Python.'

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):

        shell = self.shell

        self._forward_input(allow_stdin)

        reply_content = {}

        shell._reply_content = None

        try:
            tokens = tokenize(code)
            _ast = hy_compile(tokens, "__console__", root=ast.Interactive)
            _ast_for_print = ast.Module()
            _ast_for_print.body = _ast.body

            shell.run_cell(
                astor.codegen.to_source(_ast_for_print),
                store_history=store_history,
                silent=silent
            )
        except:
            status = u'error'
            # FIXME: this code right now isn't being used yet by default,
            # because the run_cell() call above directly fires off exception
            # reporting.  This code, therefore, is only active in the scenario
            # where runlines itself has an unhandled exception.  We need to
            # uniformize this, for all exception construction to come from a
            # single location in the codbase.
            etype, evalue, tb = sys.exc_info()
            if not hasattr(evalue, 'source') or evalue.source is None:
                evalue.source = code
            tb_list = traceback.format_exception(etype, evalue, tb)
            reply_content.update(shell._showtraceback(etype, evalue, tb_list))
        else:
            status = u'ok'
        finally:
            self._restore_input()

        reply_content[u'status'] = status

        # Return the execution counter so clients can display prompts
        reply_content['execution_count'] = shell.execution_count - 1

        # FIXME - fish exception info out of shell, possibly left there by
        # runlines.  We'll need to clean up this logic later.
        if shell._reply_content is not None:
            reply_content.update(shell._reply_content)
            e_info = dict(
                engine_uuid=self.ident,
                engine_id=self.int_id,
                method='execute'
            )
            reply_content['engine_info'] = e_info
            # reset after use
            shell._reply_content = None

        if 'traceback' in reply_content:
            self.log.info(
                'Exception in execute request:\n%s',
                '\n'.join(reply_content['traceback'])
            )

        # At this point, we can tell whether the main code execution succeeded
        # or not.  If it did, we proceed to evaluate user_expressions
        if reply_content['status'] == 'ok':
            reply_content[u'user_expressions'] = \
                shell.user_expressions(user_expressions or {})
        else:
            # If there was an error, don't even try to compute expressions
            reply_content[u'user_expressions'] = {}

        # Payloads should be retrieved regardless of outcome, so we can both
        # recover partial output (that could have been generated early in a
        # block, before an error) and clear the payload system always.
        reply_content[u'payload'] = shell.payload_manager.read_payload()
        # Be agressive about clearing the payload because we don't want
        # it to sit in memory until the next execute_request comes in.
        shell.payload_manager.clear_payload()

        return reply_content

if __name__ == '__main__':
    from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=HyKernel)
