This project is a branch of <a target="_blank" rel="noopener" href="https://pypi.org/project/pyzmq/">pyzmq</a> on <a href="https://www.qpython.org">QPython</a>.

# PyZMQ: Python bindings for ØMQ

This package contains Python bindings for [ZeroMQ](https://zeromq.org).
ØMQ is a lightweight and fast messaging implementation.

PyZMQ should work with any reasonable version of Python (≥ 3.8), as well as PyPy.
PyZMQ supports libzmq ≥ 3.2.2 (including 4.x).

For a summary of changes to pyzmq, see our
[changelog](https://pyzmq.readthedocs.io/en/latest/changelog.html).

### ØMQ 3.x, 4.x

PyZMQ fully supports the stable (not DRAFT) 3.x and 4.x APIs of libzmq,
developed at [zeromq/libzmq](https://github.com/zeromq/libzmq).
No code to change, no flags to pass,
just build pyzmq against the latest and it should work.

## Documentation

See PyZMQ's Sphinx-generated
documentation [on Read the Docs](https://pyzmq.readthedocs.io) for API
details, and some notes on Python and Cython development. If you want to
learn about using ØMQ in general, the excellent [ØMQ
Guide](http://zguide.zeromq.org/py:all) is the place to start, which has a
Python version of every example. We also have some information on our
[wiki](https://github.com/zeromq/pyzmq/wiki).
