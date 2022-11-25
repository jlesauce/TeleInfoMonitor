from teleinfomonitor.model.tele_info_data import TeleInfoFrame


class Model:
    APPLICATION_NAME = 'TeleInfo Monitor'
    APPLICATION_SHORT_NAME = 'teleinfomonitor'

    def __init__(self):
        self.application_name = Model.APPLICATION_NAME
        self.tele_info_frames = []

    def set_tele_info_frames(self, tele_info_frames: list[TeleInfoFrame]):
        self.tele_info_frames = tele_info_frames

    def add_new_tele_info_frame(self, tele_info_frame: TeleInfoFrame):
        self.tele_info_frames.append(tele_info_frame)
