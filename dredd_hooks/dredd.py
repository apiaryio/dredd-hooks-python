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
from functools import wraps

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
                    [fn(data) for fn in hooks._before_all]

                if msg['event'] == "afterAll":
                    [fn(data) for fn in hooks._after_all]

                if msg['event'] == "beforeEachValidation":
                    [fn(data) for fn in hooks._before_each_validation]
                    if data.get('name') in hooks._before_validation:
                        [fn(data) for fn in
                         hooks._before_validation[data.get('name')]]

                if msg['event'] == "beforeEach":
                    [fn(data) for fn in hooks._before_each]
                    if data.get('name') in hooks._before:
                        [fn(data) for fn in
                         hooks._before[data.get('name')]]

                if msg['event'] == "afterEach":
                    if data.get('name') in hooks._after:
                        [fn(data) for fn in
                         hooks._after[data.get('name')]]
                    [fn(data) for fn in hooks._after_each]

                msg = json.dumps(msg) + MESSAGE_DELIMITER
                if sys.version_info[0] > 2:
                    self.wfile.write(msg.encode('utf-8'))
                else:
                    self.wfile.write(msg)
        except ValueError:
            print("\nConnection closed\n", file=sys.stderr)


def add_named_hook(obj, hook, name):
    obj.setdefault(name, [])
    obj[name].append(hook)


def load_hook_files(pathname):
    """
     Loads files either defined as a glob or a single file path.
    """
    global hooks

    fsglob = glob.iglob(pathname)
    for path in fsglob:
        real_path = os.path.realpath(path)
        # Append hooks file directory to the sys.path so submodules can be
        # loaded too.
        if os.path.dirname(real_path) not in sys.path:
            sys.path.append(os.path.dirname(real_path))
        module = imp.load_source(os.path.basename(path), real_path)
        for name in dir(module):
            obj = getattr(module, name)
            if hasattr(obj, 'dredd_hooks') and callable(obj):
                func_hooks = getattr(obj, 'dredd_hooks')
                for hook, name in func_hooks:
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
                        add_named_hook(hooks._before_validation, obj, name)
                    if hook == BEFORE:
                        add_named_hook(hooks._before, obj, name)
                    if hook == AFTER:
                        add_named_hook(hooks._after, obj, name)


def flusher(func):
    if func in flusher.flushed:
        return flusher.flushed[func]

    @wraps(func)
    def call(*args, **kwargs):
        result = func(*args, **kwargs)
        sys.stderr.flush()
        sys.stdout.flush()
        return result
    flusher.flushed[func] = call
    return call

flusher.flushed = {}


def make_hook(func, kind, name=None):
    f = flusher(func)
    if not hasattr(f, 'dredd_hooks'):
        f.dredd_hooks = set()

    f.dredd_hooks.add((kind, name))
    return f


# Hook decorators
# Each adds a function property so that the hook loader
# can easily distinguish each of them
def before_all(f):
    return make_hook(f, BEFORE_ALL)


def after_all(f):
    return make_hook(f, AFTER_ALL)


def before_each(f):
    return make_hook(f, BEFORE_EACH)


def before_each_validation(f):
    return make_hook(f, BEFORE_EACH_VALIDATION)


def after_each(f):
    return make_hook(f, AFTER_EACH)


def before_validation(name):
    def decorator(f):
        return make_hook(f, BEFORE_VALIDATION, name)
    return decorator


def before(name):
    def decorator(f):
        return make_hook(f, BEFORE, name)
    return decorator


def after(name):
    def decorator(f):
        return make_hook(f, AFTER, name)
    return decorator


def shutdown():
    global server
    server.shutdown()
    server.server_close()
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
