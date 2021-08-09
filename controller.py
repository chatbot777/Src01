from PyQt5.QtWidgets import QApplication
from log_module import get_module_logger, autolog
from model import Model
from view import View
from comm_service import CommThread, PortCheckThread

logger = get_module_logger(__name__)


class Controller:
    def __init__(self, app: QApplication, view: View, model: Model):
        logger.debug(autolog())
        self.view = view
        self.model = model
        self.app = app
        self.portchk_thread = PortCheckThread(self)
        self.comm_thread = CommThread(self)

        self.view.register(self.model, self)
        self.portchk_thread.start()

    def portUpdated(self, list_ports):
        logger.debug(autolog())
        self.model.portUpdated(list_ports)
        self.view.updateUI()

    def portSelected(self, port):
        logger.debug(autolog())
        self.portchk_thread.stop()
        port_name = port.data()
        logger.debug('port selected: {0}'.format(port_name))
        self.model.commConnected()
        self.comm_thread.startCommunication(port_name)
        self.view.updateUI()

    def returnPressed(self, text):
        logger.debug(autolog())
        self.comm_thread.worker.send(text)
        self.view.updateUI()

    def commReceived(self, text):
        logger.debug(autolog())
        self.model.commReceived(text)
        self.view.updateUI()

    def commDisconnected(self):
        logger.debug(autolog())
        self.model.commDisconnected()
        self.portchk_thread.start()
        self.view.updateUI()

    def quitPressed(self):
        logger.debug(autolog())
        self.app.quit()

    def windowClosed(self):
        logger.debug(autolog())
