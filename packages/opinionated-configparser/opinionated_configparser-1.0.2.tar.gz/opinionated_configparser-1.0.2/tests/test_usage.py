from opinionated_configparser import OpinionatedConfigParser


TEST_DICT1 = {
    "_common": {
        "key1[foo_bar_1]": "value6",
        "key3": "value7",
        "key4": "value8"
    },
    "section1": {
        "key1": "value1",
        "key1[fOo]": "value2",
        "key1[foo_bar]": "value3",
        "key2": "value4"
    },
    "section2": {
        "key3": "value5"
    },
    "section3": {
        "issue8[foo]bar": "foobar"
    }
}


def test_constructor():
    x = OpinionatedConfigParser()
    assert x is not None


def test_issue8():
    x = OpinionatedConfigParser()
    x.read_dict(TEST_DICT1)
    assert x.get("section3", "issue8[foo]bar") == "foobar"


def test_read_dict_without_inheritance():
    x = OpinionatedConfigParser(configuration_name="foo")
    x.read_dict(TEST_DICT1)
    assert x.get("section1", "key1") == "value2"
    assert x.get("section1", "key2") == "value4"
    assert x.get("section1", "key3", fallback=None) is None
    assert x.get("section1", "key4", fallback=None) is None
    assert x.get("section2", "key1", fallback=None) is None
    assert x.get("section2", "key3") == "value5"
    assert x.get("section2", "key4", fallback=None) is None


def test_read_dict_without_inheritance2():
    x = OpinionatedConfigParser(configuration_name="foo_foo_foo_foo")
    x.read_dict(TEST_DICT1)
    assert x.get("section1", "key1") == "value2"
    assert x.get("section1", "key2") == "value4"
    assert x.get("section1", "key3", fallback=None) is None
    assert x.get("section1", "key4", fallback=None) is None
    assert x.get("section2", "key1", fallback=None) is None
    assert x.get("section2", "key3") == "value5"
    assert x.get("section2", "key4", fallback=None) is None


def test_read_dict_with_inheritance():
    x = OpinionatedConfigParser(configuration_name="foo",
                                default_section="_common")
    x.read_dict(TEST_DICT1)
    assert x.get("section1", "key1") == "value2"
    assert x.get("section1", "key2") == "value4"
    assert x.get("section1", "key3") == "value7"
    assert x.get("section1", "key4") == "value8"
    assert x.get("section2", "key1", fallback=None) is None
    assert x.get("section2", "key3") == "value5"
    assert x.get("section1", "key4") == "value8"
    assert x.get("_common", "key3", fallback=None) is None


def test_read_dict_with_inheritance2():
    x = OpinionatedConfigParser(configuration_name="foo_bar_1",
                                default_section="_common")
    x.read_dict(TEST_DICT1)
    assert x.get("section1", "key1") == "value6"
    assert x.get("section1", "key2") == "value4"
    assert x.get("section1", "key3") == "value7"
    assert x.get("section1", "key4") == "value8"
    assert x.get("section2", "key1") == "value6"
    assert x.get("section2", "key3") == "value5"
    assert x.get("section1", "key4") == "value8"
    assert x.get("_common", "key3", fallback=None) is None
