from ..utils import MatcherUtil, MessageChain
from ..apis import Element, Matcher

from typing import List, Union, Tuple, Type

import re


class CommandMatcher(Matcher):
    """
    > 说明
        命令匹配器.
    > 参数
        + command [list[str] | tuple[str] | str]: 命令字符串或列表
        + match_all_width [bool]: 是否同时匹配半角和全角 [default=False]
        + ignore [list[type[Element]]]: 忽略消息中的元素, 如忽略 `At`, `Reply` [defualt=[]]
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
