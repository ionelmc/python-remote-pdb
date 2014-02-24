from __future__ import print_function
from pdb import Pdb
import socket
import logging
import sys
import errno


def cry(message, stderr=sys.__stderr__):
    logging.critical(message)
    print(message, file=stderr)


class RemotePdb(Pdb):
    """
    This will run pdb as a ephemeral telnet service. Once you connect no one
    else can connect. On construction this object will block execution till a
    client has connected.

    Based on https://github.com/tamentis/rpdb I think ...

    To use this::

        RemotePdb(4444).set_trace()

    Then run: telnet 127.0.0.1 4444
    """
    def __init__(self, host, port, patch_stdstreams=False):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        listen_socket.bind((host, port))
        if not port:
            cry("RemotePdb session open at %s:%s, waiting for connection ..." % listen_socket.getsockname())
            sys.stderr.flush()
        listen_socket.listen(1)
        connection, address = listen_socket.accept()
        cry("RemotePdb accepted connection from %s." % repr(address))
        self.handle = connection.makefile('rw')
        Pdb.__init__(self, completekey='tab', stdin=self.handle, stdout=self.handle)
        self.backup = []
        if patch_stdstreams:
            for name in (
                'stderr',
                'stdout',
                '__stderr__',
                '__stdout__',
                'stdin',
                '__stdin__',
            ):
                self.backup.append((name, getattr(sys, name)))
                setattr(sys, name, self.handle)

    def __restore(self):
        cry('Restoring streams: %s ...' % self.backup)
        for name, fh in self.backup:
            setattr(sys, name, fh)
        self.handle.close()

    #def do_continue(self, arg):
    #    self._close_session()
    #    self.set_continue()
    #    return 1
    #do_c = do_cont = do_continue

    def do_quit(self, arg):
        self.__restore()
        self.set_quit()
        return 1
    do_q = do_exit = do_quit

    def set_trace(self, frame=None):
        if frame is None:
            frame = sys._getframe(1).f_back
        try:
            Pdb.set_trace(self, frame)
        except IOError as exc:
            if exc.errno != errno.ECONNRESET:
                raise

    def set_quit(self):
        sys.settrace(None)

def set_trace(host='127.0.0.1', port=0):
    """
    Opens a remote PDB on first available port.
    """
    rdb = RemotePdb(host, port)
    rdb.set_trace()

