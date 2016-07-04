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
        print("%d" % (sys.version_info[0]))
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


class TestMultiHooks(unittest.TestCase):
    """
    Tests multiple hooks one function.
    """
    @classmethod
    def setUpClass(cls):
        cls.output = io.StringIO()
        cls.saved_stdout = sys.stdout
        sys.stdout = cls.output
        cls.hooks_thr = threading.Thread(target=hooks.main,
                                         args=([os.path.abspath(__file__)],))
        cls.hooks_thr.start()
        time.sleep(1)
        cls.conn = Connection()

    @classmethod
    def tearDownClass(cls):
        cls.output.close()
        sys.stdout = cls.saved_stdout
        cls.conn.close()
        hooks.shutdown()
        cls.hooks_thr.join()
        time.sleep(1)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_before_all(self):
        self.conn.writeline(json.dumps({"event": "beforeAll", "data": [{}]}))
        msg = json.loads(self.conn.readline())
        expect = {"event": "beforeAll",
                  "data": [{
                      "hooks_modifications": ["multi hook for all"]}]}
        self.assertDictEqual(msg, expect)

    def test_after_all(self):
        self.conn.writeline(json.dumps({"event": "afterAll", "data": [{}]}))
        msg = json.loads(self.conn.readline())
        expect = {"event": "afterAll",
                  "data": [{
                      "hooks_modifications": ["multi hook for all"]}]}
        self.assertDictEqual(msg, expect)

    def test_before_validation(self):
        self.conn.writeline(json.dumps(
            {"event": "beforeEachValidation",
             "data": {
                 "name": "Machines > Machines collection > Get Machines"}}))
        msg = json.loads(self.conn.readline())
        expect = \
            {
                "event": "beforeEachValidation",
                "data":
                {
                    "name": "Machines > Machines collection > Get Machines",
                    "hooks_modifications":
                    [
                        "multi hook for single",
                    ],
                    "extra": "extra item",
                }
            }
        self.assertDictEqual(msg, expect)

    def test_before(self):
        self.conn.writeline(json.dumps(
            {"event": "beforeEach",
             "data": {
                 "name": "Machines > Machines collection > Get Machines"}}))
        msg = json.loads(self.conn.readline())
        expect = \
            {
                "event": "beforeEach",
                "data":
                {
                    "name": "Machines > Machines collection > Get Machines",
                    "hooks_modifications":
                    [
                        "multi hook for single",
                        "multi hook for single",
                    ],
                    "extra": "extra item",
                }
            }
        self.assertDictEqual(msg, expect)

    def test_after(self):
        self.conn.writeline(json.dumps(
            {"event": "afterEach",
             "data": {
                 "name": "Machines > Machines collection > Get Machines"}}))
        msg = json.loads(self.conn.readline())
        expect = \
            {
                "event": "afterEach",
                "data":
                {
                    "name": "Machines > Machines collection > Get Machines",
                    "hooks_modifications":
                    [
                        "multi hook for single",
                        "multi hook for single",
                    ],
                    "extra": "extra item",
                }
            }
        self.assertDictEqual(msg, expect)

    def test_output(self):
        out = self.output.getvalue()
        for s in ['multi hook for all',
                  'multi hook for single',
                  'multi hook with extra item']:
            self.assertNotEqual(out.find(s), -1)


@hooks.after_all
@hooks.before_all
@hooks.before_each
@hooks.after_each
@hooks.before_validation('Machines > Machines collection > Get Machines')
@hooks.before("Machines > Machines collection > Get Machines")
@hooks.after("Machines > Machines collection > Get Machines")
def multi_hook_test(trans):
    if isinstance(trans, list):
        if 'hooks_modifications' not in trans[0]:
            trans[0]['hooks_modifications'] = []
        trans[0]['hooks_modifications'].append("multi hook for all")
        print('multi hook for all')
    else:
        if 'hooks_modifications' not in trans:
            trans['hooks_modifications'] = []
        trans['hooks_modifications'].append("multi hook for single")
        print('multi hook for single')
        if trans['name'] == 'Machines > Machines collection > Get Machines':
            trans['extra'] = 'extra item'
            print("multi hook with extra item")


if __name__ == '__main__':
    try:
        unittest.main()
    except Exception as e:
        exit(-1)
