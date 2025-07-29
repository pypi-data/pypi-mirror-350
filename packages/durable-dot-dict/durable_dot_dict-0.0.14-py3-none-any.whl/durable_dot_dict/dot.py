from typing import MutableMapping, Union


class DotList(list):
    def __getitem__(self, index):
        value = super().__getitem__(index)
        if isinstance(value, dict):
            return Dot(value)
        return value


class Dot(dict):

    def __getattr__(self, item) -> Union['Dot', DotList]:
        value = self[item]
        if isinstance(value, dict):
            return Dot(value)
        elif isinstance(value, list):
            return DotList(value)
        return value