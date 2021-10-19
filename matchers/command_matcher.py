from JustBot.utils import MatcherUtil

from typing import List, Union

import re


class CommandMatcher:
    def __init__(self, commands: Union[List[str], str], match_all_width: bool = False):
        self.commands = commands
        self.match_all_width = match_all_width

    def match(self, string: str) -> bool:
        converted_commands = [MatcherUtil.convert_to_half_width(command) for command in self.commands]
        if not self.match_all_width:
            result = re.match(r'|'.join(self.commands), string)
        else:
            result = re.match(r'|'.join(converted_commands), MatcherUtil.convert_to_half_width(string))
        return (result.span() is not None) if result else False
