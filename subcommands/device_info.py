import logging

from lib.utils import get_info


LOG = logging.getLogger(__name__)


def run(args):
    info_dict = get_info()
    for key, value in info_dict.items():
        LOG.info("%s => %s", key, value)
