import argparse
import logging

import serial

from src.model import Model
from src.util.logger import configure_logger

logger = logging.getLogger(__name__)


def main():
    configure_logger(log_file=f'{Model.APPLICATION_SHORT_NAME}.log')
    args = _parse_arguments()

    logger.info(f'Start {Model.APPLICATION_NAME}')

    serial_port = serial.Serial('/dev/ttyAMA0', baudrate=1200, bytesize=7, timeout=1,
                                stopbits=serial.STOPBITS_ONE)

    while True:
        # Read data out of the buffer until a carriage return / new line is found
        text = serial_port.readline().decode('Ascii')

        print(f'Reading: {text}')


def _parse_arguments():
    parser = _create_argument_parser()
    return parser.parse_args()


def _create_argument_parser():
    parser = argparse.ArgumentParser(description='Application used to read TeleInfo data frames from serial link '
                                                 'connected to Enedis Linky meter equipment.')

    return parser


if __name__ == "__main__":
    main()
