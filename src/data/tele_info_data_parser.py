from typing import Match

from src.data.tele_info_data import TeleInfoData
import re


class TeleInfoDataParser:
    TELE_INFO_MSG_REGEX = r'(\w+)\s+(\S+)\s+(.)'

    def __init__(self, frames_: list[list[str]]):
        self.frames = frames_

    def parse(self) -> list[TeleInfoData]:
        tele_info_data_objects = []
        for frame in self.frames:
            tele_info_data_objects.append(self._parse_frame(frame))
        return tele_info_data_objects

    def _parse_frame(self, frame) -> TeleInfoData:
        tele_info_entries_as_dict = {}
        for entry in frame:
            if self._validate_entry(entry):
                teleinfo_tag, value = self._extract_value_from_entry(entry)
                tele_info_entries_as_dict[teleinfo_tag] = value
            else:
                raise ValueError(f'Invalid teleinfo message: {entry}')

        return TeleInfoData(tele_info_entries_as_dict)

    @staticmethod
    def _validate_entry(entry: str) -> Match[str] | None:
        return re.match(TeleInfoDataParser.TELE_INFO_MSG_REGEX, entry)

    @staticmethod
    def _extract_value_from_entry(entry: str) -> (str, str):
        matches = re.search(TeleInfoDataParser.TELE_INFO_MSG_REGEX, entry)
        return matches.group(1), matches.group(2)
