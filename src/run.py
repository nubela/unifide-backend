__author__ = 'kianwei'

from unifide_backend.unifide import app, _app_init
from werkzeug.serving import run_simple

if __name__ == '__main__':
    _app_init(app)
    run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=True)