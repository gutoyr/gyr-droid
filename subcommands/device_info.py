import logging

from lib.utils import get_info
from lib.utils import run_adb as adb
from lib.utils import run_fastboot as fastboot


LOG = logging.getLogger(__name__)

def run(args):
    info_dict = get_info()
    for key, value in info_dict.items():
        LOG.info("{} => {}".format(key, value))
