import sys
from argparse import ArgumentParser, Action, ArgumentTypeError, HelpFormatter

from settings import *
from core.marmosetsession import MarmosetSession


def required_length(nmin, nmax=sys.maxint):
    class RequiredLength(Action):
        def __init__(self, *args, **kwargs):
            super(RequiredLength, self).__init__(*args, **kwargs)

        def __call__(self, parser, namespace, values, option_string=None):
            if not nmin <= len(values) <= nmax:
                msg = None
                if nmax == sys.maxint:
                    msg = "%s expects at least %s arguments"%(self.dest, nmin)
                else:
                    msg = "%s expects between %s and %s arguments"%(self.dest, nmin, nmax)
                raise ArgumentTypeError(msg)
            setattr(namespace, self.dest, values)
    return RequiredLength


def main():
    """
    The main command-line argument parser for the Marmoset submission
    command-line interface tool.  Parses the arguments and determines
    the appropriate call to take.

    @param arguments: List of command line arguments.
    @return: None
    """
    parser = ArgumentParser(prog=PROG,
                            description=DESCRIPTION,
                            version="%s %s" %(PROG, VERSION),
                            epilog=EPILOG,
                            formatter_class = lambda prog: HelpFormatter(prog, max_help_position=30))

    parser_a = ArgumentParser(add_help=False)
    parser_a.add_argument('course', help="specify a course")
    parser_a.add_argument('assignment', help="specify an assignment")
    parser_a.add_argument('-u', '--username', dest='username', metavar='username', help="user to login as, defaults to the default user")
    parser_a.add_argument('-n', '--nosave', action='store_true', help="don't save the user being logged in as")

    parser_b = ArgumentParser(add_help=False)
    parser_b.add_argument('submission', nargs='?', type=int, help="specific submission or number of submissions")

    parser_c = ArgumentParser(add_help=False)
    group = parser_c.add_argument_group(title="keyring utilities")
    group.add_argument('-a', '--adduser', action='store_true', help="add a user to the marmoset keyring")
    group.add_argument('-c', '--changeuser', action='store_true', help="change the default user in the marmoset keyring")
    group.add_argument('-r', '--removeuser', action='store_true', help="remove a user from the marmoset keyring")

    subparsers = parser.add_subparsers(dest='method', title="commands")
    commands = sorted(['submit', 'download', 'fetch', 'long', 'release', 'keyring'])

    for cmd in commands:
        if cmd == 'submit':
            sub = subparsers.add_parser(cmd, parents=[parser_a], help="submit file(s) to the marmoset submission server")
            sub.add_argument('files', nargs='+', help="one or more files to submit")
        elif cmd == 'keyring':
            sub = subparsers.add_parser(cmd, parents=[parser_c], help="modify the marmoset keyring")
            sub.add_argument('username', help="marmoset username")
        else:
            sub = subparsers.add_parser(cmd, parents=[parser_a, parser_b],  help="{0} the most recent submission(s).  Defaults to last/latest".format(cmd))

        if cmd in ['submit', 'download']:
            sub.add_argument('-z', '--zipname', type=str, metavar='zipname', help="name of the zipfile to submit/download")

    args = vars(parser.parse_args())

    if len(args) == 0:
        parser.print_help()
        return

    MarmosetSession().call(**args)


if __name__ == "__main__":
    import sys
    main()
    
