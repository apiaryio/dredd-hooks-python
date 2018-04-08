#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
import sys
import socket
import os
import json
import threading
import time
import dredd_hooks as hooks
if sys.version_info[0] > 2:
    import io
else:
    import StringIO as io

hooks_thr = None


class Connection(object):

    def __init__(self):
        self.connection = socket.create_connection((hooks.HOST, hooks.PORT))
        self.rfile = self.connection.makefile('rb', -1)  # buffered input
        self.wfile = self.connection.makefile('wb', 0)  # unbuffered output

    def writeline(self, msg):
        msg = msg + hooks.MESSAGE_DELIMITER
        if sys.version_info[0] > 2:
            self.wfile.write(msg.encode('utf-8'))
        else:
            self.wfile.write(msg)

    def readline(self):
        if sys.version_info[0] > 2:
            return self.rfile.readline().decode('utf-8').strip()
        else:
            return self.rfile.readline().strip()

    def close(self):
        self.rfile.close()
        self.wfile.close()
        self.connection.close()


class TestValueError(unittest.TestCase):
    """
    Tests exception handling.
    """
    @classmethod
    def setUpClass(cls):
        cls.output = io.StringIO()
        cls.saved_stderr = sys.stderr
        sys.stderr = cls.output
        cls.hooks_thr = threading.Thread(target=hooks.main,
                                         args=([os.path.abspath(__file__)],))
        cls.hooks_thr.start()
        time.sleep(1)
        cls.conn = Connection()

    @classmethod
    def tearDownClass(cls):
        cls.output.close()
        sys.stderr = cls.saved_stderr
        cls.conn.close()
        hooks.shutdown()
        cls.hooks_thr.join()

    def setUp(self):
        self.conn.writeline(json.dumps({"event": "beforeAll", "data": [{}]}))
        try:
            json.loads(self.conn.readline())
        except Exception:
            pass

    def tearDown(self):
        pass

    def test_output(self):
        out = self.output.getvalue()
        self.assertNotEqual(out.find('ValueErrorRaised'), -1)


class TestGenericException(unittest.TestCase):
    """
    Tests exception handling.
    """
    @classmethod
    def setUpClass(cls):
        cls.output = io.StringIO()
        cls.saved_stderr = sys.stderr
        sys.stderr = cls.output
        cls.hooks_thr = threading.Thread(target=hooks.main,
                                         args=([os.path.abspath(__file__)],))
        cls.hooks_thr.start()
        time.sleep(1)
        cls.conn = Connection()

    @classmethod
    def tearDownClass(cls):
        cls.output.close()
        sys.stderr = cls.saved_stderr
        cls.conn.close()
        hooks.shutdown()
        cls.hooks_thr.join()

    def setUp(self):
        self.conn.writeline(json.dumps({"event": "afterAll", "data": [{}]}))
        try:
            json.loads(self.conn.readline())
        except Exception:
            pass

    def tearDown(self):
        pass

    def test_output(self):
        out = self.output.getvalue()
        self.assertNotEqual(out.find("ExceptionRaised"), -1)


@hooks.before_all
def before_all_test(transactions):
    raise ValueError("ValueErrorRaised")


@hooks.after_all
def after_all_test(transactions):
    raise Exception("ExceptionRaised")


if __name__ == '__main__':
    try:
        unittest.main()
    except Exception as e:
        exit(-1)
