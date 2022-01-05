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

import argparse

import masa.utils
from tests import MasaTest


class TestUtils(MasaTest):

    def setUp(self) -> None:
        self.path = self.find_data('masa.tsv')

    def test_parse_date(self):
        date = '2002-02-25'
        self.assertTrue(masa.utils.parse_date(date))
        date = 'today'
        self.assertTrue(masa.utils.parse_date(date))
        date = '2002-25-02'
        with self.assertRaises(argparse.ArgumentTypeError) as ctx:
            masa.utils.parse_date(date)
        self.assertEqual(str(ctx.exception),
                         "cannot parse '2002-25-02' as date: month must be in 1..12: 2002-25-02")

    def test_file(self):
        path = self.find_data('masa.tsv')
        self.assertTrue(masa.utils.file(path))

        path = self.find_data()
        with self.assertRaises(argparse.ArgumentTypeError) as ctx:
            masa.utils.file(path)
        self.assertEqual(str(ctx.exception),
                         f"'{path}' is not a regular file")

        path = 'nimportnaoik.foo'
        with self.assertRaises(argparse.ArgumentTypeError) as ctx:
            masa.utils.file(path)
        self.assertEqual(str(ctx.exception),
                         f"'{path}' no such file")