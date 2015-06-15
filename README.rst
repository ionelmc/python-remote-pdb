=========================
    python-remote-pdb
=========================

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor|
        | |coveralls| |codecov| |landscape| |scrutinizer|
    * - package
      - |version| |downloads|

..
    |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/python-remote-pdb/badge/?style=flat
    :target: https://readthedocs.org/projects/python-remote-pdb
    :alt: Documentation Status

.. |travis| image:: http://img.shields.io/travis/ionelmc/python-remote-pdb/master.svg?style=flat&label=Travis
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/ionelmc/python-remote-pdb

.. |appveyor| image:: https://img.shields.io/appveyor/ci/ionelmc/python-remote-pdb/master.svg?style=flat&label=AppVeyor
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/ionelmc/python-remote-pdb

.. |coveralls| image:: http://img.shields.io/coveralls/ionelmc/python-remote-pdb/master.svg?style=flat&label=Coveralls
    :alt: Coverage Status
    :target: https://coveralls.io/r/ionelmc/python-remote-pdb

.. |codecov| image:: http://img.shields.io/codecov/c/github/ionelmc/python-remote-pdb/master.svg?style=flat&label=Codecov
    :alt: Coverage Status
    :target: https://codecov.io/github/ionelmc/python-remote-pdb

.. |landscape| image:: https://landscape.io/github/ionelmc/python-remote-pdb/master/landscape.svg?style=flat
    :target: https://landscape.io/github/ionelmc/python-remote-pdb/master
    :alt: Code Quality Status

.. |version| image:: http://img.shields.io/pypi/v/remote-pdb.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/remote-pdb

.. |downloads| image:: http://img.shields.io/pypi/dm/remote-pdb.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/remote-pdb

.. |wheel| image:: https://pypip.in/wheel/remote-pdb/badge.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/remote-pdb

.. |supported-versions| image:: https://pypip.in/py_versions/remote-pdb/badge.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/remote-pdb

.. |supported-implementations| image:: https://pypip.in/implementation/remote-pdb/badge.svg?style=flat
    :alt: Supported imlementations
    :target: https://pypi.python.org/pypi/remote-pdb

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/ionelmc/python-remote-pdb/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/ionelmc/python-remote-pdb/

Remote vanilla PDB (over TCP sockets) *done right*: no extras, proper handling around connection failures and CI.
Based on `pdbx <https://pypi.python.org/pypi/pdbx>`_.

* Free software: BSD license

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

Alternately, one can connect with NetCat: ``nc -C 127.0.0.1 4444``.  When
finished debugging, either exit the debugger, or press Control-c.

Requirements
============

Python 2.6, 2.7, 3.2, 3.3 and PyPy are supported.

Similar projects
================

* `qdb <https://pypi.python.org/pypi/qdb>`_
