import sys
import os
import jinja2

if sys.version_info[:2] < (3, 5):
    # pylint: disable=E0401
    from backports import configparser
else:
    # pylint: disable=E0401
    import configparser


IS_PYTHON_2 = sys.version_info < (3, 0)


def get_real_option(option):
    if "[" not in option:
        return option
    if not option.endswith("]"):
        return option
    return option.split("[", 1)[0]


def get_default_configuration_name():
    return os.environ.get("MFCONFIG", "GENERIC").lower()


def get_variant(option):
    if "[" not in option or "]" not in option:
        return None
    if not option.endswith("]"):
        return None
    tmp = option.split("[", 1)[1][:-1]
    if len(tmp) == 0:
        return None
    return tmp.lower()


def get_score(variant, configuration_name):
    if variant == configuration_name:
        return sys.maxsize
    if variant is None:
        return 0.5
    tmp = configuration_name.split("_")
    if len(tmp) > 1:
        for i in range(len(tmp) - 1, 0, -1):
            tmp2 = "_".join(tmp[0:i])
            if variant == tmp2:
                return i
    return 0


class Jinja2Interpolation(configparser.Interpolation):

    def __init__(self, jinja2_context, **template_kwargs):
        if "undefined" not in template_kwargs:
            template_kwargs["undefined"] = jinja2.Undefined
        self.__template_kwargs = template_kwargs
        self.__jinja2_context = jinja2_context
        configparser.Interpolation.__init__(self)

    def before_get(self, parser, section, option, value, defaults):
        template = jinja2.Template(value, **self.__template_kwargs)
        return template.render(self.__jinja2_context)


class OpinionatedConfigParser(configparser.ConfigParser):
    def __init__(
        self,
        configuration_name=None,
        ignore_sections_starting_with="_",
        *args,
        **kwargs
    ):
        if configuration_name is not None:
            self.configuration_name = configuration_name.lower()
        else:
            self.configuration_name = get_default_configuration_name()
        if "default_section" in kwargs:
            # we can't use configparser default_section feature
            # so we will emulate later in the code
            self.__default_section = kwargs["default_section"]
        else:
            self.__default_section = None
        kwargs["default_section"] = None
        if "interpolation" not in kwargs:
            if IS_PYTHON_2:
                tmp = {}
                for x, y in os.environ.items():
                    try:
                        tmp[x] = y.decode('utf8')
                    except Exception:
                        print(x)
                        # probably a unicode error
                        pass
                kwargs["interpolation"] = Jinja2Interpolation(tmp)
            else:
                kwargs["interpolation"] = Jinja2Interpolation(os.environ)
        self.ignore_sections_starting_with = ignore_sections_starting_with
        configparser.ConfigParser.__init__(self, *args, **kwargs)

    def read(self, *args, **kwargs):
        tmp = configparser.ConfigParser.read(self, *args, **kwargs)
        self._resolve_variant()
        return tmp

    def read_dict(self, *args, **kwargs):
        tmp = configparser.ConfigParser.read_dict(self, *args, **kwargs)
        self._resolve_variant()
        return tmp

    def read_string(self, *args, **kwargs):
        tmp = configparser.ConfigParser.read_string(self, *args, **kwargs)
        self._resolve_variant()
        return tmp

    def read_file(self, *args, **kwargs):
        tmp = configparser.ConfigParser.read_file(self, *args, **kwargs)
        self._resolve_variant()
        return tmp

    def _resolve_variant(self):
        def deal_with_option(tmp, read_section, write_section, option):
            real_option = get_real_option(option)
            variant = get_variant(option)
            score = get_score(variant, self.configuration_name)
            if score == 0:
                return
            if real_option in tmp[write_section]:
                if score <= tmp[write_section][real_option][0]:
                    # not better score
                    return
            value = self.get(read_section, option)
            tmp[write_section][real_option] = (score, value)

        has_default = (
            self.__default_section is not None
            and self.__default_section in self.sections()
        )
        # first pass
        tmp = {}
        for section in self.sections():
            tmp[section] = {}
            for option in self.options(section):
                deal_with_option(tmp, section, section, option)
            if has_default:
                for option in self.options(self.__default_section):
                    deal_with_option(
                        tmp, self.__default_section, section, option
                    )
        # clear
        self.clear()
        # second pass
        for section in tmp.keys():
            if self.ignore_sections_starting_with and section.startswith(
                self.ignore_sections_starting_with
            ):
                continue
            for real_option in tmp[section].keys():
                value = tmp[section][real_option][1]
                if not self.has_section(section):
                    self.add_section(section)
                self.set(section, real_option, value)
