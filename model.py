from log_module import get_module_logger, autolog

logger = get_module_logger(__name__)


class Model:
    def __init__(self):
        logger.debug(autolog())
        self.line = ''
        self.text = ''

    def returnPressed(self, text):
        logger.debug(autolog())
        self.text += text + '\n'
