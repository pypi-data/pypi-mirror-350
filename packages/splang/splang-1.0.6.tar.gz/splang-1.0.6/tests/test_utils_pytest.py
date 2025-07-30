import pytest
from splang.utils import get_last_second, get_first_second, process_ms, get_first_ascii_character


def test_get_last_second_valid():
    assert get_last_second("5:32") == 2
    assert get_last_second("10:09") == 9
    with pytest.raises(ValueError):
        get_last_second("invalid")


def test_get_first_second_valid():
    assert get_first_second("5:32") == 3
    assert get_first_second("0:05") == 0
    with pytest.raises(ValueError):
        get_first_second("5")


def test_process_ms_rounding_and_format():
    assert process_ms(0) == "0:00"
    assert process_ms(500) == "0:01"
    assert process_ms(1000) == "0:01"
    assert process_ms(15500) == "0:16"
    assert process_ms(61500) == "1:02"
    assert process_ms(59999) == "1:00"


def test_get_first_ascii_character():
    assert get_first_ascii_character("hello") == "h"
    assert get_first_ascii_character("123!abc") == "1"
    # non-ascii characters should return inverted question mark
    assert get_first_ascii_character("¡¢£") == "¿"
    assert get_first_ascii_character("") == "¿"
