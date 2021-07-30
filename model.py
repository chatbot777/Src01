import inspect
from log_module import get_module_logger

logger = get_module_logger(__name__)


def autolog():
    func = inspect.currentframe().f_back.f_code
    obj = inspect.currentframe().f_back.f_locals['self']
    return '{0:10}, {1}()'.format(obj.__class__.__name__, func.co_name)


class Model:
    def __init__(self):
        logger.debug(autolog())
        self.line = ''
        self.text = ''

    def returnPressed(self, text):
        logger.debug(autolog())
        self.text += text + '\n'
