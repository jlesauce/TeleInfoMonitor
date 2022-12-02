import logging
from datetime import datetime
from typing import List

from PyQt6.QtCore import QSettings

from teleinfomonitor.database.database_client import DatabaseClient
from teleinfomonitor.model.model import Model
from teleinfomonitor.model.tele_info_data import TeleInfoFrame

logger = logging.getLogger(__name__)


class DatabaseController:

    def __init__(self, model: Model):
        self.settings: QSettings = model.settings

        database_name = self.settings.value('database/name')
        user = self.settings.value('database/user')
        password = self.settings.value('database/password')
        host = self.settings.value('server/ip_address')
        port = self.settings.value('database/port')

        self._database_client = DatabaseClient(database_name, user, password, host, port)

    def connect_to_database(self):
        self._update_database_client_settings(self.settings)
        logger.info(f'Connect to remote database {self._database_client.database_name}@{self._database_client.host}')
        self._database_client.connect()

    def is_database_connected(self):
        return self._database_client.is_connected()

    def retrieve_tele_info_frames_by_date(self, date: datetime) -> List[TeleInfoFrame]:
        sql_request = self._create_select_tele_info_frames_by_date_request(date)
        results = self._database_client.execute_sql_retrieve_request(sql_request)
        return [TeleInfoFrame.from_raw_data(result) for result in results]

    @staticmethod
    def _create_select_tele_info_frames_by_date_request(date):
        request = 'SELECT * FROM teleinfodb.teleinfoframes ' \
                  'WHERE (timestamp BETWEEN ' \
                  f"'{date} 00:00:00'" \
                  ' AND ' \
                  f"'{date} 23:59:59'" \
                  ')'
        return request

    def _update_database_client_settings(self, settings: QSettings):
        self._database_client.database_name = settings.value('database/name')
        self._database_client.user = settings.value('database/user')
        self._database_client.password = settings.value('database/password')
        self._database_client.host = settings.value('server/ip_address')
        self._database_client.port = settings.value('database/port')
