import logging
import logging.handlers
import sys


class Logger(object):
    def __init__(self, log_file_path=None, verbose=False):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        sh = logging.StreamHandler(sys.stdout)
        if verbose:
            sh.setLevel(logging.DEBUG)
        else:
            sh.setLevel(logging.INFO)
        sh.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(sh)

        if log_file_path:
            log_dir = os.path.dirname(log_file_path)
        else:
            log_file_path = "dt.log"

        logger.info("Logs available at %s" % log_file_path)

        rfh = logging.handlers.RotatingFileHandler(
            log_file_path, maxBytes=0, backupCount=1)
        rfh.setLevel(logging.DEBUG)
        rfh.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s: %(message)s'))
        logger.addHandler(rfh)
