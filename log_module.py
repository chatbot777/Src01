import logging


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
