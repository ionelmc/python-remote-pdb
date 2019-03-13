
Changelog
=========

1.3.0 (2019-03-13)
------------------

* Documented support for Python 3.8's ``breakpoint()``.
* Added support for setting the socket listening host/port through the ``REMOTE_PDB_HOST``/``REMOTE_PDB_PORT``
  environment variables. Contributed by Matthew Wilkes in `#14 <https://github.com/ionelmc/python-remote-pdb/pull/14>`_.
* Removed use of `rw` file wrappers around sockets (turns out socket's ``makefile`` is very buggy in Python 3.6 and
  later - `output is discarded <https://bugs.python.org/issue35928>`_). Contributed in `#13
  <https://github.com/ionelmc/python-remote-pdb/pull/13>`_.

1.2.0 (2015-09-26)
------------------

* Always print/log listening address.

1.1.3 (2015-07-06)
------------------

* Corrected the default frame tracing starts from.

1.1.2 (2015-07-06)
------------------

* Small readme update.

1.1.1 (2015-07-06)
------------------

* Remove bogus ``remote_pdb`` console script.

1.1.0 (2015-06-21)
------------------

* Fixed buffering issues when running on Python 3 and Windows.

1.0.0 (2015-06-15)
------------------

* Added support for PDB++.

0.2.1 (2014-03-07)
------------------

* First release on PyPI.
