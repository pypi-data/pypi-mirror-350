import logging

log = logging.getLogger("topovec")


def configLog(level=logging.DEBUG):
    from rich.logging import RichHandler

    global log
    log.setLevel(level)
    log.addHandler(RichHandler(rich_tracebacks=True))
