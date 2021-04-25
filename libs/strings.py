import json


accepted_locales = ['en-us']
default_locale = 'en-us'
cached_strings = dict()


def refresh() -> None:
    global cached_strings
    with open(f'strings/{default_locale}.json') as f:
        cached_strings = json.load(f)


def gettext(name: str) -> str:
    return cached_strings[name]


def set_default_locale(locale: str) -> None:
    global default_locale
    default_locale = locale


refresh()
