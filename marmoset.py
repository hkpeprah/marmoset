#!/usr/bin/python
"""Script main, options, interaction, etc.
   author: hkpeprah"""

import argparse, re
from marmosetSubmit import *


if __name__ == "__main__":
    """Handle options and direct user."""
    parser = argparse.ArgumentParser(description = "Use this script to submit assignments and fetch mark from the University of Waterloo Marmoset Submission Server.")
    group = parser.add_mutually_exclusive_group(required = True)
    parser.add_argument('course', metavar='course', nargs=1, help='the course to submit/fetch from.')
    parser.add_argument('problem', metavar='problem', nargs=1, help='the assignment or problem name.')
    parser.add_argument('filename', metavar='filename', nargs='?', help='the file to submit. (or int in case of release/result)')
    group.add_argument('-s', '--submit', dest = 'submit', action="store_true", help='submit a file to marmoset.  Inputs: course, problem and file.')
    group.add_argument('-f', '--fetch', dest='fetch', action="store_true", help='fetch grades from marmoset.  Inputs: course,  problem/assignment, and possible an integer.')
    group.add_argument('-l', '--long', dest="long", action="store_true", help='get long result for test.  Inputs: course, assignment, and int.')
    group.add_argument('-r', '--release', dest='release', action="store_true", help='release test submission.  Inputs: course, assignment, and int.')
    args = parser.parse_args()
    if ( args.submit ):
        if ( args.filename == None ): parser.print_help()
        else: marmoset_submit(args.course[0], args.problem[0], args.filename)
    elif ( args.fetch ):
        if ( args.filename == None ): marmoset_fetch(args.course[0], args.problem[0])
        else: 
            try: marmoset_fetch(args.course[0], args.problem[0], int(args.filename))
            except Exception as e:
                parser.print_help()
    elif ( args.long ):
        if args.filename == None: marmoset_long(args.course[0], args.problem[0])
        else:
            try: marmoset_long(args.course[0], args.problem[0], int(args.filename))
            except Exception as e: parser.print_help()
    elif ( args.release ):
        if ( args.filename == None ): marmoset_release(args.course[0], args.problem[0])
        else:
            try: marmoset_release(args.course[0], args.problem[0], int(args.filename))
            except Exception as e: parser.print_help()
    else: parser.print_help()
