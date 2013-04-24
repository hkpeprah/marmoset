Marmoset
========
#####Author: hkpeprah


Marmoset is a submission server for University of Waterloo students.  The scripts here are for submitting and fetching assignments
from the server.  
Note: You will need the mechanize and BeautifulSoup modules installed to run the script(s).  If you do not have them, you will have to install them first.  You can do this by installing first the python setup tools (https://pypi.python.org/pypi/setuptools), then running the following two commands `sudo easy_install mechanize` and `sudo easy_install BeautifulSoup`.


###How-to-Use
Without compiling and using the executable or making the program executable, you can use the script in the following ways:
* Submit: `python marmoset.py -s coursename assignmentname filename` or `python marmoset.py --submit coursename assignmentname filename`
* Fetch: `python marmoset.py -f coursename assignment [number]` or `python marmoset.py --fetch coursname assignment [number]`
If you make the script executable by using `chmod u+x marmoset.py`, you can execute it using `./marmoset.py`
Alternately, compile and run the executable (if not provided).


###Dependancies
* mechanize - Module for web browsing.
* BeautifulSoup - Module for parsing web pages.
* cookielib - Used for interacting with web session cookies; Marmoset uses cookies to keep track of login.