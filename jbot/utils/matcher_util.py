from .message_chain import MessageChain


class MatcherUtil:
    @staticmethod
    def convert_to_half_width(string: str) -> str:
        full_width = '，。？！～：；＆％＃＊＄“”‘’（）【】｛｝《》'
        half_width = ',.?!~:;&%#*$""\'\'()[]{}<>'
        for i in full_width:
            string = string.replace(i, half_width[full_width.index(i)])
        return string

    @staticmethod
    def filter_elements(chain: MessageChain, ignore: list) -> MessageChain:
        filtered_elements = []
        for element in chain.elements:
            if element.__class__ not in ignore:
                filtered_elements.append(element)
        return MessageChain.create(*filtered_elements)
