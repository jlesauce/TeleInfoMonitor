from PyQt6 import uic
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QDialog

from teleinfomonitor.model.model import Model
from teleinfomonitor.ui.design.ui_resource_file import UiResourceFile


class SettingsDialog(QDialog):

    def __init__(self, model: Model, parent=None):
        super().__init__(parent)
        self.settings: QSettings = model.settings
        uic.loadUi(UiResourceFile('settings_dialog.ui').path, self)
        self._init_ui()

    # noinspection PyUnresolvedReferences
    def _init_ui(self):
        self.setWindowTitle('Settings')
        self.ip_address_text_editor.setText(self.settings.value('server/ip_address'))
        self.port_spinner.setValue(self.settings.value('server/port'))
        self.adjustSize()
