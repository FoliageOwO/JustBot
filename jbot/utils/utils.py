from typing import Callable


def pretty_function(function: Callable) -> str:
    return '[light_green]Function<%s>[/light_green]' % function.__name__