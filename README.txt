========
Marmoset
========

Marmoset provides a tool for interacting with the Marmoset submission server; submitting
files, fetching results and release testing submissions.  Typical usage looks like this.

    $ marmoset --submit cs246 a11p4 a11p4.cpp
    Succesfully submitted a11p4.cpp to a11p4.

    $ marmoset --release cs246 a11p4 0
    You have 3 release tokens left.
    Release test this submission [y/n]? y
    Successfully release tested submission #0 for a11p4.

It can also be imported and used.

    #!/usr/bin/env python
    from marmoset import marmoset

    m = marmoset(username=username, password=password)
    m.submit('cs246', 'a11p4', 'a11p4.cpp')


