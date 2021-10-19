from typing import List, Union

import re


class CommandMatcher:
    def __init__(self, commands: Union[List[str], str]):
        self.commands = commands

    def match(self, string: str) -> bool:
        result = re.match(rf'{"|".join(self.commands)}', string)
        return (result.span() is not None) if result else False
