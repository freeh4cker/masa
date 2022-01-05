##########################################################################
# allow to filter MASA's freedivers given some criteria                  #
# Copyright (C) 2022  Bertrand Néron                                     #
#                                                                        #
# This file is part of filter_apnee package.                             #
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
import argparse

import pandas as pd


def parse_date(value):
    """

    :param str value: value parsed by command line parser
    :return: True if value can be parse as date
    :raises argparse.ArgumentTypeError: cannot be parsed as date
    """
    try:
        pd.to_datetime(value).normalize()
        return value
    except Exception as err:
        raise argparse.ArgumentTypeError(f"cannot parse '{value}' as date: {err}")


def file(value):
    """

    :param str value: value parsed by command line parser
    :return: True if value is a file
    :raises argparse.ArgumentTypeError: if value is not an existing file
    """
    if os.path.exists(value):
        if os.path.isfile(value):
            return value
        else:
            raise argparse.ArgumentTypeError(f"'{value}' is not a regular file")
    else:
        raise argparse.ArgumentTypeError(f"'{value}' no such file")



