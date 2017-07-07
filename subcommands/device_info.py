import logging

from lib.exception import AdbNotReadyError
from lib.exception import FastbootModeError
from lib.utils import check_adb
from lib.utils import check_fastboot
from lib.utils import get_info
from lib.utils import run_fastboot as fastboot


LOG = logging.getLogger(__name__)


def run(args):
    try:
        check_adb()
        info_dict = get_info()
        for key, value in info_dict.items():
            LOG.info("%s => %s", key, value)
    except AdbNotReadyError:
        try:
            LOG.info(check_fastboot())
            _, err = fastboot('getvar all')
            LOG.info(err)
        except FastbootModeError:
            raise
