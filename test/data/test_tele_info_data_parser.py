import pytest

from teleinfomonitor.model.tele_info_data_parser import TeleInfoDataParser
from teleinfomonitor.model.teleinfo_format_error import TeleInfoFormatError


def test_checksum_with_valid_input():
    input_str = 'IINST 010 J'
    assert TeleInfoDataParser.compute_checksum(input_str) == 'J'


def test_checksum_with_empty_input_should_raise_exception():
    with pytest.raises(ValueError) as error:
        TeleInfoDataParser.compute_checksum('')
    assert str(error.value) == 'Input string should not be empty'


def test_checksum_with_malformed_input_should_raise_exception():
    with pytest.raises(TeleInfoFormatError) as error:
        TeleInfoDataParser.compute_checksum('foo')
    assert str(error.value) == 'Input string does not match teleinfo format: foo'
