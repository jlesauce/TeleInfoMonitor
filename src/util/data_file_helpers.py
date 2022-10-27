import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def parse_data_file(file_path: Path) -> list[list[str]]:
    logger.debug(f'Start parsing data file: {file_path}')
    with open(file_path, mode='r') as data_file:
        return _create_teleinfo_frame_subset_arrays(data_file)


def _create_teleinfo_frame_subset_arrays(iterable) -> list[list[str]]:
    is_start_frame_detected = False
    frames = []
    frame = []
    for line in iterable:
        if line.startswith('ADCO'):
            is_start_frame_detected = True
            frame = [line]
        elif is_start_frame_detected:
            frame.append(line)
            if line.startswith('MOTDETAT'):
                is_start_frame_detected = False
                frames.append(frame)
    return frames
