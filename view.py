from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLineEdit, QTextEdit, QGridLayout, QAction, QFrame,
    QListView, QAbstractItemView
)
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QFont
from log_module import get_module_logger, autolog

logger = get_module_logger(__name__)


class View(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.debug(autolog())
        self.setFixedSize(640, 480)
        self.setFont(QFont('MeiryoKe_Gothic', 10))

    def register(self, model, controller):
        logger.debug(autolog())
        self.model = model
        self.controller = controller
        self.initUI()
        self.main_widget.register(self.model, self.controller)
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
        self.main_widget.updateUI()

    def showWindow(self):
        logger.debug(autolog())
        self.main_widget.show()
        self.show()

    def closeEvent(self, event):
        self.controller.windowClosed()


class MainWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        logger.debug(autolog())
        self.initUI()

    def register(self, model, controller):
        logger.debug(autolog())
        self.model = model
        self.controller = controller
        self.commdata_widget.register(self.model, self.controller)
        self.ptsel_bg_widget.register(self.model, self.controller)
        self.ptsel_fg_widget.register(self.model, self.controller)

    def initUI(self):
        logger.debug(autolog())
        self.commdata_widget = CommDataWidget(self)
        self.ptsel_bg_widget = PortSelectBgWidget(self)
        self.ptsel_fg_widget = PortSelectFgWidget(self)
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.addWidget(self.commdata_widget, 1, 0)
        self.grid.addWidget(self.ptsel_bg_widget, 1, 0)
        self.grid.addWidget(self.ptsel_fg_widget, 1, 0)
        self.setLayout(self.grid)

    def updateUI(self):
        logger.debug(autolog())
        self.commdata_widget.updateUI()
        self.ptsel_bg_widget.updateUI()
        self.ptsel_fg_widget.updateUI()


class CommDataWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        logger.debug(autolog())
        self.initUI()

    def register(self, model, controller):
        logger.debug(autolog())
        self.model = model
        self.controller = controller
        self.le.returnPressed.connect(lambda: self.controller.returnPressed(self.le.text()))
        # self.le.returnPressed.connect(self.controller.returnPressed)

    def initUI(self):
        logger.debug(autolog())
        self.le = QLineEdit(self)
        self.te = QTextEdit(self)
        self.te.setReadOnly(True)
        self.grid = QGridLayout()
        self.grid.addWidget(self.le, 1, 0)
        self.grid.addWidget(self.te, 2, 0)
        self.setLayout(self.grid)

    def updateUI(self):
        logger.debug(autolog())
        self.le.setText(self.model.line)
        self.te.setText(self.model.text)


class PortSelectBgWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        logger.debug(autolog())
        self.initUI()

    def register(self, model, controller):
        logger.debug(autolog())
        self.model = model
        self.controller = controller

    def initUI(self):
        logger.debug(autolog())

        self.fr = QFrame(self)
        self.fr.setStyleSheet("background-color: rgba(0, 0, 0, 105);")

        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.addWidget(self.fr, 1, 0)
        self.setLayout(self.grid)

    def updateUI(self):
        logger.debug(autolog())
        self.setVisible(self.model.portselect_visible)


class PortSelectFgWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        logger.debug(autolog())
        self.initUI()

    def register(self, model, controller):
        logger.debug(autolog())
        self.model = model
        self.controller = controller

    def initUI(self):
        logger.debug(autolog())

        self.lv = QListView(self)
        self.lv.setStyleSheet('''
            border-style: outset;
            border-width: 1px;
            border-color: black;
            ''')
        self.lv.setFixedSize(220, 160)
        self.lv.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lv.doubleClicked.connect(lambda p: self.controller.portSelected(p))

        self.grid = QGridLayout()
        self.grid.addWidget(self.lv, 1, 0)
        self.setLayout(self.grid)

    def updateUI(self):
        logger.debug(autolog())
        model = QStringListModel()
        model.setStringList(self.model.list_ports)
        self.lv.setModel(model)
        self.setVisible(self.model.portselect_visible)
