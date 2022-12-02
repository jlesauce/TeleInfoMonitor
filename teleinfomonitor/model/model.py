from PyQt6.QtCore import QSettings

from teleinfomonitor.model.tele_info_data import TeleInfoFrame


class Model:
    APPLICATION_NAME = 'TeleInfo Monitor'
    APPLICATION_SHORT_NAME = 'teleinfomonitor'

    def __init__(self):
        self.application_name = Model.APPLICATION_NAME
        self.tele_info_frames = []
        self.settings = QSettings(Model.APPLICATION_SHORT_NAME)
        self._init_settings()

    def set_tele_info_frames(self, tele_info_frames: list[TeleInfoFrame]):
        self.tele_info_frames = tele_info_frames

    def add_new_tele_info_frame(self, tele_info_frame: TeleInfoFrame):
        self.tele_info_frames.append(tele_info_frame)

    def _init_settings(self):
        self.settings.setValue('server/ip_address', '192.168.1.117')
        self.settings.setValue('server/port', 50007)
        self.settings.setValue('database/name', 'teleinfodb')
        self.settings.setValue('database/user', 'teleinfomonitor')
        self.settings.setValue('database/password', 'jacqueschirac')
        self.settings.setValue('database/port', 3306)
