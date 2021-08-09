from log_module import get_module_logger, autolog

logger = get_module_logger(__name__)


class Model:
    def __init__(self):
        logger.debug(autolog())
        self.line = ''
        self.text = ''
        self.portselect_visible = True

    def portUpdated(self, list_ports):
        self.list_ports = list_ports

    def commReceived(self, text):
        logger.debug(autolog())
        self.text += text.decode() + '\n'

    def commConnected(self):
        self.portselect_visible = False

    def commDisconnected(self):
        self.portselect_visible = True
