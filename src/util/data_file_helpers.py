import logging
from pathlib import Path

logger = logging.getLogger()


def parse_data_file(file_path: Path):
    logger.debug(f'Start parsing data file: {file_path}')
