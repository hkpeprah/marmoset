import argparse
import utils

import settings
import core.marmoset_browser as marmoset_browser

def main ( arguments ):
    """
    The main command-line argument parser for the Marmoset submission
    command-line interface tool.  Parses the arguments and determines
    the appropriate call to take.

    @param arguments: List of command line arguments.
    @return: None
    """
    parser = argparse.ArgumentParser(prog=settings.PROG,
                                     usage=settings.USAGE,
                                     description=settings.DESCRIPTION)
    group = parser.add_mutually_exclusive_group(required=True)

    for arg in settings.COMMAND_LINE_ARGUMENTS:
        group.add_argument(arg['short'], arg['long'], **arg['args'])

    args = parser.parse_args(arguments[1:])

    # Determine which command line argument was called and pass control
    for opt, val in args.__dict__.items():
        if val:
            marmoset_browser.Marmoset(method = opt, args = val)
            break


if __name__ == "__main__":
    import sys

    main(sys.argv)
    
