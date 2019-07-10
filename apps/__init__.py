import logging
import logging.config
from flask import Flask

import werkzeug.utils
from apps.middlewares import log

def register_middlewares(new_app, path, middlewares):
    for name in middlewares:
        m = werkzeug.utils.import_string('%s.%s' % (path, name))
        before_request = getattr(m, 'before_request', None)
        after_request = getattr(m, 'after_request', None)
        teardown_request = getattr(m, 'teardown_request', None)
        if before_request:
            new_app.before_request(before_request)
        if after_request:
            new_app.after_request(after_request)
        if teardown_request:
            new_app.teardown_request(teardown_request)
    return new_app

def create_app():
    app = Flask(__name__)
    from apps.views import user, business

    app.register_blueprint(user.bp)
    app.register_blueprint(business.bb)

    # init log config
    logging.config.fileConfig("logger.conf", disable_existing_loggers=False)

    register_middlewares(app, 'apps.middlewares', [
        "log",
    ])

    return app

app = create_app()





