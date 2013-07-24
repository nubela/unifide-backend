#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from unifide_backend.unifide import app, _app_init

if __name__ == '__main__':
    _app_init(app)
    WSGIServer(app, bindAddress='./fcgi.sock').run()