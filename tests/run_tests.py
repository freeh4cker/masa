##########################################################################
# allow to filter MASA's freedivers given some criteria                  #
# Copyright (C) 2022  Bertrand Néron                                     #
#                                                                        #
# This file is part of masa package.                                     #
#                                                                        #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################

import os
import sys
import unittest


def discover(test_files=None, test_root_path=None):
    if not test_root_path:
        test_root_path = os.path.dirname(__file__)

    if not test_files:
        suite = unittest.TestLoader().discover(test_root_path, pattern="test_*.py")

    else:
        test_files = [os.path.abspath(f) for f in test_files]
        test_files = [t for t in test_files if test_root_path in t]
        suite = unittest.TestSuite()
        for test_file in test_files:
            if os.path.exists(test_file):
                if os.path.isfile(test_file):
                    fpath, fname = os.path.split(test_file)
                    suite.addTests(unittest.TestLoader().discover(fpath, pattern=fname))
                elif os.path.isdir(test_file):
                    suite.addTests(unittest.TestLoader().discover(test_file))
            else:
                sys.stderr.write(f"{test_file} : no such file or directory\n")

    return suite


def run_tests(test_files, verbosity=0):
    """
    Execute Unit Tests
    :param test_files: the file names of tests to run.
                       if it is empty, discover recursively tests from 'tests' directory.
                       a test is a python module with the test_*.py pattern
    :type test_files: list of string
    :param verbosity: the verbosity of the output
    :type verbosity: positive int
    :return: True if the test passed successfully, False otherwise.
    :rtype: bool
    """
    test_root_path = os.path.abspath(os.path.dirname(__file__))
    suite = discover(test_files, test_root_path)
    test_runner = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return test_runner


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("tests",
                        nargs='*',
                        default=False,
                        help="name of test to execute")

    parser.add_argument("-v", "--verbose",
                        dest="verbosity",
                        action="count",
                        help="set the verbosity level of output",
                        default=0
                        )

    args = parser.parse_args(args)

    old_path = sys.path

    test_runner = run_tests(args.tests, verbosity=args.verbosity)
    unit_results = test_runner.wasSuccessful()
    sys.path = old_path
    return unit_results


if __name__ == '__main__':

    unit_results = main(sys.argv[1:])
    if unit_results:
        sys.exit(0)
    else:
        sys.exit(1)
