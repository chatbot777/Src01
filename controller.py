from log_module import get_module_logger, autolog

logger = get_module_logger(__name__)


class Controller:
    def __init__(self, view, model, app):
        logger.debug(autolog())
        self.view = view
        self.model = model
        self.app = app

        self.view.register(self)

    def returnPressed(self):
        logger.debug(autolog())
        self.model.returnPressed(self.view.main_widget.le.text())
        self.view.updateUI()

    def quitPressed(self):
        logger.debug(autolog())
        self.app.quit()
