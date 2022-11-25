import logging
import socket
import threading

from observable import Observable

logger = logging.getLogger(__name__)


class SocketClient:
    OBSERVABLE_NEW_MASSAGE_EVENT = 'new_message'

    def __init__(self, host_name='192.168.1.117', port=50007):
        self.host_name = host_name
        self.port = port
        self._client_thread = threading.Thread(target=self._run_client)
        self._client_socket = None
        self._observable = Observable()

    def subscribe_to_new_messages(self, function):
        self._observable.on(self.OBSERVABLE_NEW_MASSAGE_EVENT, function)

    def _notify_new_message_incoming_to_subscribers(self, message):
        logger.debug(f'Notify {self.OBSERVABLE_NEW_MASSAGE_EVENT} event received')
        self._observable.trigger(self.OBSERVABLE_NEW_MASSAGE_EVENT, message)

    def start_client(self):
        self._create_client()
        self._client_thread.start()

    def stop_client(self):
        if self.is_client_created():
            logger.info(f'Disconnect client socket from server {self.host_name}:{self.port}')
            self._client_socket.close()
            self._client_socket = None

    def is_client_created(self):
        return True if self._client_socket else False

    def _create_client(self):
        logger.info(f'Create socket client on {self.host_name}:{self.port}')
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._client_socket.connect((self.host_name, self.port))
        except ConnectionRefusedError as e:
            logger.error(f'Failed to connect to server {self.host_name}:{self.port}: {e}')
            self._client_socket = None

    def _run_client(self):
        if not self.is_client_created():
            logger.warning('Could not start client thread: socket not created')
            return

        logger.info(f'Start listening from client socket...')
        size = 1024
        while self.is_client_created():
            try:
                data = self._client_socket.recv(size)
                if data:
                    msg = data.decode("utf-8")
                    self._notify_new_message_incoming_to_subscribers(msg)
                else:
                    logger.error('Something wrong detected: probably disconnected from server')
                    self.stop_client()
            except ConnectionAbortedError as e:
                logger.debug(f'Client socket disconnected: {e}')
            except OSError as e:
                if e.errno == 10038:
                    logger.debug(f'Client socket closed during reception: {e}')

        logger.info(f'Client thread stopped')
