import logging

from subcommands import cleanup_device
from subcommands import device_info
from subcommands import screenshot
from subcommands import test
from lib.parser import get_args
from lib import exception


LOG = logging.getLogger(__name__)
SUBCOMMANDS = {
    'cleanup': cleanup_device,
    'device-info': device_info,
    'screenshot': screenshot,
    'teste': test,
}


if __name__ == '__main__':
    try:
        args = get_args()
        LOG.debug(args)
        subcommand = args.get('subcommand')
        SUBCOMMANDS[subcommand].run(args)
    except exception.BaseException as e:
        LOG.exception("Subcommand %s failed.", subcommand)
