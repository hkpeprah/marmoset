"""marmosetSubmit.py - Submit code to marmoset using this script.
   author: hkpeprah
"""

import re, getpass, string, mechanize, cookielib, os, sys
from pyquery import PyQuery
from anonBrowser import *

marmoset_url="http://marmoset.student.cs.uwaterloo.ca"
cas_url = "http://www.cas.uwaterloo.ca"

"""Initalize the cookies and browser."""
browser = anonBrowser()
cookie_file = "/tmp/marmosetCookies"
cookies = cookielib.MozillaCookieJar(cookie_file)
browser.set_cookiejar(cookies)


"""Helper Functions"""
findclass = lambda html, course: [ i.attr('href') for i in PyQuery(html).items('a') if not(re.match(course + " \(", i.text(), re.I) == None) ]
findassignment = lambda assignment: re.compile('<a href="(.*)">\s+' + assignment + '\s+</a>\s+</td>\s+<td> <a href="(.*)"> view </a></td>\s+<td> <a href="(.*)"> submit </a>', re.I)
findassignments = lambda assignment: re.compile('<a href="(.*)">\s+' + assignment + '.*\s+</a>\s+</td>\s+<td> <a href="(.*)"> view </a></td>\s+<td> <a href="(.*)"> submit </a>', re.I)

def sigerr( num ):
    """signal an error and quit"""
    if ( num == 0 ): print "Invalid login credentials."
    elif ( num == 1 or num == 2 ): print "%s not found.  Are you sure you entered correctly?"%( "Course" if num == 1 else "Assignment" )
    elif ( num == 3 ): print "Multiple courses found for query.  Are you sure you entered correctly?"
    elif ( num == 4 ): print "Submission not found."
    exit(0)


def login():
    """Returns browser if login failed or succeeded.  Attempt to connct, if connection fail
    prompt for credentials.  If connection/credentials fail, return None."""
    if ( os.path.exists( cookie_file ) ): cookies.load(ignore_discard = True, ignore_expires = True)
    browser.open(marmoset_url)
    if ( string.find(browser.geturl(), "cas") == -1 ):
        return browser
    else:
        """Prompt for credentials"""
        browser.select_form(nr = 0)
        browser.form['username'] = str(raw_input("Enter your username: "))
        browser.form['password'] = getpass.getpass("Enter your password: ")
        """Submit form, attempt connection again."""
        browser.submit()
        browser.open(marmoset_url)
        if ( string.find(browser.geturl(), "cas") == -1 ):
            cookies.save(cookie_file, ignore_discard=True, ignore_expires=True)
            return browser
    return None


def coursepage( course ):
    """navigate to the marmoset course page for a course."""
    marmoset = login()
    if ( marmoset == None ): sigerr(0)
    try:
        """Try to submit the assignment.
        We start by jumping to the course selection page by submitting."""
        new_url = marmoset_url + "/view/index.jsp"
        marmoset.open(new_url)
        marmoset.select_form(nr = 0)
        marmoset.submit()
        """Check if the course exists, if not, return error."""
        html  = marmoset.open(new_url).read()
        link = findclass(html, course) 
        if link == []: sigerr(1)
        else:
            return (marmoset, marmoset_url + link[0])
    except Exception as e:
        print "Something went wrong, manually submit."
        exit(0)


def marmoset_submit( course, assignment, fname ):
    """When given a course name, assignment name, and file name, attempts to submit
    the file to the respective course on Marmoset."""
    try:
        data = coursepage( course )
        marmoset = data[0]
        html = marmoset.open(data[1]).read()
        link = findassignment(assignment).search(html)
        if link == None: sigerr(2)
        else:
            """Jump to the submit page and try to submit"""
            new_url = marmoset_url + link.group(3)
            marmoset.open(new_url)
            marmoset.select_form(nr = 0)
            marmoset.form.add_file(open(fname), 'text/plain', fname)
            marmoset.submit()
    except Exception as e:
        print "Something went wrong, manually submit."
        exit(0)
    print "Successfully submitted assignment %s"%(assignment)
    return None


