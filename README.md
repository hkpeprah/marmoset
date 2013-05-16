Marmoset
========
#####Author: hkpeprah


Marmoset is a submission server for University of Waterloo students.  The scripts here are for submitting and fetching assignments
from the server.  
Note: You will need the mechanize and BeautifulSoup modules installed to run the script(s).  If you do not have them, you will have to install them first.  You can do this by installing first the python setup tools (https://pypi.python.org/pypi/setuptools), then running the following two commands `sudo easy_install mechanize` and `sudo easy_install pyquery`.


###How-to-Use
Without compiling and using the executable or making the program executable, you can use the script in the following ways:
* Submit: `python marmoset -s coursename assignmentname filename` or `python marmoset --submit coursename assignmentname filename`
* Fetch: `python marmoset -f coursename assignment [number]` or `python marmoset --fetch coursname assignment [number]`
* Release: `python marmoset -r coursename assignment submission_number` or `python marmoset --release`
* Long Test: `python marmoset -l coursename assignment submission_number` or `python marmoset --long`

**NOTE**: The file `marmoset` is a standalone script, that can be placed in bin by itself and executed (it's a concatenation of the individual files).
If you make the script executable by using `chmod u+x marmoset`, you can execute it using `./marmoset`
Alternately, compile and run the executable (if not provided).


###Dependancies
* mechanize - Module for web browsing.
* pyquery - Use JQuery to parse web pages.


###To-do
* Test stuff.
