import argparse
import json
import logging
from datetime import datetime

import serial

from src.io.socket_server import SocketServer
from src.util.logger import configure_logger
from src.util.tele_info_helpers import is_valid_tele_info, extract_value_from_entry

APPLICATION_NAME = 'TeleInfo Monitor'
APPLICATION_SHORT_NAME = 'teleinfomonitor'

logger = logging.getLogger(__name__)

server = SocketServer(port=50007)


def main():
    configure_logger(log_file=f'{APPLICATION_SHORT_NAME}.log')
    parse_arguments()

    logger.info(f'Start {APPLICATION_NAME}')

    server.start_server()
    start_tele_info_reading(create_serial_port())


def start_tele_info_reading(serial_port):
    frame = list()
    first_frame_detected = False
    logger.info(f'Start TeleInfo reading...')

    while True:
        entry = read_tele_info_entry(serial_port)

        if is_valid_tele_info(entry):
            if is_start_of_frame(entry):
                first_frame_detected = True
                if len(frame):
                    collect_frame(frame)
                    frame.clear()

            if first_frame_detected:
                frame.append(entry)


def collect_frame(frame):
    frame_dict = {}
    for entry in frame:
        key, value = extract_value_from_entry(entry)
        frame_dict[key] = value

    json_entry_element = {
        'timestamp': get_current_timestamp(),
        'frame': frame_dict
    }
    json_object = json.dumps(json_entry_element, indent=4)
    logger.debug(f'Received TeleInfo frame: {flatten_json(json_object)}')

    send_data_to_connected_clients(json_object)


def flatten_json(json_str):
    return json_str.replace('\n', ' ').replace(' ', '')


def send_data_to_connected_clients(data: str):
    if server.is_server_created():
        server.send_data_to_connected_clients(data)


def get_current_timestamp():
    time_stamp = datetime.now().timestamp()
    return str(datetime.fromtimestamp(time_stamp))


def is_start_of_frame(entry):
    return entry.startswith('ADCO ')


def read_tele_info_entry(serial_port):
    # Read data out of the buffer until a carriage return / new line is found
    return serial_port.readline().decode('Ascii').strip()


def create_serial_port():
    serial_link_file = '/dev/ttyAMA0'
    logger.info(f'Open serial link {serial_link_file}')
    return serial.Serial('/dev/ttyAMA0', baudrate=1200, bytesize=7, timeout=1,
                         stopbits=serial.STOPBITS_ONE)


def parse_arguments():
    parser = create_argument_parser()
    return parser.parse_args()


def create_argument_parser():
    parser = argparse.ArgumentParser(description='Application used to read TeleInfo data frames from serial link '
                                                 'connected to Enedis Linky meter equipment.')

    return parser


if __name__ == "__main__":
    main()
