import argparse
import logging
import os

from util.logger import configure_logger
from util.data_file_helpers import parse_data_file

APPLICATION_NAME = 'TeleInfo Monitor'
APPLICATION_SHORT_NAME = 'teleinfomonitor'

logger = logging.getLogger()


def main():
    configure_logger(log_file=f'{APPLICATION_SHORT_NAME}.log')
    args = _parse_arguments()

    logger.info(f'Start {APPLICATION_NAME}')

    if args.data_file:
        logger.info(f'data_file specified: {args.data_file}')
        parse_data_file(args.data_file)


def _parse_arguments():
    parser = _create_argument_parser()
    return parser.parse_args()


def _create_argument_parser():
    parser = argparse.ArgumentParser(
        description='Application used to monitor TeleInfo serial data from Enedis Linky meter equipment.')
    parser.add_argument('--data_file', metavar='FILE', type=lambda x: is_valid_file(parser, x),
                        help='File containing TeleInfo data.')
    return parser


def is_valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error('The file {} does not exist!'.format(arg))
    return arg


if __name__ == "__main__":
    main()
