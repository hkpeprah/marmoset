========
Marmoset
========

Marmoset provides a tool for interacting with the Marmoset submission server; submitting
files, fetching results and release testing submissions.


usage: marmoset [-h] [-v] {download,fetch,keyring,long,release,submit} ...

A command line tool for interacting with the Marmoset Submission Server.
-------------------------------------------------------------------------

optional arguments:
  -h, --help                  show this help message and exit
  -v, --version               show program's version number and exit

commands:
  {download,fetch,keyring,long,release,submit}
    download                  download the most recent submission(s). Defaults
                              to last/latest
    fetch                     fetch the most recent submission(s). Defaults to
                              last/latest
    keyring                   modify the marmoset keyring
    long                      long the most recent submission(s). Defaults to
                              last/latest
    release                   release the most recent submission(s). Defaults
                              to last/latest
    submit                    submit file(s) to the marmoset submission server


usage: marmoset download [-h] [-u username] [-n] [-z zipname]
                         course assignment [submission]

positional arguments:
  course                specify a course
  assignment            specify an assignment
  submission            specific submission or number of submissions

optional arguments:
  -h, --help            show this help message and exit
  -u username, --username username
                        user to login as, defaults to the default user
  -n, --nosave          don't save the user being logged in as
  -z zipname, --zipname zipname
                        name of the zipfile to submit/download


usage: marmoset fetch [-h] [-u username] [-n] course assignment [submission]

positional arguments:
  course                specify a course
  assignment            specify an assignment
  submission            specific submission or number of submissions

optional arguments:
  -h, --help            show this help message and exit
  -u username, --username username
                        user to login as, defaults to the default user
  -n, --nosave          don't save the user being logged in as


usage: marmoset keyring [-h] [-a] [-c] [-r] username

positional arguments:
  username          marmoset username

optional arguments:
  -h, --help        show this help message and exit

keyring utilities:
  -a, --adduser     add a user to the marmoset keyring
  -c, --changeuser  change the default user in the marmoset keyring
  -r, --removeuser  remove a user from the marmoset keyring


usage: marmoset long [-h] [-u username] [-n] course assignment [submission]

positional arguments:
  course                specify a course
  assignment            specify an assignment
  submission            specific submission or number of submissions

optional arguments:
  -h, --help            show this help message and exit
  -u username, --username username
                        user to login as, defaults to the default user
  -n, --nosave          don't save the user being logged in as


usage: marmoset release [-h] [-u username] [-n] course assignment [submission]

positional arguments:
  course                specify a course
  assignment            specify an assignment
  submission            specific submission or number of submissions

optional arguments:
  -h, --help            show this help message and exit
  -u username, --username username
                        user to login as, defaults to the default user
  -n, --nosave          don't save the user being logged in as


usage: marmoset submit [-h] [-u username] [-n] [-z zipname]
                       course assignment files [files ...]

positional arguments:
  course                specify a course
  assignment            specify an assignment
  files                 one or more files to submit

optional arguments:
  -h, --help            show this help message and exit
  -u username, --username username
                        user to login as, defaults to the default user
  -n, --nosave          don't save the user being logged in as
  -z zipname, --zipname zipname
                        name of the zipfile to submit/download
