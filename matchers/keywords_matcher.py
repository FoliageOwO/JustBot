from JustBot.utils.matcher_util import MatcherUtil

from typing import List, Union

import re


class KeywordsMatcher:
    def __init__(self, keyword: Union[List[str], str],
                 match_all_width: bool = False) -> None:
        self.keyword = keyword
        self.match_all_width = match_all_width

    def match(self, string: str) -> bool:
        converted_commands = [MatcherUtil.convert_to_half_width(command) for command in self.commands]
        if not self.match_all_width:
            result = re.search(r'|'.join(self.keyword), string)
        else:
            result = re.search(r'|'.join(converted_commands), MatcherUtil.convert_to_half_width(string))
        return result is not None
