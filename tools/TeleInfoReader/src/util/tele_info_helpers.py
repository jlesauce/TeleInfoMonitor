import re

TELE_INFO_MSG_REGEX = r'(\w+)\s+(\S+)\s+(.)'


def is_valid_tele_info(entry: str):
    return re.match(TELE_INFO_MSG_REGEX, entry)


def extract_value_from_entry(entry: str) -> (str, str):
    matches = re.search(TELE_INFO_MSG_REGEX, entry)
    return matches.group(1), matches.group(2)
