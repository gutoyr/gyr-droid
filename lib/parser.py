import argparse
import sys

from lib import logger


COMMON_ARGS = {
    ('-a', '--arg',):
        dict(help='common argument',
             action='store_true'),
}

SUBCOMMANDS = [
    ('cleanup', 'Erase cache and user data from device.',
        [COMMON_ARGS]),
    ('device-info', 'Retrieve device information.',
        [COMMON_ARGS]),
    ('screenshot', 'Take screenshots from current device screen.',
        [COMMON_ARGS]),
    ('teste', 'Used for testing purposed only.',
        [COMMON_ARGS]),
]


class Parser(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        # parse cmd_line
        self.set_parser(SUBCOMMANDS)

    def set_parser(self, subcommands):
        self.parser.add_argument('-v', '--verbose',
                                 help='Verbose mode',
                                 action='store_true')

        subparsers = self.parser.add_subparsers(
            dest='subcommand',
            help='Available subcommands')
        subparsers.required = True
        for command, help_msg, arg_groups in subcommands:
            command_parser = subparsers.add_parser(command, help=help_msg)
            for arg_group in arg_groups:
                for arg, options in arg_group.items():
                    command_parser.add_argument(*arg, **options)

    def parse(self):
        args = self.parser.parse_args()
        return vars(args)


def get_args():
    line_parser = Parser()
    args = line_parser.parse()
    logger.Logger(verbose=args['verbose'])
    return args
