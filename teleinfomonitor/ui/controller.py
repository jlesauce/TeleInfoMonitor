import logging
from datetime import datetime
from typing import List

from PyQt6.QtCore import QSettings

from teleinfomonitor.io.socket_client import SocketClient
from teleinfomonitor.model.model import Model
from teleinfomonitor.model.tele_info_data import TeleInfoFrame
from teleinfomonitor.ui.main_window import MainWindow
from teleinfomonitor.ui.monthly_power_usage_tab_view import MonthlyPowerUsageTabView
from teleinfomonitor.ui.real_time_data_tab_view import RealTimeDataTabView

logger = logging.getLogger(__name__)


class Controller:

    def __init__(self, model: Model, view: MainWindow):
        self.model = model
        self.view = view
        self.tele_info_transmission_client = None

    def start_application(self):
        self._init_event_listeners()
        self.view.start_application()

    def close_application(self, _):
        logger.info('Close application')
        self.stop_tele_info_transmission_from_server()

    def start_tele_info_transmission_from_server(self):
        if not self.tele_info_transmission_client:
            logger.info('Start reception of TeleInfo data from remote server')

            try:
                settings: QSettings = self.model.settings
                self.tele_info_transmission_client = SocketClient(host_name=settings.value('server/ip_address'),
                                                                  port=settings.value('server/port'))
                self.tele_info_transmission_client.subscribe_to_new_messages(self._on_new_tele_info_data_received)
                self.tele_info_transmission_client.start_client()
                self.view.set_connected_state()
            except Exception as e:
                logger.error(e)
        else:
            logger.warning('Reception of TeleInfo data is already running')

    def stop_tele_info_transmission_from_server(self):
        if self.tele_info_transmission_client:
            logger.info('Stop reception of TeleInfo data from remote server')
            self.tele_info_transmission_client.stop_client()
            self.tele_info_transmission_client = None
            self.view.set_disconnected_state()

    def _init_event_listeners(self):
        self.view.add_event_listener(self.close_application, MainWindow.EVENT_ID_ON_CLOSE_BUTTON_CLICKED)
        self.view.add_event_listener(self.start_tele_info_transmission_from_server,
                                     RealTimeDataTabView.EVENT_ID_ON_START_TELEINFO_RECEPTION_BUTTON_CLICKED)
        self.view.add_event_listener(self.stop_tele_info_transmission_from_server,
                                     RealTimeDataTabView.EVENT_ID_ON_STOP_TELEINFO_RECEPTION_BUTTON_CLICKED)
        self.view.add_event_listener(self._on_day_power_usage_selected,
                                     MonthlyPowerUsageTabView.EVENT_ID_ON_CALENDAR_DAY_SELECTED)

    def _on_new_tele_info_data_received(self, message):
        try:
            tele_info_frame = TeleInfoFrame(message)
            logger.info(
                f'Received new TeleInfo frame: {tele_info_frame.timestamp}: '
                f'IINST={tele_info_frame.instantaneous_intensity_in_a}')

            self.model.add_new_tele_info_frame(tele_info_frame)
            self.view.update_real_time_data_plot_view()
        except KeyError as e:
            logger.error(f'Invalid TeleInfo frame received: {e}')

    def _on_day_power_usage_selected(self, selected_day: datetime):
        self.retrieve_tele_info_frames_by_date(selected_day)

    def retrieve_tele_info_frames_by_date(self, date: datetime) -> List[TeleInfoFrame]:
        logger.info(f'Retrieve TeleInfo frames by date: {date}')
        return list()
