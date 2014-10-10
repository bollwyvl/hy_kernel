import argparse
import ast
import sys
import traceback

from IPython.kernel.zmq.ipkernel import IPythonKernel

import hy

from hy.lex import LexException, PrematureEndOfInput, tokenize
from hy.compiler import hy_compile, HyTypeError
from hy.importer import ast_compile, import_buffer_to_module
from hy.completer import completion

from hy.macros import macro, require

from hy._compat import builtins

SIMPLE_TRACEBACKS = True

class HyKernel(IPythonKernel):
    implementation = 'ihy'
    implementation_version = '1.0'
    language = 'python'  # will be used for
                         # syntax highlighting
    language_version = ''
    banner = 'Simple plotting'

    # lifted from ipython/ipython/IPython/core/interactiveshell.py
    def _run_cell(self, raw_cell, store_history=False, silent=False, shell_futures=True):
        """Run a complete IPython cell.

        Parameters
        ----------
        raw_cell : str
          The code (including IPython code such as %magic functions) to run.
        store_history : bool
          If True, the raw and translated cell will be stored in IPython's
          history. For user code calling back into IPython's machinery, this
          should be set to False.
        silent : bool
          If True, avoid side-effects, such as implicit displayhooks and
          and logging.  silent=True forces store_history=False.
        shell_futures : bool
          If True, the code will share future statements with the interactive
          shell. It will both be affected by previous __future__ imports, and
          any __future__ imports in the code will affect the shell. If False,
          __future__ imports are not shared in either direction.
        """

        shell = self.shell

        if (not raw_cell) or raw_cell.isspace():
            return

        if silent:
            store_history = False

        shell.events.trigger('pre_execute')
        if not silent:
            shell.events.trigger('pre_run_cell')

        # If any of our input transformation (input_transformer_manager or
        # prefilter_manager) raises an exception, we store it in this variable
        # so that we can display the error after logging the input and storing
        # it in the history.
        cell = raw_cell  # cell has to exist so it can be stored/logged

        # Store raw and processed history
        if store_history:
            shell.history_manager.store_inputs(shell.execution_count,
                                              cell, raw_cell)
        if not silent:
            shell.logger.log(cell, raw_cell)

        compiler = ast_compile

        with shell.builtin_trap:
            cell_name = shell.compile.cache(cell, shell.execution_count)

            with shell.display_trap:
                # Execute the user code
                interactivity = "none" if silent else shell.ast_node_interactivity
                tokens = tokenize(raw_cell)
                _ast = hy_compile(tokens, "__console__", root=ast.Interactive)
                shell.run_ast_nodes(_ast.body, cell_name,
                                   interactivity=interactivity, compiler=compiler)

                shell.events.trigger('post_execute')
                if not silent:
                    shell.events.trigger('post_run_cell')

        if store_history:
            # Write output to the database. Does nothing unless
            # history output logging is enabled.
            shell.history_manager.store_output(shell.execution_count)
            # Each cell is a *single* input, regardless of how many lines it has
            shell.execution_count += 1


    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        shell = self.shell # we'll need this a lot here

        self._forward_input(allow_stdin)

        reply_content = {}
        # FIXME: the shell calls the exception handler itself.
        shell._reply_content = None

        try:
            self._run_cell(code, store_history=store_history, silent=silent)
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
            e_info = dict(engine_uuid=self.ident, engine_id=self.int_id, method='execute')
            reply_content['engine_info'] = e_info
            # reset after use
            shell._reply_content = None

        if 'traceback' in reply_content:
            self.log.info('Exception in execute request:\n%s', '\n'.join(reply_content['traceback']))


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
