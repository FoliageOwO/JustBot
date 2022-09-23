from ..utils import MatcherUtil, MessageChain
from ..apis import Element, Matcher

from typing import List, Union, Tuple, Type

import re


class CommandMatcher(Matcher):
    """
    命令匹配器

    :param command: 命令字符串或列表
    :param match_all_width: 是否匹配半角和全角 [默认: False]
    :param ignore: 忽略消息中的元素 [默认: 空列表]
    """

    def __init__(self, command: Union[List[str], Tuple[str], str],
                 match_all_width: bool = False, ignore: Union[List[Type[Element]], Tuple[Type[Element]]] = ()) -> None:
        self.cmd = command if isinstance(command, list) else [command]
        self.command = [c + ' ' for c in self.cmd] + [c + '\n' for c in self.cmd] + [c for c in self.cmd]
        self.match_all_width = match_all_width
        self.ignore = ignore

    def match(self, message_chain: MessageChain) -> bool:
        chain = MatcherUtil.filter_elements(message_chain, self.ignore) if self.ignore else message_chain
        converted_commands = [MatcherUtil.convert_to_half_width(command) for command in self.command]
        if not self.match_all_width:
            result = re.match(r'|'.join(self.command), chain.as_display())
        else:
            result = re.match(r'|'.join(converted_commands), MatcherUtil.convert_to_half_width(chain.as_display()) + ' ')
        return (result.span() is not None) if result else False
