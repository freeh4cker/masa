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

import sys
from time import strftime, localtime
import pkg_resources


__version__ = strftime("%Y%m%d", localtime())
__DATA__ = pkg_resources.resource_filename('masa', "data")


def get_version_message():
    from numpy import __version__ as np_vers
    from pandas import __version__ as pd_vers
    version_text = """masa version {masa}
Using:
 - Python {py}
 - numpy {np}
 - pandas {pd}

Authors:
 - Bertrand Neron

masa is distributed under the terms of the GNU General Public License (GPLv3).
See the COPYING file for details.
""".format(masa=__version__,
           py=sys.version.replace('\n', ' '),
           np=np_vers,
           pd=pd_vers,
           )

    return version_text