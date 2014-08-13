=========================
    python-remote-pdb
=========================

.. image:: https://secure.travis-ci.org/ionelmc/python-remote-pdb.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/ionelmc/python-remote-pdb

.. image:: https://coveralls.io/repos/ionelmc/python-remote-pdb/badge.png?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/r/ionelmc/python-remote-pdb

.. image:: https://badge.fury.io/py/remote-pdb.png
    :alt: PYPI Package
    :target: https://pypi.python.org/pypi/remote-pdb

Remote vanilla PDB (over TCP sockets) *done right*: no extras, proper handling around connection failures and CI.
Based on `pdbx <https://pypi.python.org/pypi/pdbx>`_.

Usage
=====

To open a remote PDB on first available port::

    from remote_pdb import set_trace
    set_trace() # you'll see the port number in the logs

To use some specific host/port::

    from remote_pdb import RemotePdb
    RemotePdb('127.0.0.1', 4444).set_trace()

To connect just run ``telnet 127.0.0.1 4444`` ...

Requirements
============

Python 2.6, 2.7, 3.2, 3.3 and PyPy are supported.

Similar projects
================

* `qdb <https://pypi.python.org/pypi/qdb>`_
