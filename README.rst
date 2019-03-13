========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-remote-pdb/badge/?style=flat
    :target: https://readthedocs.org/projects/python-remote-pdb
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/ionelmc/python-remote-pdb.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/ionelmc/python-remote-pdb

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/ionelmc/python-remote-pdb?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/ionelmc/python-remote-pdb

.. |requires| image:: https://requires.io/github/ionelmc/python-remote-pdb/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/ionelmc/python-remote-pdb/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/ionelmc/python-remote-pdb/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/ionelmc/python-remote-pdb

.. |codecov| image:: https://codecov.io/github/ionelmc/python-remote-pdb/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/ionelmc/python-remote-pdb

.. |version| image:: https://img.shields.io/pypi/v/remote-pdb.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/remote-pdb

.. |commits-since| image:: https://img.shields.io/github/commits-since/ionelmc/python-remote-pdb/v1.3.0.svg
    :alt: Commits since latest release
    :target: https://github.com/ionelmc/python-remote-pdb/compare/v1.3.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/remote-pdb.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/remote-pdb

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/remote-pdb.svg
    :alt: Supported versions
    :target: https://pypi.org/project/remote-pdb

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/remote-pdb.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/remote-pdb


.. end-badges

Remote vanilla PDB (over TCP sockets) *done right*: no extras, proper handling around connection failures and CI. Based
on `pdbx <https://pypi.python.org/pypi/pdbx>`_.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install remote-pdb

Usage
=====

To open a remote PDB on first available port:

.. code:: python

    from remote_pdb import set_trace
    set_trace() # you'll see the port number in the logs

To use some specific host/port:

.. code:: python

    from remote_pdb import RemotePdb
    RemotePdb('127.0.0.1', 4444).set_trace()

To connect just run ``telnet 127.0.0.1 4444``.  When you are finished
debugging, either exit the debugger, or press Control-], then Control-d.

Alternately, one can connect with NetCat: ``nc -C 127.0.0.1 4444`` or Socat: ``socat readline
tcp:127.0.0.1:4444`` (for line editing and history support).  When finished debugging, either exit
the debugger, or press Control-c.

Integration with breakpoint() in Python 3.7+
============================================

If you are using Python 3.7 one can use the new ``breakpoint()`` built in to invoke
remote PDB. In this case the following environment variable must be set:

.. code:: bash

    PYTHONBREAKPOINT=remote_pdb.set_trace

The debugger can then be invoked as follows, without any imports:

.. code:: python

    breakpoint()

As the ``breakpoint()`` function does not take any arguments, environment variables can be used to
specify the host and port that the server should listen to. For example, to run ``script.py`` in such a
way as to make ``telnet 127.0.0.1 4444`` the correct way of connecting, one would run:

.. code:: bash

    PYTHONBREAKPOINT=remote_pdb.set_trace REMOTE_PDB_HOST=127.0.0.1 REMOTE_PDB_PORT=4444 python script.py

If ``REMOTE_PDB_HOST`` is omitted then a default value of 127.0.0.1 will be used. If ``REMOTE_PDB_PORT`` is
omitted then the first available port will be used. The connection information will be logged to the console,
as with calls to ``remote_pdb.set_trace()``.


Note about OS X
===============

In certain scenarios (backgrounded processes) OS X will prevent readline to be imported (and readline is a dependency of pdb). 
A workaround (run this early):

.. code:: python

    import signal
    signal.signal(signal.SIGTTOU, signal.SIG_IGN)

See `#9 <https://github.com/ionelmc/python-remote-pdb/issues/9>`_ and `cpython#14892 <http://bugs.python.org/issue14892>`_.

Requirements
============

Python 2.6, 2.7, 3.2, 3.3 and PyPy are supported.

Similar projects
================

* `qdb <https://pypi.python.org/pypi/qdb>`_
