import logging

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar
from observable import Observable

from teleinfomonitor.model.model import Model
from teleinfomonitor.ui.current_plot_view import CurrentPlotView

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    EVENT_ID_ON_CLOSE_BUTTON_CLICKED = 'close_event'
    EVENT_ID_ON_CONNECT_BUTTON_CLICKED = 'connect_event'
    EVENT_ID_ON_DISCONNECT_BUTTON_CLICKED = 'disconnect_event'

    def __init__(self, model: Model, application: QApplication):
        super().__init__()
        self.model = model
        self.application = application
        self.current_plot_view = CurrentPlotView(self.model)
        self._observable = Observable()
        self._create_ui()

    def start_application(self):
        self.show()

    def add_event_listener(self, function, event_id: str):
        self._observable.on(event_id, function)

    def closeEvent(self, event):
        logger.debug(f'Notify {self.EVENT_ID_ON_CLOSE_BUTTON_CLICKED} received')
        self._observable.trigger(self.EVENT_ID_ON_CLOSE_BUTTON_CLICKED, event)
        event.accept()

    def update_current_plot_view(self):
        self.current_plot_view.update_plot()

    def _on_click_connect_menu_item(self):
        logger.debug(f'Notify {self.EVENT_ID_ON_CONNECT_BUTTON_CLICKED} received')
        self._observable.trigger(self.EVENT_ID_ON_CONNECT_BUTTON_CLICKED)

    def _on_click_disconnect_menu_item(self):
        logger.debug(f'Notify {self.EVENT_ID_ON_DISCONNECT_BUTTON_CLICKED} received')
        self._observable.trigger(self.EVENT_ID_ON_DISCONNECT_BUTTON_CLICKED)

    def _create_ui(self):
        self.setWindowTitle(self.model.application_name)
        self.resize(500, 500)
        self._center()

        self._create_menu_bar()

        self.current_plot_view.create_ui()
        self.setCentralWidget(self.current_plot_view)

    def _center(self):
        frame_geometry = self.frameGeometry()
        screen = self.application.primaryScreen()
        center_point = screen.availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def _create_menu_bar(self):
        self.statusBar()

        menu_bar = self.menuBar()
        self._create_file_menu(menu_bar)

    def _create_file_menu(self, menu_bar: QMenuBar):
        file_menu = menu_bar.addMenu('&File')

        file_menu.addAction(self._create_connect_action())
        file_menu.addAction(self._create_disconnect_action())
        file_menu.addAction(self._create_exit_action())

    # noinspection PyUnresolvedReferences
    def _create_connect_action(self) -> QAction:
        connect_action = QAction('&Connect', self)
        connect_action.setStatusTip('Connect to remote server')
        connect_action.triggered.connect(self._on_click_connect_menu_item)
        return connect_action

    # noinspection PyUnresolvedReferences
    def _create_disconnect_action(self) -> QAction:
        disconnect_action = QAction('&Disconnect', self)
        disconnect_action.setStatusTip('Disconnect from remote server')
        disconnect_action.triggered.connect(self._on_click_disconnect_menu_item)
        return disconnect_action

    # noinspection PyUnresolvedReferences
    def _create_exit_action(self) -> QAction:
        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QApplication.instance().quit)
        return exit_action
