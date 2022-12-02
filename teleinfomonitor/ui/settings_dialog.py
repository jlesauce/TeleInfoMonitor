import logging

from PyQt6 import uic
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QDialog, QDialogButtonBox

from teleinfomonitor.model.model import Model
from teleinfomonitor.ui.design.ui_resource_file import UiResourceFile

logger = logging.getLogger(__name__)


class SettingsDialog(QDialog):
    EVENT_ID_ON_OK_BUTTON_CLICKED = 'ok_event'
    EVENT_ID_ON_APPLY_BUTTON_CLICKED = 'apply_event'
    EVENT_ID_ON_CANCEL_BUTTON_CLICKED = 'cancel_event'

    def __init__(self, model: Model, parent=None):
        super().__init__(parent)
        self.settings: QSettings = model.settings
        uic.loadUi(UiResourceFile('settings_dialog.ui').path, self)
        self._init_ui()

    # noinspection PyUnresolvedReferences
    def _init_ui(self):
        self.setWindowTitle('Settings')
        self.server_ip_address_text_editor.setText(self.settings.value('server/ip_address'))
        self.server_port_spinner.setValue(self.settings.value('server/port'))
        self.database_name_text_editor.setText(self.settings.value('database/name'))
        self.database_user_text_editor.setText(self.settings.value('database/user'))
        self.database_password_text_editor.setText(self.settings.value('database/password'))
        self.database_port_spinner.setValue(self.settings.value('database/port'))

        self._init_actions()
        self.adjustSize()

    # noinspection PyUnresolvedReferences
    def _init_actions(self):
        self.accepted.connect(self._on_click_ok_button)
        self.rejected.connect(self._on_click_cancel_button)
        apply_buttons = [button for button in self.ok_cancel_button_box.buttons() if
                         self.ok_cancel_button_box.buttonRole(button) is QDialogButtonBox.ButtonRole.ApplyRole]
        apply_buttons[0].clicked.connect(self._on_click_apply_button)

    # noinspection PyUnresolvedReferences
    def _update_model(self):
        self.settings.setValue('server/ip_address', self.server_ip_address_text_editor.text())
        self.settings.setValue('server/port', self.server_port_spinner.value())
        self.settings.setValue('database/name', self.database_name_text_editor.text())
        self.settings.setValue('database/user', self.database_user_text_editor.text())
        self.settings.setValue('database/password', self.database_password_text_editor.text())
        self.settings.setValue('database/port', self.database_port_spinner.value())

        new_settings_str = '\n'.join([f'{key}={self.settings.value(key)}' for key in self.settings.allKeys()])
        logger.debug(f'Update model with new settings:\n{new_settings_str}')

    def _on_click_ok_button(self):
        logger.debug(f'Notify {self.EVENT_ID_ON_OK_BUTTON_CLICKED} received')
        self._update_model()

    def _on_click_apply_button(self):
        logger.debug(f'Notify {self.EVENT_ID_ON_APPLY_BUTTON_CLICKED} received')
        self._update_model()

    def _on_click_cancel_button(self):
        logger.debug(f'Notify {self.EVENT_ID_ON_CANCEL_BUTTON_CLICKED} received')
