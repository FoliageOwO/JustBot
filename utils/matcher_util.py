class MatcherUtil:
    @staticmethod
    def convert_to_half_width(string: str) -> str:
        full_width = '，。？！～：；＆％＃＊＄“”‘’（）【】｛｝《》'
        half_width = ',.?!~:;&%#*$""\'\'()[]{}<>'
        for i in full_width:
            string = string.replace(i, half_width[full_width.index(i)])
        return string
