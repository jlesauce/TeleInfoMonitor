import re
from typing import Match

from src.model.tele_info_data import TeleInfoFrame
from src.model.teleinfo_format_error import TeleInfoFormatError


class TeleInfoDataParser:
    TELE_INFO_MSG_REGEX = r'(\w+)\s+(\S+)\s+(.)'

    def __init__(self, frames_: list[list[str]]):
        self.frames = frames_

    def parse(self) -> list[TeleInfoFrame]:
        tele_info_data_objects = []
        for frame in self.frames:
            tele_info_data_objects.append(self._parse_frame(frame))
        return tele_info_data_objects

    def _parse_frame(self, frame) -> TeleInfoFrame:
        tele_info_entries_as_dict = {}
        for entry in frame:
            if self._validate_entry(entry):
                teleinfo_tag, value = self._extract_value_from_entry(entry)
                tele_info_entries_as_dict[teleinfo_tag] = value
            else:
                raise ValueError(f'Invalid teleinfo message: {entry}')

        return TeleInfoFrame(tele_info_entries_as_dict)

    @staticmethod
    def _validate_entry(entry: str) -> Match[str] | None:
        return re.match(TeleInfoDataParser.TELE_INFO_MSG_REGEX, entry)

    @staticmethod
    def _extract_value_from_entry(entry: str) -> (str, str):
        matches = re.search(TeleInfoDataParser.TELE_INFO_MSG_REGEX, entry)
        return matches.group(1), matches.group(2)

    @staticmethod
    def compute_checksum(entry: str):
        if not entry:
            raise ValueError('Input string should not be empty')
        if not TeleInfoDataParser._validate_entry(entry):
            raise TeleInfoFormatError(f'Input string does not match teleinfo format: {entry}')
        s1 = sum([ord(char) if char != ' ' else 0x9 for char in entry[:-1]])
        return chr((s1 & 0x3F) + 0x20)
