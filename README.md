# hy_kernel
A simple [IPython][] kernel for [Hy](http://hylang.org), a pythonic lisp.

> NOTE: This requires IPython 3, which is not yet released.

[![The Hy Tutorial as an IPython Notebook](screenshot.png) _The Hy tutorial as an IPython Notebook_][tutorial]

## Features
- basic REPL functionality
- inherits autocomplete from IPython
- syntax highlighting from [lighttable-hylang][]

## Installation
To give it a spin, either check out this repo and `python setup.py` or:

```shell
pip install https://github.com/bollwyvl/hy_kernel/zipball/master
```

Then:

```shell
ipython notebook
```

And pick the `Hy` kernel from the kernel selector. Or:

```shell
ipython qtconsole --kernel hy
```

Though a lot of things don't work quite right there.


## Implementation
It subclasses [IPythonKernel][] directly, as opposed to using [KernelBase][], which is probably the correct thing to do. It works, but might be brittle.

Browser-based syntax highlighting is installed into the `static` area of the default IPython profile at install time... this could probably be done better.


## TODO
- Support cell and line magics
- `do_complete` for better autocomplete
- `do_inspect` for inspection


[IPythonKernel]: https://github.com/ipython/ipython/blob/master/IPython/kernel/zmq/ipkernel.py
[KernelBase]: https://github.com/ipython/ipython/blob/master/IPython/kernel/zmq/kernelbase.py
[lighttable-hylang]: https://github.com/cndreisbach/lighttable-hylang
[tutorial]: http://nbviewer.ipython.org/github/bollwyvl/hy_kernel/blob/master/notebooks/Tutorial.ipynb
[IPython]: http://ipython.org
