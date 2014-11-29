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
To give it a spin, either:

use `pip` 

```shell
pip install -U https://github.com/bollwyvl/hy_kernel/zipball/master
```

or the equivalent

```shell
git clone https://github.com/bollwyvl/hy_kernel.git
cd hy_kernel
pip install -r requirements-test.txt
python setup.py install
# just to be sure
python -m hy_kernel.setup_assets
```

## Execution
To start the notebook in your directory of choice, with a running Hy kernel:
```console
ipython console --kernel hy
```

Or the notebook web GUI:
```shell
ipython notebook --kernel hy
```

Or:
```shell
ipython qtconsole --kernel hy
```

Or:
Your GUI might have a kernel selector: In the Web GUI it's in the 
upper-right-hand corner. Find it, and select `Hy` kernel from the kernel 
selector.
![IPython Kernel Selector ](http://ipython.org/ipython-doc/dev/_images/kernel_selector_screenshot.png)


> Note:
A lot of things don't work quite right in the qt console, and this will not be
supported to the same extent as the HTML notebook.


## Implementation
This kernel subclasses [IPythonKernel][] directly, as opposed to using
[KernelBase][], which is probably the correct thing to do. This works, but might
be brittle. Each cell is run through [astor][], so you're actually seeing hy →
ast → py → ast. While this probably incurs additional overhead, the benefits 
(free magics, all the history works) are just too great to give up.

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
