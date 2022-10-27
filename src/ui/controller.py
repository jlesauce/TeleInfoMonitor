import logging
import random

from PyQt6 import QtCore

from src.model.model import Model
from src.model.tele_info_data import TeleInfoFrame
from src.ui.main_window import MainWindow

logger = logging.getLogger(__name__)


class Controller:

    def __init__(self, model: Model, view: MainWindow):
        self.model = model
        self.view = view
        self.timer = QtCore.QTimer()

    def start_application(self):
        self.view.start_application()

    def start_fake_monitoring(self):
        logger.info('Start fake monitoring')
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.create_fake_tele_info_frame)
        self.timer.start()

    def create_fake_tele_info_frame(self):
        logger.debug('Timer notify: create_fake_tele_info_frame')
        random_frame = TeleInfoFrame()
        random_frame.instantaneous_intensity_in_a = random.randint(0, 10)
        self.model.add_new_tele_info_frame(random_frame)
        # FIXME Replace with Observable model mechanism
        self.view.update_current_plot_view()
