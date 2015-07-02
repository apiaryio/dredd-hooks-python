from __future__ import print_function
import json, sys, os, glob, imp

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
MESSAGE_DELIMITER = "\n"

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
    Main hook events handler, upon recpetion executes the correct hook
    based on the incoming event
    """
    def handle(self):
        global hooks
        try:
            while 1:
                if sys.version_info[0] > 2:
                    msg = json.loads(self.rfile.readline().
                                      decode('utf-8').strip())
                else:
                    msg = json.loads(self.rfile.readline().strip())

                if msg['event'] == "beforeAll":
                    [f(msg['data']) for f in hooks._before_all]

                if msg['event'] == "afterAll":
                    [f(msg['data']) for f in hooks._after_all]

                if msg['event'] == "beforeValidation":
                    [f(msg['data']) for f in hooks._before_each_validation]
                    if msg['data']['name'] in hooks._before_validation:
                        hooks._before_validation[msg['data']['name']](msg['data'])

                if msg['event'] == "beforeEach":
                    [f(msg['data']) for f in hooks._before_each]
                    if msg['data']['name'] in hooks._before:
                        hooks._before[msg['data']['name']](msg['data'])

                if msg['event'] == "afterEach":
                    if msg['data']['name'] in hooks._after:
                        hooks._after[msg['data']['name']](msg['data'])
                    [f(msg['data']) for f in hooks._after_each]

                msg = json.dumps(msg) + MESSAGE_DELIMITER
                if sys.version_info[0] > 2:
                    self.wfile.write(msg.encode('utf-8'))
                else:
                    self.wfile.write(msg)
        except ValueError as e:
            print("\nConnection closed\n", file=sys.stderr)
            return
        except Exception as e:
            raise e

#Hook Loader
def load_hook_files(pathname):
    """
     Loads files either defined as a glob or a single file path.
    """
    global hooks
    hooks = Hooks()

    fsglob = glob.iglob(pathname)
    for path in fsglob:
        module = imp.load_source(os.path.basename(path), path)
        for name in dir(module):
            obj = getattr(module, name)
            if hasattr(obj, 'dredd_hook') and callable(obj):
                hook = getattr(obj, 'dredd_hook')
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
                    hooks._before_validation[getattr(obj,'dredd_name')] = obj
                if hook == BEFORE:
                    hooks._before[getattr(obj,'dredd_name')] = obj
                if hook == AFTER:
                    hooks._after[getattr(obj,'dredd_name')] = obj

# Hook decorators
# Each adds a function property so that the hook loader
# can easily distinguish each of them
def before_all(f):
    f.dredd_hook = BEFORE_ALL
    return f

def after_all(f):
    f.dredd_hook = AFTER_ALL
    return f

def before_each(f):
    f.dredd_hook = BEFORE_EACH
    return f

def before_each_validation(f):
    f.dredd_hook = BEFORE_EACH_VALIDATION
    return f

def after_each(f):
    f.dredd_hook = AFTER_EACH
    return f

def before_validation(name):
    def decorator(f):
        f.dredd_hook = BEFORE_VALIDATION
        f.dredd_name = name
        return f
    return decorator

def before(name):
    def decorator(f):
        f.dredd_hook = BEFORE
        f.dredd_name = name
        return f
    return decorator

def after(name):
    def decorator(f):
        f.dredd_hook = AFTER
        f.dredd_name = name
        return f
    return decorator


def shutdown():
    global server
    server.shutdown()

def main(args):
    global server
    #Load hook files
    for a in args:
        load_hook_files(a)
    # Start the server
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer((HOST, PORT), HookHandler)
    print('Dredd Python hooks handler is running', file=sys.stderr)
    server.serve_forever()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Not enough parameters", file=sys.stderr)
        exit(-1)
    main(sys.argv[1:])
