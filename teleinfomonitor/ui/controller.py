import logging

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
        self._start_tele_info_transmission_from_server()
        self.view.add_close_event_listener(self._on_application_stopped)
        self.view.start_application()

    def _start_tele_info_transmission_from_server(self):
        logger.info('Start reception of TeleInfo data from remote server')
        self.tele_info_transmission_client = SocketClient()
        self.tele_info_transmission_client.subscribe_to_new_messages(self._on_new_tele_info_data_received)
        self.tele_info_transmission_client.start_client()

    def _stop_tele_info_transmission_from_server(self):
        logger.info('Stop reception of TeleInfo data from remote server')
        self.tele_info_transmission_client.stop_client()

    def _on_application_stopped(self, event):
        self._stop_tele_info_transmission_from_server()

    def _on_new_tele_info_data_received(self, message):
        try:
            tele_info_frame = TeleInfoFrame(message)
            # logger.debug(f'Received new message: {tele_info_frame}')
            logger.info(
                f'Received new TeleInfo frame: {tele_info_frame.timestamp}: '
                f'IINST={tele_info_frame.instantaneous_intensity_in_a}')

            self.model.add_new_tele_info_frame(tele_info_frame)
            self.view.update_current_plot_view()
        except KeyError as e:
            logger.error(f'Invalid TeleInfo frame received: {e}')
