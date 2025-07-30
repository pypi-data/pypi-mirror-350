import sys
from opinionated_configparser import get_real_option, get_variant, get_score


def test_get_real_option():
    assert get_real_option("") == ""
    assert get_real_option("foo[bar]") == "foo"
    assert get_real_option("foo[bar_1]") == "foo"


def test_get_variant():
    assert get_variant("") is None
    assert get_variant("foo") is None
    assert get_variant("foo[") is None
    assert get_variant("foo[bar") is None
    assert get_variant("foo[bar]") == "bar"
    assert get_variant("foo[]") is None
    assert get_variant("foo[bar_1_2]") == "bar_1_2"


def test_get_score():
    assert get_score(None, "generic") > 0 and get_score(None, "generic") < 1
    assert get_score("foo", "generic") == 0
    assert get_score("foo", "foo") == sys.maxsize
    assert get_score("foo", "foo_bar") == 1
    assert get_score("foo_bar", "bar") == 0
    assert get_score("foo_bar", "foo_bar_1_2_3_4") == 2
