#!/usr/bin/python
"""Script main, options, interaction, etc.
   author: hkpeprah"""

import argparse, re
from marmosetSubmit import *


if __name__ == "__main__":
    """Handle options and direct user."""
    parser = argparse.ArgumentParser(description = "Use this script to submit assignments and fetch mark from the University of Waterloo Marmoset Submission Server.")
    parser.add_argument('course', metavar='course', nargs=1, help='the course to submit/fetch from.')
    parser.add_argument('problem', metavar='problem', nargs=1, help='the assignment or problem name.')
    parser.add_argument('filename', metavar='filename', nargs='?', help='the file to submit.')
    parser.add_argument('-s', '--submit', dest = 'submit', action="store_true", help='submit a file to marmoset.  Inputs: course, problem and file.')
    parser.add_argument('-f', '--fetch', dest='fetch', action="store_true", help='fetch grades from marmoset.  Inputs: course,  problem/assignment.')
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
    else: parser.print_help()
