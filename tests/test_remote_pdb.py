from __future__ import print_function

import logging
import os
import re
import socket
import sys
from contextlib import closing

from process_tests import wait_for_strings, dump_on_error
from process_tests import TestProcess
from remote_pdb import PY3
from remote_pdb import set_trace

TIMEOUT = int(os.getenv('REMOTE_PDB_TEST_TIMEOUT', 10))


def test_simple():
    with TestProcess(sys.executable, __file__, 'daemon', 'test_simple') as proc:
        with dump_on_error(proc.read):
            wait_for_strings(proc.read, TIMEOUT,
                             '{a1}',
                             '{b1}',
                             'RemotePdb session open at ')
            host, port = re.findall("RemotePdb session open at (.+):(.+),", proc.read())[0]
            with closing(socket.create_connection((host, int(port)), timeout=TIMEOUT)) as conn:
                if PY3:
                    fh = conn.makefile('rw', buffering=1)
                else:
                    fh = conn.makefile(bufsize=0)
                wait_for_strings(proc.read, TIMEOUT, 'accepted connection from')
                fh.readline()
                assert "-> print('{b2}')" == fh.readline().strip()
                fh.write('quit\r\n')
                fh.readline()
                fh.close()
            wait_for_strings(proc.read, TIMEOUT,
                             'Restoring streams',
                             'DIED.')


def test_redirect():
    with TestProcess(sys.executable, __file__, 'daemon', 'test_redirect') as proc:
        with dump_on_error(proc.read):
            wait_for_strings(proc.read, TIMEOUT,
                             '{a1}',
                             '{b1}',
                             'RemotePdb session open at ')
            host, port = re.findall("RemotePdb session open at (.+):(.+),", proc.read())[0]
            with closing(socket.create_connection((host, int(port)), timeout=TIMEOUT)) as conn:
                if PY3:
                    fh = conn.makefile('rw', buffering=1)
                else:
                    fh = conn.makefile(bufsize=0)
                wait_for_strings(proc.read, TIMEOUT, 'accepted connection from')
                fh.readline()
                assert "-> print('{b2}')" == fh.readline().strip()
                fh.write('break func_a\r\n')
                fh.write('continue\r\n')
                line = fh.readline()
                assert line.startswith('(Pdb) Breakpoint') or line.startswith('(Pdb++) Breakpoint')
                assert fh.readline().strip() in ('(Pdb) {b2}', '(Pdb++) {b2}')
                fh.readline()
                assert "-> print('{a2}')" == fh.readline().strip()
                fh.write('continue\r\n')
                try:
                    fh.readline()
                except Exception as exc:
                    print("fh.readline() failed:", exc)

            wait_for_strings(proc.read, TIMEOUT, 'DIED.')
            assert 'Restoring streams' not in proc.read()


def test_simple_break():
    with TestProcess(sys.executable, __file__, 'daemon', 'test_simple') as proc:
        with dump_on_error(proc.read):
            wait_for_strings(proc.read, TIMEOUT,
                             '{a1}',
                             '{b1}',
                             'RemotePdb session open at ')
            host, port = re.findall("RemotePdb session open at (.+):(.+),", proc.read())[0]
            with closing(socket.create_connection((host, int(port)), timeout=TIMEOUT)) as conn:
                if PY3:
                    fh = conn.makefile('rw', buffering=1)
                else:
                    fh = conn.makefile(bufsize=0)
                wait_for_strings(proc.read, TIMEOUT, 'accepted connection from')
                fh.readline()
                assert "-> print('{b2}')" == fh.readline().strip()
                fh.write('break func_a\r\n')
                fh.write('continue\r\n')
                fh.readline()
                fh.readline()
                assert "-> print('{a2}')" == fh.readline().strip()
                fh.write('continue\r\n')
                try:
                    fh.readline()
                except Exception as exc:
                    print("fh.readline() failed:", exc)

            wait_for_strings(proc.read, TIMEOUT, 'DIED.')
            assert 'Restoring streams' not in proc.read()
            # print('\nCHILD> '.join(proc.read().splitlines()))


def func_b(patch_stdstreams):
    print('{b1}')
    set_trace(patch_stdstreams=patch_stdstreams)
    print('{b2}')


def func_a(block=lambda _: None, patch_stdstreams=False):
    print('{a1}')
    func_b(patch_stdstreams)
    print('{a2}')
    x = block('{a3} ?')
    print('{=> %s}' % x)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(process)d %(asctime)s,%(msecs)05d %(name)s %(levelname)s %(message)s',
        datefmt="%x~%X"
    )
    test_name = sys.argv[2]

    if test_name == 'test_simple':
        func_a()
    elif test_name == 'test_redirect':
        func_a(patch_stdstreams=True)
    else:
        raise RuntimeError('Invalid test spec %r.' % test_name)
    logging.info('DIED.')
