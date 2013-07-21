import os
import subprocess


def check_expect (command, testdir, expectdir):
    """
    Runs the tests in the testdir against the command and checks
    the results against the expected results in the expectdir.
    E.g. test named "test0.in" should have a corresponding
    "test1.out".

    @param command: The command to execute the test with.
    @param testdir: Directory of tests.
    @param expectdir: Directory of expected results.
    @return: boolean
    """
    root = os.getcwd()

    for (dirpath, dirnames, tests) in os.walk(testdir, followlinks=True):
        results = []

        for test in tests:
            testpath = os.path.join(dirpath, test)
            expect = os.path.join(dirpath.replace(testdir, expectdir), test.replace(".in", ".out"))
            if not os.path.exists(expect):
                raise Exception("Could not find the expected test results.")
            else:
                expected = open(expect, 'r').read().split("\n")
                cmd = "{0} < {1}".format(command, testpath)
                actual = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                (stdout, stderr) = actual.communicate()
                actual = stdout.split("\n")

                if stderr:
                    raise Exception(stderr)

                i = 0
                for j in range(0, min(len(actual), len(expected))):
                    if not actual[0] == expected[0]:
                        results.append("{0} Actual: {1}".format(i, actual[0]))
                        results.append("{0} Expected: {1}".format(i, expected[0]))
                    actual, expected = actual[1:], expected[1:]
                    i = j + 1

                for j in range(0, max(len(actual), len(expected))):
                    results.append("{0} {1}: {2}".format(i, *(("Actual", actual[0]) if len(actual) > 0 else
                                                              ("Expected", expected[0]))))

    if len(results) > 0:
        return {'success': False, 'results': results}

    return {'success': True, 'results': []}
