from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLineEdit, QTextEdit, QGridLayout, QAction
)
from PyQt5.QtGui import QFont
from log_module import get_module_logger, autolog

logger = get_module_logger(__name__)


class View(QMainWindow):
    def __init__(self, model):
        logger.debug(autolog())
        super().__init__()
        self.setFixedSize(640, 480)
        self.setFont(QFont('MeiryoKe_Gothic', 10))
        self.model = model

    def register(self, controller):
        logger.debug(autolog())
        self.controller = controller
        self.initUI()
        self.main_widget.register(self.controller)
        self.exit_action.triggered.connect(self.controller.quitPressed)

    def initUI(self):
        logger.debug(autolog())
        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)

        self.exit_action = QAction('&Exit', self)
        self.exit_action.setShortcut('Ctrl+Q')

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(self.exit_action)

    def updateUI(self):
        logger.debug(autolog())
        self.main_widget.updateUI(self.model.line, self.model.text)

    def showWindow(self):
        logger.debug(autolog())
        self.main_widget.show()
        self.show()


class MainWidget(QWidget):
    def __init__(self, parent):
        logger.debug(autolog())
        super(QWidget, self).__init__(parent)
        self.initUI()

    def register(self, controller):
        logger.debug(autolog())
        self.controller = controller
        self.le.returnPressed.connect(self.controller.returnPressed)

    def initUI(self):
        logger.debug(autolog())
        self.le = QLineEdit(self)
        self.te = QTextEdit(self)
        self.te.setReadOnly(True)
        self.grid = QGridLayout()
        self.grid.addWidget(self.le, 1, 0)
        self.grid.addWidget(self.te, 2, 0)
        self.setLayout(self.grid)

    def updateUI(self, line, text):
        logger.debug(autolog())
        self.le.setText(line)
        self.te.setText(text)
