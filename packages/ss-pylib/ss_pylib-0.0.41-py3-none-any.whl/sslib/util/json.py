'''json.py'''

import json
from sslib.base.entity import Entity


class JsonUtil:
    '''JsonUtil'''

    @staticmethod
    def to_json(source: any) -> str | None:
        '''to_json'''
        if source is None:
            return None
        target = source
        if isinstance(source, list):
            elements = []
            for element in source:
                elements.append(JsonUtil.__to_json(element))
            target = elements
            if len(target) == 0:
                return None
        else:
            target = JsonUtil.__to_json(source)
        return json.dumps(target, ensure_ascii=False)

    @staticmethod
    def __to_json(source: any):
        if isinstance(source, Entity):
            return source.to_dict()
        return source

    @staticmethod
    def from_json(source: str, fallback: str = '[]') -> any:
        '''from_json'''
        if source is None:
            source = fallback
        return json.loads(source)
