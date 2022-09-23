from dataclasses import dataclass
from typing import Awaitable, Dict, List, Tuple
from jieba import posseg, setLogLevel

setLogLevel('WARNING')
MINIMUM_CONFIDENCE = 60.0


@dataclass
class Handler:
    function: Awaitable
    keywords: List[str]
    params: Dict[str, str]
    c: float

class NLP:
    def __init__(self) -> None:
        self.handlers: List[Handler] = []
    
    def add_handler(self, **kwargs):
        self.handlers.append(Handler(**kwargs))
    
    def __check(self, message: str, handler: Handler) -> bool:
        keywords = handler.keywords
        if keywords != []:
            for keyword in keywords:
                if keyword in message:
                    return True
            return False
        return True

    async def handle(self, message_chain: 'MessageChain', command: str) -> Tuple[Dict[str, str], bool]:
        queue: List[Handler] = []
        message: str = ' '.join([plain.as_display()
                           for plain in message_chain.elements
                           if plain.__class__.__name__ == 'Plain']).strip()

        try:
            for handler in self.handlers:
                if self.__check(message, handler):
                    queue.append(handler)
        except Exception:
            return {}, False, None

        queue.sort(key=lambda it: it.c, reverse=True)
        the_best = queue[0] if queue != [] else None

        if the_best and the_best.c >= MINIMUM_CONFIDENCE:
            return self.__get_params(message, the_best.params), True, command
        return {}, False, None
    
    def __get_params(self, message: str, params: Dict[str, str]) -> dict:
        result = {}
        words = posseg.lcut(message)
        for param in params:
            for word in words:
                if word.flag in params[param].split(','):
                    result[param] = word.word
                    break
        return result
