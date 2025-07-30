# -*- coding: utf-8 -*-

import os
import six
from opinionated_configparser import OpinionatedConfigParser

if six.PY2:
    UNICODE = u"ééé"
else:
    UNICODE = "ééé"

TEST_DICT1 = {
    "section1": {
        "key1": "value1{{ENV_VAR}}",
        "key2": "{{UNICODE_ENV_VAR}}"
    }
}


def test_env1():
    if "ENV_VAR" in os.environ:
        del os.environ["ENV_VAR"]
    x = OpinionatedConfigParser()
    x.read_dict(TEST_DICT1)
    assert x.get("section1", "key1") == "value1"


def test_env2():
    os.environ["ENV_VAR"] = "foo"
    x = OpinionatedConfigParser()
    x.read_dict(TEST_DICT1)
    assert x.get("section1", "key1") == "value1foo"
    del os.environ["ENV_VAR"]


def test_env3():
    if six.PY2:
        os.environ["UNICODE_ENV_VAR"] = UNICODE.encode("utf8")
    else:
        os.environ["UNICODE_ENV_VAR"] = UNICODE
    x = OpinionatedConfigParser()
    x.read_dict(TEST_DICT1)
    assert x.get("section1", "key2") == UNICODE
    del os.environ["UNICODE_ENV_VAR"]
