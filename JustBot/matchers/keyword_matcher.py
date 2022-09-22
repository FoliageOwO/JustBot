from ..utils import MatcherUtil, MessageChain
from ..apis import Element, Matcher

from typing import List, Union, Tuple

import re


class KeywordMatcher(Matcher):
    """
    关键词匹配器

    :param keyword: 关键词字符串或列表
    :param match_all_width: 是否匹配半角和全角 [默认: False]
    :param ignore: 忽略消息中的元素 [默认: 空列表]
    """
    def __init__(self, keyword: Union[List[str], Tuple[str], str],
                 match_all_width: bool = False, ignore: Union[List[Element], Tuple[Element]] = []) -> None:
        self.keyword = list(keyword)
        self.match_all_width = match_all_width
        self.ignore = ignore

    def match(self, message_chain: MessageChain) -> bool:
        chain = MatcherUtil.filter_elements(message_chain, self.ignore) if self.ignore else message_chain
        converted_commands = [MatcherUtil.convert_to_half_width(keyword) for keyword in self.keyword]
        if not self.match_all_width:
            result = re.search(r'|'.join(self.keyword), chain.as_display())
        else:
            result = re.search(r'|'.join(converted_commands), MatcherUtil.convert_to_half_width(chain.as_display()))
        return result is not None
