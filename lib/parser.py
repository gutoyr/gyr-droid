import argparse

from lib import logger


COMMON_ARGS = {
    ('-a', '--arg',):
        dict(help='common argument',
             action='store_true'),
}

SCREENSHOT_ARGS = {
    ('-s', '--serial',):
        dict(help='sequence screenshot file names will use serial number '
                  'instead of the timestamp to differ them, i.e., '
                  '<filename>_<serial_number>.png',
             action='store_false'),
    ('-f', '--filename',):
        dict(help='base file name used to store the image, '
                  'file extension must be .png',
             nargs=1,
             default=None),
}

SUBCOMMANDS = [
    ('cleanup', 'Erase cache and user data from device.',
     [COMMON_ARGS]),
    ('device-info', 'Retrieve device information.',
     [COMMON_ARGS]),
    ('screenshot', 'Take screenshots from current device screen.',
     [SCREENSHOT_ARGS]),
    ('teste', 'Used for testing purposed only.',
     [COMMON_ARGS]),
]


class Parser(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        # parse cmd_line
        self.set_parser(SUBCOMMANDS)

    def set_parser(self, subcommands):
        self.parser.add_argument('-l', '--log',
                                 help='Enable log to file '
                                      '(default logfile: gdt.log)',
                                 metavar='log_file_name',
                                 nargs='?',
                                 const='gdt.log',
                                 default=None)
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
