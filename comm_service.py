from PyQt5.QtCore import (QObject, QThread, QBasicTimer, pyqtSignal)
import serial
from serial.tools import list_ports
from log_module import get_module_logger, autolog

logger = get_module_logger(__name__)


class PortCheckThread:
    def __init__(self, controller):
        super().__init__()
        logger.debug(autolog())
        self.controller = controller
        self.list_ports = list()
        self.list_ports_prev = list()
        self.timer = PortUpdateTimer(self.step)

    def step(self):
        logger.debug(autolog())
        self.list_ports = sorted([port.name for port in list_ports.comports()])
        if self.list_ports != self.list_ports_prev:
            self.controller.portUpdated(self.list_ports)
            logger.debug('port updated: {0}'.format(self.list_ports))
        self.list_ports_prev = self.list_ports

    def start(self):
        logger.debug(autolog())
        self.list_ports = sorted([port.name for port in list_ports.comports()])
        self.controller.portUpdated(self.list_ports)
        logger.debug('port updated: {0}'.format(self.list_ports))
        self.list_ports_prev = self.list_ports

        self.timer.start(3000)

    def stop(self):
        logger.debug(autolog())
        self.timer.stop()


class PortUpdateTimer(QObject):
    def __init__(self, handler):
        super().__init__()
        logger.debug(autolog())
        self.handler = handler
        self.timer = QBasicTimer()

    def start(self, interval):
        logger.debug(autolog())
        self.timer.start(interval, self)

    def stop(self):
        logger.debug(autolog())
        self.timer.stop()

    def timerEvent(self, event):
        logger.debug(autolog())
        if event.timerId() == self.timer.timerId():
            self.handler()


class CommThread(QObject):
    def __init__(self, controller):
        super().__init__()
        logger.debug(autolog())
        self.controller = controller

    def startCommunication(self, port_name):
        logger.debug(autolog())
        self.worker = CommWorker(port_name)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.eventRecvText.connect(self.commReceived)
        self.worker.eventDisconnectPort.connect(self.commDisconnected)
        self.thread.start()

    def commReceived(self, text):
        logger.debug(autolog())
        self.controller.commReceived(text)

    def commDisconnected(self):
        logger.debug(autolog())
        self.thread.quit()
        self.controller.commDisconnected()


class CommWorker(QObject):
    eventRecvText = pyqtSignal(bytes)
    eventDisconnectPort = pyqtSignal()

    def __init__(self, port_name):
        super().__init__()
        logger.debug(autolog())
        self.ser = serial.Serial(port_name, 115200, timeout=None)

    def run(self):
        logger.debug(autolog())
        try:
            while True:
                self.line = self.ser.readline()
                logger.debug('ser.readline: {0}'.format(self.line))
                self.eventRecvText.emit(self.line)
        except serial.serialutil.SerialException:
            logger.debug('ser.SerialException')
            self.eventDisconnectPort.emit()

    def send(self, text):
        text += '\n'
        self.ser.write(text.encode())
