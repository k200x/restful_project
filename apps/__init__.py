import logging
import logging.config
from flask import Flask
# from apps import config
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



def t():
    app = Flask(__name__)
    from apps.views import user,test

    app.register_blueprint(user.bp)
    app.register_blueprint(test.bp)

    from settings.conf_onoff import on_off_dic
    conf = ""
    for key in on_off_dic:
        print(key)
        print(on_off_dic[key])
        if on_off_dic[key]:
            conf = key
            break
    if conf == "online":
        print("日志配置online")
        logging.config.fileConfig("logger.conf", disable_existing_loggers=False)
    elif conf == "dev":
        print("日志配置dev")
        logging.config.fileConfig("logger_dev.conf", disable_existing_loggers=False)
    elif conf == "test":
        print("日志配置test")
        logging.config.fileConfig("logger_test.conf", disable_existing_loggers=False)
    elif conf == "local":
        print("日志配置local")
        logging.config.fileConfig("logger_local.conf", disable_existing_loggers=False)

    register_middlewares(app, 'apps.middlewares', [
        "log",
    ])
    # config.init()
    return app

app = t()

