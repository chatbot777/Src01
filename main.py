from PyQt5.QtWidgets import QApplication
from model import Model
from view import View
from controller import Controller


def main():
    app = QApplication([])
    model = Model()
    view = View(model)
    controller = Controller(view, model, app)  # noqa F841

    view.showWindow()
    app.exec_()


if __name__ == '__main__':
    main()
