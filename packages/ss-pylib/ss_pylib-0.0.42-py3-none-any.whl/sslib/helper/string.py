import json
from datetime import datetime
from typing import Any
from stringcase import camelcase


class StringHelper:
    '''StringHelper'''

    # @staticmethod
    # def find_number(source: str, suffix: str) -> float:
    #    return re.match(r'\d+(?=㎡)')

    # @staticmethod
    # def entity_to_json(source: any) -> str:
    #    from base.entity import Entity
    #    if isinstance(source, list):
    #        elements = []
    #        for element in source:
    #            if isinstance(element, Entity):
    #                elements.append(element.to_dict())
    #        return json.dumps(elements, ensure_ascii=False)
    #    elif isinstance(source, Entity):
    #        return json.dumps(source.to_dict(), ensure_ascii=False)
    #    return None

    @staticmethod
    def to_json(source: Any) -> str:
        '''to_json'''
        return json.dumps(source, ensure_ascii=False)

    @staticmethod
    def from_json(source: str) -> Any:
        '''from_json'''
        return json.loads(source)

    @staticmethod
    def to_bool(source: str) -> bool:
        return source.lower() in ('true', '1', 'yes', 'y')

    @staticmethod
    def camel_case(source: str) -> str:
        '''camel_case'''
        return camelcase(source)

    @staticmethod
    def datetime(source: datetime) -> str | None:
        '''datetime'''
        return source.strftime('%Y-%m-%d %H:%M:%S') if source is not None else None
