import argparse
import logging
import os
from pathlib import Path

from teleinfomonitor.model.model import Model
from teleinfomonitor.model.tele_info_data import TeleInfoFrame
from teleinfomonitor.model.tele_info_data_parser import TeleInfoDataParser
from teleinfomonitor.ui.controller import Controller
from teleinfomonitor.util.data_file_helpers import parse_data_file
from teleinfomonitor.util.logger import configure_logger
from ui.main_window import MainWindow

logger = logging.getLogger(__name__)


def main():
    configure_logger(log_file=f'{Model.APPLICATION_SHORT_NAME}.log')
    args = _parse_arguments()

    app_model = Model()
    logger.info(f'Start {app_model.application_name}')

    if args.data_file:
        tele_info_frames = _parse_data_from_file(args.data_file)
        app_model.set_tele_info_frames(tele_info_frames)

    if args.gui:
        _create_ui(app_model)


def _parse_data_from_file(data_file: Path) -> list[TeleInfoFrame]:
    logger.info(f'data_file specified: {data_file}')
    frames = parse_data_file(data_file)
    data = TeleInfoDataParser(frames).parse()
    logger.debug(f'Found {len(data)} teleinfo frames in file {data_file}')
    return data


def _create_ui(model: Model):
    view = MainWindow(model)
    controller = Controller(model, view)
    controller.start_application()


def _parse_arguments():
    parser = _create_argument_parser()
    return parser.parse_args()


def _create_argument_parser():
    parser = argparse.ArgumentParser(
        description='Application used to monitor TeleInfo serial model from Enedis Linky meter equipment.')
    parser.add_argument('--gui', action='store_true', help='Start the graphical user interface')
    parser.add_argument('--data_file', metavar='FILE', type=lambda x: _is_valid_file(parser, x),
                        help='File containing TeleInfo model.')
    return parser


def _is_valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error('The file {} does not exist!'.format(arg))
    return arg


if __name__ == "__main__":
    main()
