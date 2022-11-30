import logging

from PyQt6.QtWidgets import QMainWindow
from observable import Observable

from teleinfomonitor.model.model import Model
from teleinfomonitor.ui.power_usage_plot_view import PowerUsagePlotView

logger = logging.getLogger(__name__)


class RealTimeDataTabView:
    EVENT_ID_ON_START_TELEINFO_RECEPTION_BUTTON_CLICKED = 'start_teleinfo_reception_event'
    EVENT_ID_ON_STOP_TELEINFO_RECEPTION_BUTTON_CLICKED = 'stop_teleinfo_reception_event'

    def __init__(self, parent_window: QMainWindow, model: Model, listeners: Observable):
        self.parent = parent_window
        self.model = model
        self.listeners = listeners
        self.power_usage_plot_view = PowerUsagePlotView(self.model.tele_info_frames)

        self._init_ui()

    # noinspection PyUnresolvedReferences
    def _init_ui(self):
        self.parent.real_time_data_layout.addWidget(self.power_usage_plot_view)
        self._init_real_time_data_control_panel_actions()
        self.power_usage_plot_view.update_plot(self.model.tele_info_frames)
        self.set_disconnected_state()

    def update_real_time_data_plot(self):
        if self.power_usage_plot_view:
            self.power_usage_plot_view.update_plot(self.model.tele_info_frames)

    # noinspection PyUnresolvedReferences
    def set_connected_state(self):
        self.parent.teleinfo_reception_status_label.setText('Reception running')
        self.parent.teleinfo_reception_status_label.setStyleSheet("color: green")

    # noinspection PyUnresolvedReferences
    def set_disconnected_state(self):
        self.parent.teleinfo_reception_status_label.setText('Reception stopped')
        self.parent.teleinfo_reception_status_label.setStyleSheet("color: red")

    # noinspection PyUnresolvedReferences
    def _init_real_time_data_control_panel_actions(self):
        self.parent.start_teleinfo_reception_button.clicked.connect(self._on_click_start_teleinfo_reception_button)
        self.parent.stop_teleinfo_reception_button.clicked.connect(self._on_click_stop_teleinfo_reception_button)

    def _on_click_start_teleinfo_reception_button(self):
        logger.debug(f'Notify {self.EVENT_ID_ON_START_TELEINFO_RECEPTION_BUTTON_CLICKED} received')
        self.listeners.trigger(self.EVENT_ID_ON_START_TELEINFO_RECEPTION_BUTTON_CLICKED)

    def _on_click_stop_teleinfo_reception_button(self):
        logger.debug(f'Notify {self.EVENT_ID_ON_STOP_TELEINFO_RECEPTION_BUTTON_CLICKED} received')
        self.listeners.trigger(self.EVENT_ID_ON_STOP_TELEINFO_RECEPTION_BUTTON_CLICKED)
