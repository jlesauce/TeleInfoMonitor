import logging

import mariadb

from teleinfomonitor.database.database_error import DatabaseError

logger = logging.getLogger(__name__)


class DatabaseClient:

    def __init__(self, database_name: str, user: str, password: str, host='localhost', port=3306):
        self.database_name = database_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self._connection = None

    def connect(self):
        try:
            self._connection = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database_name
            )
            self._test_connection()
        except mariadb.Error as e:
            logger.error(f'Error connecting to MariaDB Platform: {e}')
            self._connection = None
            raise DatabaseError(e)

    def is_connected(self):
        return True if self._connection else False

    def execute_sql_commit_request(self, sql_request):
        try:
            logger.debug(f'Execute sql request: {sql_request}')
            cursor = self._connection.cursor()
            cursor.execute(sql_request)
            self._connection.commit()
        except mariadb.Error as e:
            logger.error(f'Error executing request to MariaDB Platform: {e}')
            raise e

    def execute_sql_retrieve_request(self, sql_request):
        try:
            logger.debug(f'Execute sql request: {sql_request}')
            cursor = self._connection.cursor()
            cursor.execute(sql_request)

            return cursor.fetchall()
        except mariadb.Error as e:
            logger.error(f'Error executing request to MariaDB Platform: {e}')
            raise e

    def _test_connection(self):
        results = self.execute_sql_retrieve_request('select count(*) row_count from teleinfoframes')

        if results:
            single_result = results[0][0]
            logger.debug(f'Successfully accessed to database: Number of frames detected: {single_result}')
        else:
            logger.error('Failed to access to database: connection test returned nothing')
