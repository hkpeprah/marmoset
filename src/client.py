from bs4 import BeautifulSoup

from anonBrowser import anonBrowser

import re
import sys
try: 
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class marmoset():
    """
    The marmoset class manages interaction with the Marmoset Submission
    Server thrugh the anonBrowser.

    @ivar base_url: The base url for the marmoset submission server.
    """
    base_url = "http://marmoset.student.cs.uwaterloo.ca"

    def __init__(self, kwargs):
        """
        Initializes the marmoset browser.  Handles navigation and parsing
        of pages.

        @param self: The marmoset instance
        @param kwargs: Dictionary of arguments to determine method
        @return: marmoset
        """
        self.browser = anonBrowser(cookiefile="/tmp/marmoset.session.cookies")
        if self.authenticate():
            try:
                getattr(self, kwargs['method'])(*kwargs['args'])
            except Exception, e:
                print e
        else:
            raise Exception("Invalid username/password.")

    def authenticate(self):
        """
        Attempts to authenticate the user using the given username/password
        combinations.

        @param self: The marmoset instance
        @return: boolean
        """
        self.browser.open(self.base_url)
        if self.browser.geturl().find("cas") > -1:
            self.browser.select_form(nr=0)
            username, password = prompt()
            self.browser.form['username'] = username
            self.browser.form['password'] = password
            self.browser.submit()

            if self.browser.geturl().find("cas") > -1:
                return False
            
            self.browser.save_cookies()

        self.browser.select_form(nr=0)
        self.browser.submit()
        return True

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
        for group in soup.find_all('tr'):
            links = group.find_all('a')
            if len(links) > 0 and re.match(re.compile('(.|\s)*' + patt + '\s*', re.I), links[0].text):
                link = group.find(lambda tag: tag.text.find(target) > -1).find('a')
                href = link.attrs['href']
                link = next(l for l in self.browser.links() if href == dict(l.attrs)['href'])
                self.browser.follow_link(link)

    def submit(self, course, assignment, filename):
        """
        Submits a file to the specified assignment and course.

        @param self: The marmoset instance
        @param course: The course
        @param assignment: The assignment
        @param filename: The name of the file we're submitting.
        @return: None
        """
        self.select_course(course)
        self.select_and_follow(assignment, 'submit')
        self.browser.select_form(nr = 0)
        self.browser.form.add_file(open(filename), 'text/plain', filename)
        self.browser.submit()

        if self.browser.geturl().find("/view/project.jsp?projectPK=") > -1:
            print "Successfully submitted {0} for {1}".format(filename, assignment)
        else:
            print "Something went wrong.  Manually submit."

    def release(self, course, assignment, submission):
        """
        Release tests the specified submission for the assignment.

        @param self: The masonry isntance
        @param assignment: The name of the assignment
        @param submission: The submission number
        @return: None
        """
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
                print "Successfully release tested submission {0} for {1}".format(submission, assignment)
        else:
            if len(tokens) > 0: 
                tokens = tokens[0]
                print " ".join(tokens.text.split())
            print "You cannot release test this submission."

    def long(self, course, assignment, submission):
        """
        Gets the detailed test results for a specified assingment based on the submission
        number.

        @param self: The masonry instance
        @param assignment: The name of the assignment
        @param submission: The submission number
        @return: None
        """
        self.select_course(course)
        self.select_and_follow(assignment, 'view')
        self.find_submission(submission)
        self.print_table(assignment)

    def fetch(self, course, assignment):
        """
        Fetches the five most recent short results for a specified assignment.

        @param self: The masonry instance
        @param course: The name of the course
        @param assignment: The name of the assignment
        @return: None
        """
        self.select_course(course)
        self.select_and_follow(assignment, 'view')
        self.print_table(assignment, 6)

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

    def print_table(self, assignment, number_of_rows=sys.maxint):
        """
        Prints out the tables on a given Marmoset page.

        @param self: The marmoset instance
        @param assignment: The assignment we're looking at
        @param number_of_rows: The number of rows to print
        @return: None
        """
        response = self.browser.reload()
        soup = BeautifulSoup(response)

        deadline = soup.find(lambda tag: tag.name == 'p' and tag.text.find('Deadline') > -1)
        print "Project {0}: {0}\n{1}\n".format(assignment.upper(), " ".join(deadline.text.strip().split()))

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
