class MatcherUtil:
    @staticmethod
    def convert_to_half_width(string: str) -> str:
        mapping = {
            '，': ',', '。': '.', '？': '?', '！': '!', '～': '~', '：': ':',
            '；': ';', '＆': '&', '％': '%', '＃': '#', '＊': '*', '＄': '$',
            '“': '"', '”': '"', '‘': '\'', '’': '\'', '（': '(', '）': ')',
            '【': '[', '】': ']', '｛': '{', '｝': '}', '《': '<', '》': '>'
        }
        for i in mapping.keys():
            string = string.replace(i, mapping[i])
        return string
