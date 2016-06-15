# -*- coding: utf-8 -*-
#
#  Copyright (c) 2015, 2016 Apiary Czech Republic, s.r.o.
#  License: MIT
#
from __future__ import print_function
import json
import sys
import os
import glob
import imp

try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer

__all__ = ['before_all',
           'after_all',
           'before_each',
           'before_each_validation',
           'after_each',
           'before_validation',
           'before',
           'after',
           'main',
           'shutdown',
           'HOST',
           'PORT',
           'MESSAGE_DELIMITER']

HOST = '127.0.0.1'
PORT = 61321
MESSAGE_DELIMITER = '\n'

BEFORE_ALL = 'BFA'
AFTER_ALL = 'AFA'
BEFORE_EACH = 'BFE'
AFTER_EACH = 'AFE'
BEFORE_EACH_VALIDATION = 'BFE_VAL'
BEFORE_VALIDATION = 'BF_VAL'
BEFORE = 'BF'
AFTER = 'AF'

hooks = None
server = None

class Hooks(object):
    def __init__(self):
        self._before_all = []
        self._after_all = []
        self._before_each = []
        self._before_each_validation = []
        self._after_each = []
        self._before_validation = {}
        self._before = {}
        self._after = {}


class HookHandler(SocketServer.StreamRequestHandler):
    """
    Main hook events handler, upon reception executes the correct
    hooks based on the incoming event. Keeps the connection open until
    the socket is closed by peer.
    """
    def handle(self):
        global hooks
        try:
            while True:
                if sys.version_info[0] > 2:
                    msg = json.loads(self.rfile.readline().
                                     decode('utf-8').strip())
                else:
                    msg = json.loads(self.rfile.readline().strip())

                data = msg['data']
                if msg['event'] == "beforeAll":
                    [execute_and_flush(fn,data) for fn in hooks._before_all]

                if msg['event'] == "afterAll":
                    [execute_and_flush(fn,data) for fn in hooks._after_all]

                if msg['event'] == "beforeEachValidation":
                    [execute_and_flush(fn,data) for fn in hooks._before_each_validation]
                    if data.get('name') in hooks._before_validation:
                        [execute_and_flush(fn,data) for fn in
                         hooks._before_validation[data.get('name')]]

                if msg['event'] == "beforeEach":
                    [execute_and_flush(fn,data) for fn in hooks._before_each]
                    if data.get('name') in hooks._before:
                        [execute_and_flush(fn,data) for fn in
                         hooks._before[data.get('name')]]

                if msg['event'] == "afterEach":
                    if data.get('name') in hooks._after:
                        [execute_and_flush(fn,data)for fn in
                         hooks._after[data.get('name')]]
                    [execute_and_flush(fn,data) for fn in hooks._after_each]

                msg = json.dumps(msg) + MESSAGE_DELIMITER
                if sys.version_info[0] > 2:
                    self.wfile.write(msg.encode('utf-8'))
                else:
                    self.wfile.write(msg)
        except ValueError:
            print("\nConnection closed\n", file=sys.stderr)

def execute_and_flush(fn,data):
    fn(data)
    sys.stdout.flush()

def add_named_hook(obj, hook, name):
    obj.setdefault(name, [])
    obj[name].append(hook)

#Added to address issue 11  
def check_dredd_hook_and_dredd_name_append(fn,text,name=None):
    if hasattr(fn,'dredd_hook'):
        fn.dredd_hook.append(text)
    else:
        fn.dredd_hook = []
        fn.dredd_hook.append(text)
    if hasattr(fn,'dredd_name'):
        fn.dredd_name.append(name)
    else:
        fn.dredd_name = []
        fn.dredd_name.append(name)
    return fn

def load_hook_files(pathname):
    """
     Loads files either defined as a glob or a single file path.
    """
    global hooks

    fsglob = glob.iglob(pathname)
    for path in fsglob:
        module = imp.load_source(os.path.basename(path), path)
        for name in dir(module):
            print(name)
            obj = getattr(module, name)
            if hasattr(obj, 'dredd_hook') and callable(obj):
                hookz = getattr(obj, 'dredd_hook')
                namez = getattr(obj, 'dredd_name')
                for i,hook in enumerate(hookz):
                    if hook == BEFORE_ALL:
                        hooks._before_all.append(obj)
                    if hook == AFTER_ALL:
                        hooks._after_all.append(obj)
                    if hook == BEFORE_EACH:
                        hooks._before_each.append(obj)
                    if hook == AFTER_EACH:
                        hooks._after_each.append(obj)
                    if hook == BEFORE_EACH_VALIDATION:
                        hooks._before_each_validation.append(obj)
                    if hook == BEFORE_VALIDATION:
                        add_named_hook(hooks._before_validation,
                                       obj,
                                       namez[i])
                    if hook == BEFORE:
                        add_named_hook(hooks._before,
                                       obj,
                                       namez[i])
                    if hook == AFTER:
                        add_named_hook(hooks._after,
                                       obj,
                                       namez[i])


# Hook decorators
# Each adds a function property so that the hook loader
# can easily distinguish each of them
def before_all(f):
    return check_dredd_hook_and_dredd_name_append(f,BEFORE_ALL)


def after_all(f):
    return check_dredd_hook_and_dredd_name_append(f,AFTER_ALL)


def before_each(f):
    return check_dredd_hook_and_dredd_name_append(f,BEFORE_EACH)


def before_each_validation(f):
    return check_dredd_hook_and_dredd_name_append(f,BEFORE_EACH_VALIDATION)


def after_each(f):
    f.dredd_hook = AFTER_EACH
    return check_dredd_hook_and_dredd_name_append(f,AFTER_EACH)


def before_validation(name):
    def decorator(f):
        return check_dredd_hook_and_dredd_name_append(f,BEFORE_VALIDATION,name)
    return decorator


def before(name):
    def decorator(f):
        return check_dredd_hook_and_dredd_name_append(f,BEFORE,name)
    return decorator


def after(name):
    def decorator(f):
        return check_dredd_hook_and_dredd_name_append(f,AFTER,name)
    return decorator


def shutdown():
    global server
    server.shutdown()
    print("Dredd Python hooks handler shutdown")
    sys.stdout.flush()


def main(args):
    global server
    global hooks
    hooks = Hooks()
    # Load hook files
    for a in args:
        load_hook_files(a)

    try:
        # Start the server
        SocketServer.TCPServer.allow_reuse_address = True
        server = SocketServer.TCPServer((HOST, PORT), HookHandler)
        print('Starting Dredd Python hooks handler')
        sys.stdout.flush()
        server.serve_forever()
    except KeyboardInterrupt:
        shutdown()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.stderr.flush()
        raise
