from __future__ import print_function

import logging
import os
import re
import socket
import sys
import time

import psutil
import pytest
from process_tests import TestProcess
from process_tests import TestSocket
from process_tests import dump_on_error
from process_tests import wait_for_strings

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
            with TestSocket(socket.create_connection((host, int(port)), timeout=TIMEOUT)) as client:
                with dump_on_error(client.read):
                    wait_for_strings(proc.read, TIMEOUT, 'accepted connection from')
                    wait_for_strings(client.read, TIMEOUT, "-> print('{b2}')")
                    client.fh.write(b'continue\r\n')
            wait_for_strings(proc.read, TIMEOUT, 'DIED.')


@pytest.mark.parametrize('kind', ['environ', 'argument'])
def test_quiet(kind):
    with TestProcess(sys.executable, __file__, 'daemon', 'test_quiet', kind) as proc:
        with dump_on_error(proc.read):
            wait_for_strings(proc.read, TIMEOUT,
                             '{a1}',
                             '{b1}')
            psproc = psutil.Process(proc.proc.pid)
            port = None
            t = time.time()
            while port is None and time.time() - t < 5:
                for c in psproc.connections():
                    if c.status == psutil.CONN_LISTEN and c.laddr[0] == '127.0.0.1':
                        port = c.laddr[1]

            with TestSocket(socket.create_connection(('127.0.0.1', int(port)), timeout=TIMEOUT)) as client:
                with dump_on_error(client.read):
                    wait_for_strings(client.read, TIMEOUT, "-> print('{b2}')")
                    client.fh.write(b'continue\r\n')
            wait_for_strings(proc.read, TIMEOUT, 'DIED.')
            assert 'RemotePdb session open at' not in proc.read()


def test_quit():
    with TestProcess(sys.executable, __file__, 'daemon', 'test_simple') as proc:
        with dump_on_error(proc.read):
            wait_for_strings(proc.read, TIMEOUT,
                             '{a1}',
                             '{b1}',
                             'RemotePdb session open at ')
            host, port = re.findall("RemotePdb session open at (.+):(.+),", proc.read())[0]
            with TestSocket(socket.create_connection((host, int(port)), timeout=TIMEOUT)) as client:
                with dump_on_error(client.read):
                    wait_for_strings(proc.read, TIMEOUT, 'accepted connection from')
                    wait_for_strings(client.read, TIMEOUT, "-> print('{b2}')")
                    client.fh.write(b'quit\r\n')
            wait_for_strings(proc.read, TIMEOUT, 'BdbQuit')


def test_redirect():
    with TestProcess(sys.executable, __file__, 'daemon', 'test_redirect') as proc:
        with dump_on_error(proc.read):
            wait_for_strings(proc.read, TIMEOUT,
                             '{a1}',
                             '{b1}',
                             'RemotePdb session open at ')
            host, port = re.findall("RemotePdb session open at (.+):(.+),", proc.read())[0]
            with TestSocket(socket.create_connection((host, int(port)), timeout=TIMEOUT)) as client:
                with dump_on_error(client.read):
                    wait_for_strings(proc.read, TIMEOUT, 'accepted connection from')
                    wait_for_strings(client.read, TIMEOUT, "-> print('{b2}')")
                    client.fh.write(b'break func_a\r\n')
                    client.fh.write(b'continue\r\n')
                    wait_for_strings(client.read, TIMEOUT, 'Breakpoint', '{b2}')
                    wait_for_strings(client.read, TIMEOUT, "-> print('{a2}')")
                    client.fh.write(b'continue\r\n')
                    wait_for_strings(client.read, TIMEOUT, "{=>")
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
            with TestSocket(socket.create_connection((host, int(port)), timeout=TIMEOUT)) as client:
                with dump_on_error(client.read):
                    wait_for_strings(proc.read, TIMEOUT, 'accepted connection from')
                    wait_for_strings(client.read, TIMEOUT, "-> print('{b2}')")
                    client.fh.write(b'break func_a\r\n')
                    client.fh.write(b'continue\r\n')
                    wait_for_strings(client.read, TIMEOUT, "-> print('{a2}')")
                    client.fh.write(b'continue\r\n')
            wait_for_strings(proc.read, TIMEOUT, 'DIED.')
            assert 'Restoring streams' not in proc.read()


def test_trash_input():
    with TestProcess(sys.executable, __file__, 'daemon', 'test_simple') as proc:
        with dump_on_error(proc.read):
            wait_for_strings(proc.read, TIMEOUT,
                             '{a1}',
                             '{b1}',
                             'RemotePdb session open at ')
            host, port = re.findall("RemotePdb session open at (.+):(.+),", proc.read())[0]
            with TestSocket(socket.create_connection((host, int(port)), timeout=TIMEOUT)) as client:
                with dump_on_error(client.read):
                    wait_for_strings(proc.read, TIMEOUT, 'accepted connection from')
                    wait_for_strings(client.read, TIMEOUT, "-> print('{b2}')")
                    for i in range(100):
                        client.fh.write(b'\r\n'.join(b'print("[%d]")' % (i * 10 + j) for j in range(10)) + b'\r\n')
                    client.fh.write(b'continue\r\n')
                    wait_for_strings(client.read, TIMEOUT, *[
                        '[%s]' % i for i in range(1000)
                    ])

            wait_for_strings(proc.read, TIMEOUT, 'DIED.')


def func_b(**kwargs):
    print('{b1}')
    set_trace(**kwargs)
    print('{b2}')


def func_a(block=lambda _: None, **kwargs):
    print('{a1}')
    func_b(**kwargs)
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
    elif test_name == 'test_quiet':
        if sys.argv[3] == 'environ':
            os.environ['REMOTE_PDB_QUIET'] = 'x'
            func_a()
        elif sys.argv[3] == 'argument':
            func_a(quiet=True)
        else:
            raise RuntimeError('Invalid test spec %r.' % sys.argv)
    elif test_name == 'test_redirect':
        func_a(patch_stdstreams=True)
        time.sleep(TIMEOUT)
    else:
        raise RuntimeError('Invalid test spec %r.' % test_name)
    logging.info('DIED.')
