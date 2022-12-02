import logging
from typing import List

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from observable import Observable

from teleinfomonitor.model.model import Model
from teleinfomonitor.model.tele_info_data import TeleInfoFrame
from teleinfomonitor.ui.design.ui_resource_file import UiResourceFile
from teleinfomonitor.ui.monthly_power_usage_tab_view import MonthlyPowerUsageTabView
from teleinfomonitor.ui.real_time_data_tab_view import RealTimeDataTabView
from teleinfomonitor.ui.settings_dialog import SettingsDialog

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    EVENT_ID_ON_CLOSE_BUTTON_CLICKED = 'close_event'

    def __init__(self, model: Model, application: QApplication):
        super().__init__()
        self._model = model
        self._application = application
        self._observable = Observable()

        uic.loadUi(UiResourceFile('main_window.ui').path, self)
        self._monthly_power_usage_tab_view = MonthlyPowerUsageTabView(self, self._model, self._observable)
        self._real_time_data_tab_view = RealTimeDataTabView(self, self._model, self._observable)
        self._init_ui()

    def start_application(self):
        self.show()

    def add_event_listener(self, function, event_id: str):
        self._observable.on(event_id, function)

    def closeEvent(self, event):
        logger.debug(f'Notify {self.EVENT_ID_ON_CLOSE_BUTTON_CLICKED} received')
        self._observable.trigger(self.EVENT_ID_ON_CLOSE_BUTTON_CLICKED, event)
        event.accept()

    def update_real_time_data_plot_view(self):
        self._real_time_data_tab_view.update_real_time_data_plot()

    def update_day_power_usage_plot_view(self, tele_info_frames: List[TeleInfoFrame]):
        self._monthly_power_usage_tab_view.update_day_power_usage_plot(tele_info_frames)

    def set_real_time_data_running_state(self):
        self._real_time_data_tab_view.set_connected_state()

    def set_real_time_data_stopped_state(self):
        self._real_time_data_tab_view.set_disconnected_state()

    def set_connected_to_database_state(self):
        self._monthly_power_usage_tab_view.set_connected_state()

    def set_disconnected_from_database_state(self):
        self._monthly_power_usage_tab_view.set_disconnected_state()

    def _init_ui(self):
        self.setWindowTitle(self._model.application_name)
        self._init_menu_actions()

    # noinspection PyUnresolvedReferences
    def _init_menu_actions(self):
        self.menu_action_settings.triggered.connect(self._on_click_settings_menu_item)
        self.menu_action_exit.triggered.connect(QApplication.instance().quit)

    def _on_click_settings_menu_item(self):
        logger.debug(f'Notify settings button clicked')
        SettingsDialog(self._model, self).exec()
