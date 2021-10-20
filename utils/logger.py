from rich.console import Console
from typing import Optional

import time
import sys


class Logger:
    def __init__(self, logger_name: str):
        self.logger_name = logger_name
        self.console = Console()
        self.__reformat()

    def __reformat(self):
        self.formatter = f"[white][[green]{time.strftime('%H:%M:%S', time.localtime())}[white]][/green] [white][[bright_cyan]{self.logger_name}[white]][/bright_cyan]" + " {message}"

    def __console_print(self, message: str):
        self.__reformat()
        self.console.print(message)

    def info(self, message):
        self.__console_print(self.formatter.format(message=message))

    def success(self, message):
        self.__console_print(
            self.formatter.format(message="[bright_green]{}[/bright_green]".format(message)))

    def warning(self, message):
        self.__console_print(self.formatter.format(message="[bright_yellow]{}[/bright_yellow]".format(message)))

    def error(self, message):
        self.__console_print(self.formatter.format(message="[bright_red]{}[/bright_red]".format(message)))

    def critical(self, message):
        self.__console_print(
            self.formatter.format(message="[bright_red on white]{}[/bright_red on white]".format(message)))

    def rule(self, title, style):
        self.console.rule(title=title, style=style, characters="-")

    def print(self, message):
        self.__console_print(message)

    def status(self, message):
        return self.console.status(message, spinner="simpleDotsScrolling")

    def input(self, message):
        return self.console.input(message)

    class full_rule(object):
        def __init__(self, logger: object, title: str, style: Optional[str] = ""):
            self.logger = logger
            self.title = title
            self.style = style

        def __enter__(self):
            self.logger.console.rule(title=self.title, style=self.style, characters="-")

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.logger.console.rule(title="", style=self.style, characters="-")
