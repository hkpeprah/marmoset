from argparse import ArgumentParser

from settings import PROG, USAGE, DESCRIPTION
from core.marmosetbrowser import Marmoset


INCLUSIVE_COMMAND_LINE_ARGUMENTS = (
    ("-u", "--user", {
        'nargs': 1,
        'metavar': ("username"),
        'help': "user to login as, defaults to the default user"
    }),
    ("-n", "--nosave", {
        'action': "store_false",
        'help': "save the user being logged in as."
    }),
    ("additional_files", {
        'nargs': "*",
        'help': "additional files to zip with and submit"
    }),
    ("-z", "--zipname", {
        'nargs': 1,
        'metavar': ("zipname"),
        'help': "name of the zipfile to submit"
    })
)

EXCLUSIVE_COMMAND_LINE_ARGUMENTS = (
    ("-a", "--adduser", {
        'nargs': 1,
        'metavar': ("username"),
        'help': "add a user to the marmoset keyring for automatic sign in/submit."
    }),
    ("-c", "--changeuser", {
        'nargs': 1,
        'metavar': ("username"),
        'help': "change the default keyring user."
    }),
    ("-s", "--submit", {
        'nargs': 3,
        'metavar': ("course", "problem", "filename"),
        'help': "submit file(s) to the marmoset server."
    }),
    ("-f", "--fetch", {
        'nargs': 2,
        'metavar': ("course", "problem"),
        'help': "fetch the last five(5) test results."
    }),
    ("-r", "--release", {
        'nargs': 3,
        'metavar': ("course", "problem", "submission"),
        'help': "release test specified submission (0 - Most Recent, Max - Oldest)"
    }),
    ("-l", "--long", {
        'nargs': 3,
        'metavar': ("course", "problem", "submission"),
        'help': "get the long test results for the specified submission."
    }),
    ("-d", "--download", {
        'nargs': 3,
        'metavar': ("courese", "problem", "submission"),
        'help': "download a submission."
    }),
    ("-v", "--version", { 
        'action': "store_true",
        'help': "print the version string."
    })
)  


def main():
    """
    The main command-line argument parser for the Marmoset submission
    command-line interface tool.  Parses the arguments and determines
    the appropriate call to take.

    @param arguments: List of command line arguments.
    @return: None
    """
    parser = ArgumentParser(prog=PROG,
                            usage=USAGE,
                            description=DESCRIPTION)
    group = parser.add_mutually_exclusive_group(required=True)
    for arg in INCLUSIVE_COMMAND_LINE_ARGUMENTS:
        parser.add_argument(*arg[:-1], **arg[-1])
    for arg in EXCLUSIVE_COMMAND_LINE_ARGUMENTS:
        group.add_argument(*arg[:-1], **arg[-1])

    # Set the arguments
    parsed = {}
    for k, v in vars(parser.parse_args()).items():
        if not v == None:
            if k in Marmoset.supported_methods:
                parsed['method'] = k
                parsed['args'] = v
            else:
                parsed[k] = v
                if type(v) == list:
                    parsed[k] = (v if k == 'additional_files' else v[0])
    if not 'method' in parsed:
        parser.print_help()
        return None
    Marmoset(**parsed)


if __name__ == "__main__":
    import sys
    main()
    
