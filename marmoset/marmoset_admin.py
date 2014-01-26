import argparse
import utils
from zipfile import ZipFile

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
        if 'long' in arg:
            group.add_argument(arg['short'], arg['long'], **arg['args'])
        else:
            parser.add_argument(arg['name'], **arg['args'])

    args = vars(parser.parse_args(arguments[1:]))

    # Determine which command line argument was called and pass control
    for opt, val in args.items():
        if val and not opt == 'additional_files':
            alen = len(args['additional_files'])
            if alen > 0:
                if not opt == 'submit':
                    msg = "Expected %s arguments, given %s." % (len(val), len(val) + alen)
                    raise argparse.ArgumentTypeError(msg)
                # This sort of requires a knowledge of the commands, which
                # ideally, would not want.
                val[2], files = val[1] + ".zip", [val[2]] + args['additional_files']
                with ZipFile(val[2], 'a') as myzip:
                    for f in files:
                        myzip.write(f)
            marmoset_browser.Marmoset(method = opt, args = val)
            break


if __name__ == "__main__":
    import sys

    main(sys.argv)
    
