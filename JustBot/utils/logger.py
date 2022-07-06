from rich.console import Console
from rich.status import Status
from typing import Optional, NoReturn

import time


class Logger:
    def __init__(self, logger_name: str) -> None:
        self.logger_name = logger_name
        self.console = Console()
        self.formatter = '[green][%s][/green] [bright_cyan][%s][/bright_cyan] %s'
        self._update_time()
        self.lambda_ = lambda msg, color: self._print(self.formatter % (self.time, self.logger_name, '[%s]%s[%s]' % (color, msg, color)))
        self.lambdas = {
            'info': lambda msg: self.lambda_(msg, 'white'),
            'success': lambda msg: self.lambda_(msg, 'bright_green'),
            'warning': lambda msg: self.lambda_(msg, 'bright_yellow'),
            'error': lambda msg: self.lambda_(msg, 'bright_red')
        }
        for k in self.lambdas:
            self.__setattr__(k, self.lambdas[k])

    def _update_time(self) -> NoReturn:
        self.time = time.strftime('%H:%M:%S', time.localtime())

    def _print(self, message: str) -> NoReturn:
        self._update_time()
        self.console.print(message)
