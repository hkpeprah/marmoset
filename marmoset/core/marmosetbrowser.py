from bs4 import BeautifulSoup

from anonbrowser import AnonBrowser
from key import store_user_info, get_user_info, change_default_user

import re
import sys
import StringIO
try: 
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from zipfile import ZipFile


DESKTOP_USER_AGENTS = [
    "Mozilla/5.0",
    "AppleWebKit/537.346",
    "Chrome/29.0.1547.2",
    "Safari/537.36",
    "Opera/9.80",
    "Opera/12.80",
    "Netscape/9.1.0285",
    "Firebird/3.6.13",
    "Mozilla/4.0",
    "Firefox/6.0.1"
]


class NoMatchingQueryException(Exception):
    pass


class Marmoset():
    """
    The marmoset class manages interaction with the Marmoset Submission
    Server thrugh the AnonBrowser.

    @ivar base_url: The base url for the marmoset submission server.
    """
    base_url = "http://marmoset.student.cs.uwaterloo.ca"
    supported_methods = [
        'fetch',
        'download',
        'submit',
        'adduser',
        'changeuser',
        'release',
        'long'
    ]

    def __init__(self, stdout = True, **kwargs):
        """
        Initializes the marmoset browser.  Handles navigation and parsing
        of pages.

        @param self: The marmoset instance
        @param kwargs: Dictionary of arguments to determine method
        @return: marmoset
        """
        self.stdout = StringIO.StringIO
        self.browser = AnonBrowser(user_agents=DESKTOP_USER_AGENTS, cookiefile="/tmp/marmoset.session.cookies")

        if not stdout:
            self.toggle_stdout()

        for k, v in kwargs.items():
            if not k == 'method' or not k == 'args':
                setattr(self, k, v)

        try:
            getattr(self, kwargs['method'])(*kwargs['args'])
        except KeyError:
            raise NotImplementedError("Error: %s hasn't been implemented yet."% kwargs['method'])
        except NoMatchingQueryException as e:
            raise NoMatchingQueryException("Error: %s not found."% e)

    def authenticate(self, username = None, password = None):
        """
        Attempts to authenticate the user using the given username/password
        combinations.

        @param self: The marmoset instance
        @return: boolean
        """
        self.browser.open(self.base_url)
        if self.browser.geturl().find("cas") > -1:
            self.browser.select_form(nr=0)
            
            if not username and not password:
                username, password = self.login()

            self.browser.form['username'] = username
            self.browser.form['password'] = password
            self.browser.submit()

            if self.browser.geturl().find("cas") > -1:
                return False
            
            self.browser.save_cookies()

        self.browser.select_form(nr=0)
        self.browser.submit()

        return True

    def adduser(self, username, password=None):
        """
        Adds a user to the marmoset keyring.

        @param self: the marmoset instance
        @param username: user's name, a string
        @param password: user's password, a string
        @return: None
        """
        if not password:
            password = str(getpass.getpass("Enter your password: "))
        store_user_info(username, password)

    def changeuser(self, username):
        """
        Changes the default user for the marmoset keyring.

        @param self: the marmoset instance
        @param username: user's name, a string
        @return: None
        """
        change_default_user(username)

    def login(self):
        """
        Logs the user in, defaulting to the default keyring user if no user is specified.
        If no default keyring user, prompts for input.

        @param self: The marmoset instance
        @return: tuple
        """
        if getattr(self, 'user', None):
            self.user, passwd = get_user_info()
        else:
            self.user, passwd = get_user_info()

        if self.user and passwd:
            return self.user, passwd

        self.user, passwd = prompt()

        # Save to keyring if nosave isn't specified
        # Defaults to true
        if not getattr(self, 'nosave', True):
            store_user_info(self.user, passwd)

        return self.user, passwd

    def toggle_stdout(self):
        """
        Toggle stdout between the classes stdout handler and the system's standard
        output handler.

        @param self: The marmoset instance
        @return: None
        """
        sys.stdout, self.stdout = self.stdout, sys.stdout

        return None

    def select_course(self, course):
        """
        Navigates to the course selection page and determine which course
        page to visit.

        @param self: The marmoset instance
        @param course: The course
        @return: None
        """
        for link in self.browser.links():
            if re.match(re.compile('.*' + course + '(\s+|\(|:|$)', re.I), link.text):
                self.browser.follow_link(link)

    def select_and_follow(self, patt, target): 
        """
        Selects a link based on a pattern and follows it.

        @param self: The marmoset instance
        @param patt: The pattern to look for
        @param target: The target url to fo follow after matching the pattern.
        @return: None
        """
        response = self.browser.reload()
        soup = BeautifulSoup(response.read())
        link = None

        for group in soup.find_all('tr'):
            links = group.find_all('a')
            if len(links) > 0 and links[0].text.strip().lower() == patt.lower():
                link = group.find(lambda tag: tag.text.find(target) > -1).find('a')
                href = link.attrs['href']
                link = next(l for l in self.browser.links() if href == dict(l.attrs)['href'])
                self.browser.follow_link(link)

        if not link:
            raise NoMatchingQueryException(patt)

    def submit(self, course, assignment, filename):
        """
        Submits a file to the specified assignment and course.

        @param self: The marmoset instance
        @param course: The course
        @param assignment: The assignment
        @param filename: The name of the file we're submitting.
        @return: None
        """
        if not self.authenticate():
            raise Exception("Invalid username/password combination")

        self.select_course(course)
        self.select_and_follow(assignment, 'submit')
        self.browser.select_form(nr = 0)

        # If multiple files, zip and submit
        if self.additional_files and len(self.additional_files) > 0:
            filename = write_zip(assignment + ".zip", [filename] + self.additional_files)

        self.browser.form.add_file(open(filename), 'text/plain', filename)
        self.browser.submit()

        if self.browser.geturl().find("/view/project.jsp?projectPK=") > -1:
            print "Successfully submitted {0} for {1} {2}".format(filename, course, assignment)
        else:
            print "Something went wrong.  Manually submit."
            return False

        return True

    def release(self, course, assignment, submission):
        """
        Release tests the specified submission for the assignment.

        @param self: The masonry isntance
        @param assignment: The name of the assignment
        @param submission: The submission number
        @return: None
        """
        if not self.authenticate():
            raise Exception("Invalid username/password combination")

        self.select_course(course)
        self.select_and_follow(assignment, 'view')
        self.find_submission(submission)
        
        response = self.browser.reload()
        soup = BeautifulSoup(response.read())

        release_link = soup.find_all(lambda tag: tag.name == 'a' and tag.text.find('Click here to release') > -1)
        tokens = soup.find_all(lambda tag: tag.name == 'p' and tag.text.find('You currently have') > -1)

        if len(release_link) > 0:
            release_link = release_link[0]
            link = next(l for l in self.browser.links() if release_link.attrs['href'] == dict(l.attrs)['href'])
            if len(tokens) > 0:
                tokens = tokens[0]
                print " ".join(tokens.text.split())
            proceed = str(raw_input("Release test this submission [y/n]? "))
            if len(proceed) > 0 and proceed[0] == 'y':
                submission = next(tag for tag in soup.find_all('h2') if tag.text.find('Submission') > -1)
                submission = submission.text.split()[1][:-1]
                self.browser.follow_link(link)
                self.browser.select_form(nr = 0)
                self.browser.submit()
                print "Successfully release tested submission {0} for {1} {2}".format(submission, course, 
                                                                                      assignment)
        else:
            if len(tokens) > 0: 
                tokens = tokens[0]
                print " ".join(tokens.text.split())
            print "You cannot release test this submission."
            return False

        return True

    def long(self, course, assignment, submission):
        """
        Gets the detailed test results for a specified assingment based on the submission
        number.

        @param self: The masonry instance
        @param assignment: The name of the assignment
        @param submission: The submission number
        @return: None
        """
        if not self.authenticate():
            raise Exception("Invalid username/password combination")

        self.select_course(course)
        self.select_and_follow(assignment, 'view')
        self.find_submission(submission)
        
        return self.print_table(course, assignment)

    def fetch(self, course, assignment):
        """
        Fetches the five most recent short results for a specified assignment.

        @param self: The masonry instance
        @param course: The name of the course
        @param assignment: The name of the assignment
        @return: None
        """
        if not self.authenticate():
            raise Exception("Invalid username/password combination")

        self.select_course(course)
        self.select_and_follow(assignment, 'view')

        return self.print_table(course, assignment, 6)

    def find_submission(self, submission):
        """
        Finds the specified submission and follows the link.

        @param self: The marmoset instance
        @param submission: The submission number
        """
        submission = int(submission)
        response = self.browser.reload()
        soup = BeautifulSoup(response.read())

        links = self.browser.links()
        detail_links = soup.find_all(lambda tag: tag.name == 'a' and tag.text.find('view') > -1)
        for i in range(0, len(detail_links)):
            link = detail_links[i]

            try:
                link = next(l for l in links if dict(l.attrs)['href'] == link.attrs['href'])
            except StopIteration:
                pass

            if submission == 0:
                self.browser.follow_link(link)
                break
            elif i + 1 == len(detail_links):
                self.browser.follow_link(link)
                break
            else:
                submission -= 1

    def print_table(self, course, assignment, number_of_rows=sys.maxint):
        """
        Prints out the tables on a given Marmoset page.

        @param self: The marmoset instance
        @param assignment: The assignment we're looking at
        @param number_of_rows: The number of rows to print
        @return: None
        """
        response = self.browser.reload()
        soup = BeautifulSoup(response)

        text = next(tag for tag in soup.find_all('p') if tag.text.find("Deadline") > -1).text.strip().split()
        deadline = [] if len(text) < 3 else text[:3]

        print "{0} Project {1}: {1}\n{2}\n".format(course.upper(), assignment.upper(), " ".join(deadline))

        rows = soup.find_all('tr')
        headers, data = [], []
        for i in range(0, min(len(rows), number_of_rows)):
            row = rows[i]
            
            for col in row.find_all('th'):
                text = col.text.split()
                if len(text) > 0:
                    headers.append(" ".join(text))

            td = []
            for col in row.find_all('td'):
                text = col.text.split()
                if len(col.find_all('a')) > 0:
                    td.append(self.base_url + col.find('a').attrs['href'])
                elif 'colspan' in col.attrs:
                    for i in range(0, int(col.attrs['colspan'])):
                        td.append(" ".join(text))
                else:
                    td.append(" ".join(text))
            
            if len(td) > 0:
                data.append(OrderedDict(zip(headers, td)))

        for i in range(0, len(data)):
            d = data[i]
            for k, v in d.items():
                print "{0}:  {1}".format(k, v)
            if i < len(data) - 1:
                print

        return data


def write_zip(name, files):
    """
    Writes a zip file and returns the name of the file.

    @param name: string, name of the file to create
    @param files: list of strings, name of files to zip
    """
    with ZipFile(name, 'a') as myzip:
        for f in files:
            myzip.write(f)
    return name


def prompt():
    """
    Prompts a user for their authentication and returns
    the results as a tuple.

    @return: tuple
    """
    import getpass
    username = str(raw_input("Enter your username: "))
    password = str(getpass.getpass("Enter your password: "))

    return username, password
