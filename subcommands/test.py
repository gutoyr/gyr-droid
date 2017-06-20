import logging

from lib.utils import run_adb as adb
from lib.utils import run_fastboot as fastboot


LOG = logging.getLogger(__name__)


def run(args):
    LOG.debug("debug message")
    LOG.info("info message")
    LOG.error("error message")
    fastboot_args = '--version'
    fastboot(fastboot_args)
    adb_args = 'version'
    adb(adb_args)
    adb_args = 'devices'
    adb(adb_args)
