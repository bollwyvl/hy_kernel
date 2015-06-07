# hy_kernel
[![build-badge][]][build] [![pypi-badge][]][pypi]

A simple [Jupyter][] kernel for [Hy](http://hylang.org), a pythonic lisp.

[![](screenshot.png) _The Hy tutorial as a Jupyter Notebook_][tutorial]


## Features
- basic REPL functionality
- autocomplete from IPython, and most special Hy constructs
- syntax highlighting from [lighttable-hylang][]
- [cell and line magics][magic]
- [interactive widgets][widgets]
- [pretty good tests][build]


## Installation


### pip
```shell
pip install hy_kernel
```


### docker
You can try out Hy Kernel in Docker with [Docker Compose][docker-compose]:

```bash
git clone https://github.com/bollwyvl/hy_kernel.git
cd hy_kernel && docker-compose up
```

## Execution
To start the notebook in your directory of choice, with a running Hy kernel:

```console
ipython console --kernel hy
```

Or the notebook web GUI:

```shell
ipython notebook
```

Or:
```shell
ipython qtconsole --kernel hy
```

Or:
Your GUI might have a kernel selector: In the Web GUI it's in the
upper-right-hand corner. Find it, and select `Hy` kernel from the kernel
selector.

![IPython Kernel Selector][kernel-selector]


> Note:
A lot of things don't work quite right in the qt console, and this will not be
supported to the same extent as the HTML notebook.


## Implementation
This kernel subclasses [IPythonKernel][] directly, as opposed to using
[KernelBase][], which is probably the correct thing to do. This works, but
might be brittle. Each cell is run through [astor][], so you're actually
seeing hy → ast → py → ast. While this probably incurs additional overhead,
the benefits (free magics, all the history works) are just too great to
give up.

Browser-based syntax highlighting is installed into the `static` area of the
default IPython profile at install time... this could probably be done better.


## Feedback
Issues, pull requests and forks are all supported and encouraged. This
[discussion on `hylang-discuss`][discuss] is also a good place to chime in.


## TODO
- `do_inspect` for inspection

[astor]: https://github.com/berkerpeksag/astor
[build-badge]: https://travis-ci.org/bollwyvl/hy_kernel.svg
[build]: https://travis-ci.org/bollwyvl/hy_kernel
[discuss]: https://groups.google.com/forum/#!topic/hylang-discuss/UkoET6pU5sM
[docker-compose]: https://docs.docker.com/compose/
[IPythonKernel]: https://github.com/ipython/ipython/blob/master/IPython/kernel/zmq/ipkernel.py
[Jupyter]: http://jupyter.org
[kernel-selector]: http://ipython.org/ipython-doc/dev/_images/kernel_selector_screenshot.png
[KernelBase]: https://github.com/ipython/ipython/blob/master/IPython/kernel/zmq/kernelbase.py
[lighttable-hylang]: https://github.com/cndreisbach/lighttable-hylang
[magic]: notebooks/Magics.ipynb
[pypi-badge]: https://img.shields.io/pypi/v/hy_kernel.svg
[pypi]: https://pypi.python.org/pypi/hy_kernel/
[tutorial]: http://nbviewer.ipython.org/github/bollwyvl/hy_kernel/blob/master/notebooks/Tutorial.ipynb
[widgets]: notebooks/Widgets.ipynb
