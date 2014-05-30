from bs4 import BeautifulSoup

from anonbrowser import AnonBrowser

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


class NotTestedYet(Exception):
    pass


class BrowserException(Exception):
    pass


class NoMatchingQueryException(Exception):
    pass


class Marmoset():
    """
    The marmoset class manages interaction with the Marmoset Submission
    Server thrugh the AnonBrowser.

    @ivar base_url: The base url for the marmoset submission server.
    """
    base_url = "http://marmoset.student.cs.uwaterloo.ca"
    cookiefile = "/tmp/marmoset.session.cookies"

    def __init__(self, username=None, password=None, **kwargs):
        """
        Initializes the marmoset browser.  Handles navigation and parsing
        of pages.

        @param self: The marmoset instance
        @param kwargs: Dictionary of arguments to determine method
        @return: marmoset
        """
        self.browser = AnonBrowser(user_agents=DESKTOP_USER_AGENTS, cookiefile=self.cookiefile)
        self.username = username
        self.password = password

    def authenticate(self, username=None, password=None):
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

    def login(self, username=None, password=None):
        """
        Logs the user in

        @param self: The marmoset instance
        @return: tuple
        """
        self.username = username if username else self.username
        self.password = password if password else self.password
        self.browser.delete_cookies()
        self.browser.clear_cookies(self.cookiefile)

        return self.username, self.password

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

    def submit(self, course, assignment, files, zipname=None):
        """
        Submits a file to the specified assignment and course.

        @param self: The marmoset instance
        @param course: The course
        @param assignment: The assignment
        @param filename: The name of the file we're submitting.
        @return: None
        """
        if not self.authenticate():
            raise BrowserException("Invalid username/password combination for %s"%self.username)

        if not zipname:
            zipname = getattr(self, 'zipname', "%s.zip"% assignment)

        self.select_course(course)
        self.select_and_follow(assignment, 'submit')
        self.browser.select_form(nr = 0)

        # If multiple files, zip and submit
        if type(files) == list:
            filename = write_zip(zipname, files)
        else:
            filename = files

        self.browser.form.add_file(open(filename), 'text/plain', filename)
        self.browser.submit()

        if self.browser.geturl().find("/view/project.jsp?projectPK=") > -1:
            return True

        return False

    def get_num_release_tokens(self, course, assignment, submission=None):
        """
        Gets the number of release tokens the user has available to
        theme.

        @param self: The Marmoset instance
        @param course: The name of the course
        @param assignment: The assignment to look at
        @return: int
        """
        if not self.authenticate():
            raise BrowserException("Invalid username/password combination for %s"%self.username)

        self.select_course(course)
        self.select_and_follow(assignment, 'view')
        self.find_submission(submission)

        response = self.browser.reload()
        soup = BeautifulSoup(response.read())
        tokens = soup.find_all(lambda tag: tag.name == 'p' and re.search('^You currently have', tag.text))

        if len(tokens) == 0:
            raise BrowserException("This submission has no release tests.")
        elif type(tokens[0]) != str:
            tokens = list(token.text for token in tokens)
        tokens = re.search("[0-9]+", " ".join(tokens)).group(0)
        return int(tokens)

    def release(self, course, assignment, submission=None):
        """
        Release tests the specified submission for the assignment.

        @param self: The marmoset isntance
        @param assignment: The name of the assignment
        @param submission: The submission number
        @return: None
        """
        tokens = self.get_num_release_tokens(course, assignment, submission)
        response = self.browser.reload()
        soup = BeautifulSoup(response.read())
        release_link = soup.find_all(lambda tag: tag.name == 'a' and tag.text.find('Click here to release') > -1)

        if len(release_link) > 0 and tokens > 0:
            release_link = release_link[0]
            link = next(l for l in self.browser.links() if release_link.attrs['href'] == dict(l.attrs)['href'])
            submission = next(tag for tag in soup.find_all('h2') if tag.text.find('Submission') > -1)
            submission = submission.text.split()[1][:-1]
            self.browser.follow_link(link)
            self.browser.select_form(nr = 0)
            self.browser.submit()
            return True
        elif tokens == 0:
            raise BrowserException("Can't release test %s, %s tokens available."%(assignment, tokens))
        else:
            raise BrowserException("Can't release test %s at the moment."%(assignment))

        return False

    def long(self, course, assignment, submission=None):
        """
        Gets the detailed test results for a specified assingment based on the submission
        number.

        @param self: The marmoset instance
        @param assignment: The name of the assignment
        @param submission: The submission number
        @return: None
        """
        if not self.authenticate():
            raise BrowserException("Invalid username/password combination for %s"%self.username)

        self.select_course(course)
        self.select_and_follow(assignment, 'view')
        self.find_submission(submission)
        data = self.get_table(course, assignment)
        return data

    def fetch(self, course, assignment, submissions=5):
        """
        Fetches the n most recent short results for a specified assignment.

        @param self: The marmoset instance
        @param course: The name of the course
        @param assignment: The name of the assignment
        @return: None
        """
        if not self.authenticate():
            raise BrowserException("Invalid username/password combination for %s"%self.username)

        submissions = submissions if submissions else 5
        self.select_course(course)
        self.select_and_follow(assignment, 'view')
        data = self.get_table(course, assignment, submissions + 1)
        return data

    def download(self, course, assignment, submission=None, zipname=None):
        """
        Downloads the specified submission.  Defaults to the most recent
        submission.

        @param self: The marmoset instance
        @param course: The name of the course
        @param assignment: The name of the assignment
        @param submission: The submission number
        @param zipname: The name of the zipfile to create
        @return: File
        """
        if not self.authenticate():
            raise BrowserException("Invalid username/password combination for %s"%self.username)

        self.select_course(course)
        self.select_and_follow(assignment, 'view')

        f = None
        response = self.browser.reload()
        soup = BeautifulSoup(response.read())

        details = []
        rows = soup.find_all(lambda tag: tag.name == 'tr')
        for row in rows:
            if row.has_attr('class'):
                cell = row.find_all('td')[-2]
                cell = re.sub(r'[\t\n\r]+', ' ', cell.text)
                details.append(cell)
        links = soup.find_all(lambda tag: tag.name == 'a' and tag.text.find('download') > -1)
        links = list(l.attrs['href'] for l in links)
        submission = int(submission) if submission else len(links)

        # check possible error conditions
        if submission == 0:
            raise BrowserException("No submission 0")
        elif len(links) == 0:
            raise BrowserException("No submissions available.")
        elif submission > len(links) and submission > len(details):
            raise BrowserException("Invalid submission number %s" % submission)
        elif submission > len(links):
            index = (submission - 1) * -1
            raise BrowserException("Submission # %s %s "%(submission, details[index]))

        index = (submission - 1) * -1
        link = self.base_url + links[index]

        zipname = zipname if zipname else assignment + '.zip'
        f = self.browser.retrieve(link, zipname)[0]

        return f

    def find_submission(self, submission=None):
        """
        Finds the specified submission on the current page and follows the link.
        Defaults to last submission.

        @param self: The marmoset instance
        @param submission: The submission number
        @return: None
        """
        response = self.browser.reload()
        soup = BeautifulSoup(response.read())

        details = []
        rows = soup.find_all(lambda tag: tag.name == 'tr')
        for row in rows:
            if row.has_attr('class'):
                cell = row.find_all('td')[-2]
                cell = re.sub(r'[\t\n\r]+', ' ', cell.text)
                details.append(cell)
        links = soup.find_all(lambda tag: tag.name == 'a' and tag.text.find('view') > -1)
        links = list(link.attrs['href'] for link in links)

        index = -1 * (int(submission) if submission else len(details))
        submission = int(submission) if submission else len(details)

        # check possible error conditions
        if submission <= 0:
            raise BrowserException("No submission #%s"%submission)
        elif len(links) == 0:
            raise BrowserException("No submissions available.")
        elif submission > len(links) and submission > len(details):
            raise BrowserException("Invalid submission number %s" % submission)
        elif submission > len(links):
            raise BrowserException("Submission # %s %s "%(submission, details[index]))

        links = list(l for l in self.browser.links() if dict(l.attrs)['href'] in links)
        self.browser.follow_link(links[index])

    def get_assignment_deadline(self, course, assignment):
        """
        Gets the deadline of an assignment.  Returned as a datetime object.

        @param self: The marmoset instance
        @param course: The course we're looking at
        @param assignment: The assignment we're looking at
        @return: string
        """
        if not self.authenticate():
            raise BrowserException("Invalid username/password combination for %s"%self.username)

        self.select_course(course)
        self.select_and_follow(assignment, 'view')
        response = self.browser.reload();
        soup = BeautifulSoup(response)

        text = next(tag for tag in soup.find_all('p') if tag.text.find("Deadline") > -1).text.strip().split()
        deadline = [] if len(text) < 3 else text[:3]

        return deadline

    def get_table(self, course, assignment, number_of_rows=sys.maxint):
        """
        Gets the relevant data pertaining to a course

        @param self: The marmoset instance
        @param course: The course we're looking at
        @param assignment: The assignment we're looking at
        @param number_of_rows: The number of rows to return
        @return: dict
        """
        response = self.browser.reload()
        soup = BeautifulSoup(response)

        text = next(tag for tag in soup.find_all('p') if tag.text.find("Deadline") > -1).text.strip().split()
        deadline = [] if len(text) < 3 else text[:3]

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

        return data


def write_zip(name, files):
    """
    Writes a zip file and returns the name of the file.

    @param name: string, name of the file to create
    @param files: list of strings, name of files to zip
    """
    with ZipFile(name, 'w') as myzip:
        for f in files:
            if f == name:
                continue
            myzip.write(f)
    return name
