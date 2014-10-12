# hy_kernel
[![badge][]][Build Status]
A simple [IPython][] kernel for [Hy](http://hylang.org), a pythonic lisp.

> NOTE:
This requires IPython 3, which is not yet released. It is pretty easy to
[try it out][ipydev], though.

[![](screenshot.png) _The Hy tutorial as an IPython Notebook_][tutorial]

## Features
- basic REPL functionality
- autocomplete from IPython, and most special Hy constructs
- syntax highlighting from [lighttable-hylang][]
- [cell and line magics][magic]
- [pretty good tests][Build Status]

## Installation
To give it a spin, either check out this repo and `python setup.py install` or:

```shell
pip install -U https://github.com/bollwyvl/hy_kernel/zipball/master
```

Then:

```shell
ipython notebook
```

start a new notebook and pick the `Hy` kernel from the kernel selector. Or:

```shell
ipython qtconsole --kernel hy
```

> Note:
A lot of things don't work quite right in the qt console, and this will not be
supported to the same extent as the HTML notebook.


## Implementation
This kernel subclasses [IPythonKernel][] directly, as opposed to using
[KernelBase][], which is probably the correct thing to do. This works, but might
be brittle. Each cell is run through [astor][], so you're actually seeing hy →
ast → py. While this probably incurs additional overhead, the benefits (free
magics, all the history works) are just too great to give up.

Browser-based syntax highlighting is installed into the `static` area of the
default IPython profile at install time... this could probably be done better.


## Feedback
Issues, pull requests and forks are all supported and encouraged. This 
[discussion on `hylang-discuss`][discuss] is also a good place to chime in.

## TODO
- `do_inspect` for inspection

[badge]: https://travis-ci.org/bollwyvl/hy_kernel.svg?branch=master
[Build Status]: https://travis-ci.org/bollwyvl/hy_kernel
[IPythonKernel]: https://github.com/ipython/ipython/blob/master/IPython/kernel/zmq/ipkernel.py
[KernelBase]: https://github.com/ipython/ipython/blob/master/IPython/kernel/zmq/kernelbase.py
[lighttable-hylang]: https://github.com/cndreisbach/lighttable-hylang
[tutorial]: http://nbviewer.ipython.org/github/bollwyvl/hy_kernel/blob/master/notebooks/Tutorial.ipynb
[IPython]: http://ipython.org
[ipydev]: http://ipython.org/ipython-doc/dev/install/install.html#installing-the-development-version
[discuss]: https://groups.google.com/forum/#!topic/hylang-discuss/UkoET6pU5sM
[astor]: https://github.com/berkerpeksag/astor
[magic]: http://nbviewer.ipython.org/github/bollwyvl/hy_kernel/blob/master/notebooks/Magics.ipynb
