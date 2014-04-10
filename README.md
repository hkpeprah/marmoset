Marmoset
========
###Download
Check the releases section.


Description
-----------
Marmoset is a submission server for University of Waterloo CS (Computer Science) students for submitting their programming assignments.  The purpose of this package is to allow users to submit assignments and fetch results through a commandline interface.  


Installation
------------
* With `pip` (Python Installation Package): `sudo pip install Marmoset.tar.gz`
* With `easy_install`: `easy_install Marmoset.tar.gz`

**Note**: This package has dependencies on three Python packages, if you don't have `setuptools` installed, installation is a lot more difficult and not natively supported.


Dependencies
------------
* mechanize
* beautifulsoup4
* keyring


Usage
-----

| Command    | Arguments                         | Description                                                           | 
| -----------| --------------------------------- | --------------------------------------------------------------------- |
| download   | course assignment [submission]    | Downloads the specified submission.  Defaults to last.                |
| fetch      | course assignment [N]             | Fetches the last N submissions.  Defaults to 5.                       |
| keyring    | username                          | Perform operations on the marmoset keyring.                           |
| long       | course assignment [submission]    | Get the long results for the specified submission.  Defaults to last. |
| release    | course assignment [submission]    | Release test the specified submission.  Defaults to the last.         |
| submit     | course assignment file [file...]  | Submit the listed file(s) to the specified assignment.                |

Commands have additional optional arguments and flags.  For full help run `marmoset --help` or `marmoset CMD --help` for the specific command.

Typical usage looks like this:

    $ marmoset submit cs246 a11p4 a11p4.cpp
    Succesfully submitted a11p4 for cs246

    $ marmoset --release cs246 a11p4 1
    You have 3 release tokens left.
    Release test this submission [y/n]? y
    Successfully release tested submission #1 for a11p4.

It can also be imported and used:

    from marmoset import Marmoset

    m = Marmoset(username=username, password=password)
    m.submit('cs246', 'a11p4', 'a11p4.cpp')


License
-------
    Marmoset Submission Script
    The Marmoset submission script allows users to submit and test their
    programs to the University of Waterloo Marmoset server.
    Copyright (C) 2012-2013  Ford Peprah

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
