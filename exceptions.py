from JustBot.utils import Logger

logger = Logger('Exception/')


class StatusError(Exception):
    pass


class CantConnect(Exception):
    pass


def InternalError(msg: str):
    logger.critical(msg)


def NoContact(msg: str):
    logger.error(msg)


def InvalidFunctionType(msg: str):
    logger.critical(msg)
