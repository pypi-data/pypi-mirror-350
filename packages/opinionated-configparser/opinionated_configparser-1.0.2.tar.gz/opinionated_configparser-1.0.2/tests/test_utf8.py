# -*- coding: utf-8 -*-

import six
from opinionated_configparser import OpinionatedConfigParser


if six.PY2:
    UNICODE = u"ééé"
else:
    UNICODE = "ééé"

TEST_DICT1 = {
    "section1": {
        "key1": UNICODE
    }
}


def test_unicode():
    x = OpinionatedConfigParser()
    x.read_dict(TEST_DICT1)
    assert x.get("section1", "key1") == UNICODE
