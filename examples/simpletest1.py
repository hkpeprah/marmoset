import sys
sys.path.insert(0, '..')

from marmoset import Marmoset, BrowserException
import getpass

m = Marmoset()
username, password = raw_input("Enter username: "), getpass.getpass("Enter password: ")
m.login(username, password)

for course in ['cs246', 'cs241']:
    for assignment in ['a4p1', 'a4p2']:
        try:
            tokens = m.get_num_release_tokens(course, assignment)
            print "Number of release tokens for {0} {1}: {2}".format(course, assignment, tokens)
        except BrowserException:
            pass
