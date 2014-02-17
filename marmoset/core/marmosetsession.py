import getpass

from marmosetbrowser import *
from key import *


class MarmosetSession():
    """
    The MarmosetSession class provides an interface for both executing instructions
    in both interactive and non-interactive sessions for the Marmoset browser.

    @ivar supported_methods: A list of methods supported by the browser.
    """
    supported_methods = [
        'fetch',
        'download',
        'submit',
        'adduser',
        'changeuser',
        'release',
        'long',
        'download'
    ]

    def __init__(self, *args, **kwargs):
        """
        Inititalizes the marmoset session.

        @param self: The session
        @param kwargs: Dictionary of arguments passed to the session
        """
        self.browser = Marmoset()

    def start(self):
        """
        Starts an interactive Marmoset session.  Evaluates the commands
        as if they were command line input.

        @param self: The session instance
        @return: None
        """
        pass

    def call(self, method, **kwargs):
        """
        Determines the appropriate method for the Marmoset browser to perform.

        @param self: The session instance
        @param method: String representing the method to perform
        @param args: List of arguments
        @params kwargs: Dictionary of arguments
        @return: None
        """
        try:
            # Assign username from the beginning
            username = kwargs.get('username', None)

            # Utility methods here
            if kwargs.get('adduser', False):
                password = str(getpass.getpass("Enter password for %s: "%username))
                store_user_info(username, password)
                print "Added user %s to keyring." % username

            if kwargs.get('changeuser', False):
                change_default_user(username)
                print "Changed default user to %s." % username

            if kwargs.get('removeuser', False):
                remove_user(username)
                print "Removed user %s from the keyring." % username

            if method == 'keyring':
                return

            # Do login stuff here
            username, password = get_user_info(username)

            if not password:
                if username:
                    password = str(getpass.getpass("Enter password for %s: "%username))
                else:
                    username, password = prompt()

            if not kwargs.get('nosave', False):
                store_user_info(username, password)

            self.browser.login(username, password)

            course = kwargs.get('course', None)
            assignment = kwargs.get('assignment', None)
            submission = kwargs.get('submission', None)
            files = kwargs.get('files', None)

            # Determine appropriate Marmoset browser action
            # Assumes successful login
            if method == 'fetch':
                data = self.browser.fetch(course, assignment, submission)
                for d in data:
                    for k, v in d.items():
                        print "%s: %s"%(k.capitalize(), v)
                    print

            elif method == 'download':
                f = self.browser.download(course, assignment, submission)
                print "Downloaded %s %s submission to %s"%(course, assignment, f)

            elif method == 'submit':
                status = self.browser.submit(course, assignment, files, zipname=kwargs.get('zipname', None))
                if status:
                    print "Successfully submitted %s for %s" % (assignment, course)
                else:
                    print "Failed to submit %s for %s.  Manually submit." % (assignment, course)

            elif method == 'release':
                tokens = self.browser.get_num_release_tokens(course, assignment, submission)
                print "You have %s release tokens available." % tokens
                if tokens > 0:
                    release = raw_input("Release test this submission [y/n]? ")
                    if release == 'y':
                        status = self.browser.release(course, assignment, submission)
                        if status:
                            print "Successully release tested submission."
                        else:
                            print "Failed to release test submission.  Manually release."

            elif method == 'long':
                data = self.browser.long(course, assignment, submission)
                for d in data:
                    for k, v in d.items():
                        print "%s: %s"%(k.capitalize(), v)
                    print

        except KeyError as e:
            print e

        except NoMatchingQueryException as e:
            print "Could not find %s." % e

        except BrowserException as e:
            print str(e).capitalize()


def prompt():
    """
    Prompts a user for their authentication and returns
    the results as a tuple.

    @return: tuple
    """
    username = str(raw_input("Enter your username: "))
    password = str(getpass.getpass("Enter your password: "))

    return username, password
