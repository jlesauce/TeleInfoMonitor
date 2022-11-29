import logging

from PyQt6.QtCore import QSettings

from teleinfomonitor.io.socket_client import SocketClient
from teleinfomonitor.model.model import Model
from teleinfomonitor.model.tele_info_data import TeleInfoFrame
from teleinfomonitor.ui.main_window import MainWindow

logger = logging.getLogger(__name__)


class Controller:

    def __init__(self, model: Model, view: MainWindow):
        self.model = model
        self.view = view
        self.tele_info_transmission_client = None

    def start_application(self):
        self.view.add_event_listener(self._on_close_application_event, MainWindow.EVENT_ID_ON_CLOSE_BUTTON_CLICKED)
        self.view.add_event_listener(self._on_connect_button_clicked, MainWindow.EVENT_ID_ON_CONNECT_BUTTON_CLICKED)
        self.view.add_event_listener(self._on_disconnect_button_clicked,
                                     MainWindow.EVENT_ID_ON_DISCONNECT_BUTTON_CLICKED)
        self.view.start_application()

    def _start_tele_info_transmission_from_server(self):
        if not self.tele_info_transmission_client:
            logger.info('Start reception of TeleInfo data from remote server')

            try:
                settings: QSettings = self.model.settings
                self.tele_info_transmission_client = SocketClient(host_name=settings.value('server/ip_address'),
                                                                  port=settings.value('server/port'))
                self.tele_info_transmission_client.subscribe_to_new_messages(self._on_new_tele_info_data_received)
                self.tele_info_transmission_client.start_client()
            except Exception as e:
                logger.error(e)
        else:
            logger.warning('Reception of TeleInfo data is already running')

    def _stop_tele_info_transmission_from_server(self):
        if self.tele_info_transmission_client:
            logger.info('Stop reception of TeleInfo data from remote server')
            self.tele_info_transmission_client.stop_client()
            self.tele_info_transmission_client = None

    def _on_new_tele_info_data_received(self, message):
        try:
            tele_info_frame = TeleInfoFrame(message)
            logger.info(
                f'Received new TeleInfo frame: {tele_info_frame.timestamp}: '
                f'IINST={tele_info_frame.instantaneous_intensity_in_a}')

            self.model.add_new_tele_info_frame(tele_info_frame)
            self.view.update_current_plot_view()
        except KeyError as e:
            logger.error(f'Invalid TeleInfo frame received: {e}')

    def _on_close_application_event(self, _):
        logger.info('Close application')
        self._stop_tele_info_transmission_from_server()

    def _on_connect_button_clicked(self):
        self._start_tele_info_transmission_from_server()

    def _on_disconnect_button_clicked(self):
        self._stop_tele_info_transmission_from_server()
