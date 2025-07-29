'''number.py'''

import re


class NumberUtil:
    '''NumberUtil'''

    @staticmethod
    def to_int(src: str, fallback: int | None = 0) -> int | None:
        '''문자열을 정수로 변경'''
        if src is None:
            return fallback
        unit = 10000 if src.endswith('만원') else 1
        find = re.findall(pattern=r'\d+', string=src)
        return int(''.join(find)) * unit if find is not None and len(find) > 0 else fallback

    @staticmethod
    def find_percent(src: str, fallback: int | None = 0) -> int | None:
        '''문자열에 퍼센트 찾기'''
        find = re.search(r'\d+%', src)
        return int(find.group().replace('%', '')) if find is not None else fallback

    @staticmethod
    def find_area(src: str, fallback: int | None = 0) -> float | None:
        '''문자열에서 면적 찾기'''
        if src is None:
            return fallback
        find = re.findall(r'\d+\.?\d*(?=㎡)', src)
        if find is None:
            return fallback
        return sum(float(str(re.sub(r'[^0-9.]', '', x)).strip().replace(')', '')) for x in find)
