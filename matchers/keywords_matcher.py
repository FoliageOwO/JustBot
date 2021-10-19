from typing import List, Union

import re


class KeywordsMatcher:
    def __init__(self, keyword: Union[List[str], str]):
        self.keyword = keyword

    def match(self, string: str) -> bool:
        result = re.search('|'.join(self.keyword), string)
        return result is not None
