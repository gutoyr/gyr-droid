import logging
import logging.handlers
import sys


LOG_FILE = './gdt.log'


class Logger(object):
    def __init__(self, enable_log=False, verbose=False):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler(sys.stdout)
        if verbose:
            stream_handler.setLevel(logging.DEBUG)
        else:
            stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(stream_handler)

        if enable_log:
            logger.info("Logs available at %s", LOG_FILE)

            rfh = logging.handlers.RotatingFileHandler(
                LOG_FILE, maxBytes=0, backupCount=1)
            rfh.setLevel(logging.DEBUG)
            rfh.setFormatter(logging.Formatter(
                '%(asctime)s | %(levelname)s | %(name)s: %(message)s'))
            logger.addHandler(rfh)