def marmoset_fetch( course, asmt, num = 3 ):
    """Fetches the marks for the assignment(s) in the given course.  If there is more than
    one match, it fetches the top marks for all the matching assignments, otherwise, the top
    three for the matching assignment are fetched."""
    try:
        data = coursepage( course )
        marmoset = data[0]
        html = marmoset.open(data[1]).read()
        assignments = findassignments(asmt).findall(html)
        """marks are a match of form Row Class, ID, Date, Score"""
        marks = re.compile('<tr class="(.*)">\s+<td>(.*)</td>\s+<td>(.*)</td>\s+<td>\s+(.*)\s+</td>(\s+<td>\s*(.*) / (.*)\s*</td>)?', re.I)
        for assignment in assignments:
            """Print the top marks.  Get the assignment page then parse."""
            page = marmoset.open(marmoset_url + assignment[1]).read()
            grades = re.findall(marks, page)
            title = re.compile('<title>(.*)</title>').search(page).group(1).replace("All", "Most Recent")
            print title
            for i in range(0, min(num, len(grades))):
                print "%s %30s %15s %15s"%(grades[i][1], grades[i][2], grades[i][3], 
                                           ("" if grades[i][5] == "" else str(grades[i][5]) + " / " + str(grades[i][6])))
    except Exception as e:
        print e
        print "Something went wrong.  Manually check."
        exit(0)
    return None


def marmoset_long( course, assignment, submission = None, release = False ):
    """displays the long test result for a submission.  if no number is given, returns the long
    test result for the most recent submission"""
    try:
        data = coursepage( course )
        marmoset = data[0]
        html = marmoset.open(data[1]).read()
        link = findassignment(assignment).search(html)
        if link == None: sigerr(2)
        else:
            page = marmoset.open(marmoset_url + link.group(2)).read()
            long_url = re.compile('<td><a href="(.*)">view</a></td>').findall(page)
            if (len(long_url) == 0) or (not(submission == None) and (submission > len(long_url) or submission < 0)): 
                sigerr(4)
            long_url = (long_url[0] if submission == None else long_url[len(long_url) - submission])
            page = marmoset.open(marmoset_url + long_url).read()
            """print out the table now if release is false, otherwise we want to return where we are."""
            if release: return (marmoset, marmoset_url + long_url)
            details = (re.compile('<p>You received [0-9]+/[0-9]+ points for public test cases.').search(page).group(0).replace("<p>",""),
                       re.compile('<p>You currently have [0-3]+ release').search(page).group(0).replace("<p>",""))
            rows = re.compile('<th>(.*)</th>').findall(page) + re.compile('<td>(.*)</td>').findall(page)
            print "Project %s: Test Results for Submission %d"%(assignment, (len(long_url) if submission == None else submission))
            for col in xrange(0, len(rows)):
                if rows[col] == "public" or rows[col] == "release": print
                print "%-*s"%(15, rows[col]),
            print "\n\n%s\n%s tokens available."%(details[0], details[1])
    except Exception as e:
        print "Something went wrong, manually look up."
        exit(0)
    return None


def marmoset_release( course, assignment, submission = None ):
    """fire off a release test for an assignment. upper limit of 99 submissions to be displayed."""
    data = marmoset_long( course, assignment, submission, True )
    try:
        marmoset = data[0]
        page = marmoset.open(data[1]).read()
        release_url = re.compile('<a href="(.*)"> Click here to release test').search(page)
        if release_url == None: 
            print "Sorry, can't release test.  No release tokens available."
            return None
        else:
            marmoset.open(marmoset_url + release_url.group(1))
            marmoset.select_form(nr = 0)
            marmoset.submit()
    except Exception as e:
        print "Something went wrong, manually release."
        exit(0)
    print "Release testing was successful."
    return None
