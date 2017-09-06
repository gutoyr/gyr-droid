import importlib
import logging

from lib.device import wait_for_activity

LOG = logging.getLogger(__name__)


def run(args):
    module = importlib.import_module(args.get('module')[0])
    action_list = getattr(module, args.get('actions')[0])
    activities = getattr(module, 'ACTIVITIES')

    for action in action_list:
        activity = action[0]
        action_parameter = action[1]
        wait_for_activity(activities[activity][0])
        LOG.info("%s", activity)
        activities[activity][1](action_parameter)
