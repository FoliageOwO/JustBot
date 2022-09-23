from typing import List

from .message_chain import MessageChain


class MatcherUtil:
    @staticmethod
    def convert_to_half_width(string: str) -> str:
        """
        > 说明
            将文本中所有全角符号替换为半角符号.
        > 参数
            + string [str]: 待替换的文本
        """
        full_width = '，。？！～：；＆％＃＊＄“”‘’（）【】｛｝《》'
        half_width = ',.?!~:;&%#*$""\'\'()[]{}<>'
        for i in full_width:
            string = string.replace(i, half_width[full_width.index(i)])
        return string

    @staticmethod
    def filter_elements(chain: MessageChain, ignore: List['Element']) -> MessageChain:
        """
        > 说明
            过滤元素, 保留特定元素.
        > 参数
            + chain [MessageChain]: 消息链实例
            + ignore [list[Element]]: 要过滤的元素列表
        """
        filtered_elements = []
        for element in chain.elements:
            if element.__class__ not in ignore:
                filtered_elements.append(element)
        return MessageChain.create(*filtered_elements)
