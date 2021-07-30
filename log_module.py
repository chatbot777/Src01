import logging
import inspect


# from <modname> import get_module_logger
# logger = get_module_logger(__name__)
# http://joemphilips.com/post/python_logging/

def get_module_logger(modname):
    logger = logging.getLogger(modname)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(threadName)-10s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def autolog():
    func = inspect.currentframe().f_back.f_code
    obj = inspect.currentframe().f_back.f_locals['self']
    return '{0:20}, {1}()'.format(obj.__class__.__name__, func.co_name)
