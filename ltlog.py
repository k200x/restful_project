import logging
import logging.config
import datetime
import sys

on_off = True

def _log(*argl, **kwargs):
    _log_msg = (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))+" "
    _log_msg += sys._getframe().f_back.f_back.f_code.co_name + "  "
    for l in argl:
        if type(l) == tuple:
            ps = str(l)
        else:
            try:
                ps = "%r" % l
            except:
                try:
                    ps = str(l)
                except:
                    ps = 'ERROR LOG OBJECT'
        if type(l) == str:
            _log_msg += ps[1:-1] + ' '
        else:
            _log_msg += ps + ' '
    if len(kwargs) > 0:
        _log_msg += str(kwargs)
    return _log_msg

def info(*arg, **kw):
    if on_off:
        logging.getLogger("log_dev").critical(_log(*arg, **kw))






