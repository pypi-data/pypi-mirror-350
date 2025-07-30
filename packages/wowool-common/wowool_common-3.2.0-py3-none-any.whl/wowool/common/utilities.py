import re


def strip_version(component_name: str) -> str:
    return re.sub("""(.*)@(?:dev\\d*|[0-9\\.]+[\\d]+)(\\.(?:language|dom))?""", "\\1\\2", component_name)


def get_lxware_version():
    from os import environ

    if "WOWOOL_LXWARE_VERSION" in environ:
        return environ["WOWOOL_LXWARE_VERSION"]
    return ""
