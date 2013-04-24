Marmoset
========
#####Author: hkpeprah


Marmoset is a submission server for University of Waterloo students.  The scripts here are for submitting and fetching assignments
from the server.


###How-to-Use
Without compiling and using the executable or making the program executable, you can use the script in the following ways:
* Submit: `python marmoset.py -s coursename assignmentname filename` or `python marmoset.py --submit coursename assignmentname filename`
* Fetch: `python marmoset.py -f coursename assignment [number]` or `python marmoset.py --fetch coursname assignment [number]`
If you make the script executable by using `chmod u+x marmoset.py`, you can execute it using `./marmoset.py`
Alternately, compile and run the executable (if not provided).