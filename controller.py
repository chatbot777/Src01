import inspect
from log_module import get_module_logger

logger = get_module_logger(__name__)


def autolog():
    func = inspect.currentframe().f_back.f_code
    obj = inspect.currentframe().f_back.f_locals['self']
    return '{0:10}, {1}()'.format(obj.__class__.__name__, func.co_name)


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
