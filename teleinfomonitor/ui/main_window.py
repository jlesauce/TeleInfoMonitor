import sys

from PyQt6.QtWidgets import QApplication, QMainWindow

from teleinfomonitor.model.model import Model
from teleinfomonitor.ui.current_plot_view import CurrentPlotView


class MainWindow:

    def __init__(self, model: Model):
        self.model = model
        self.application = QApplication(sys.argv[:1])
        self.main_window = QMainWindow()
        self.current_plot_view = CurrentPlotView(self.model)
        self._create_ui()

    def start_application(self):
        self.main_window.show()
        self.application.exec()

    def update_current_plot_view(self):
        self.current_plot_view.update_plot()

    def _create_ui(self):
        self.main_window.setWindowTitle(self.model.application_name)
        self.main_window.resize(500, 500)
        self._center()

        self.current_plot_view.create_ui()
        self.main_window.setCentralWidget(self.current_plot_view)

    def _center(self):
        frame_geometry = self.main_window.frameGeometry()
        screen = self.application.primaryScreen()
        center_point = screen.availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.main_window.move(frame_geometry.topLeft())
