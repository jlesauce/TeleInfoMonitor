import logging

from PyQt6.QtWidgets import QApplication, QMainWindow
from observable import Observable

from teleinfomonitor.model.model import Model
from teleinfomonitor.ui.current_plot_view import CurrentPlotView

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):

    def __init__(self, model: Model, application: QApplication):
        super().__init__()
        self.model = model
        self.application = application
        self.current_plot_view = CurrentPlotView(self.model)
        self._create_ui()
        self._observable = Observable()

    def start_application(self):
        self.show()

    def add_close_event_listener(self, function):
        self._observable.on("closeEvent", function)

    def closeEvent(self, event):
        logger.debug(f'Notify closeEvent received')
        self._observable.trigger("closeEvent", event)
        event.accept()

    def update_current_plot_view(self):
        self.current_plot_view.update_plot()

    def _create_ui(self):
        self.setWindowTitle(self.model.application_name)
        self.resize(500, 500)
        self._center()

        self.current_plot_view.create_ui()
        self.setCentralWidget(self.current_plot_view)

    def _center(self):
        frame_geometry = self.frameGeometry()
        screen = self.application.primaryScreen()
        center_point = screen.availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
