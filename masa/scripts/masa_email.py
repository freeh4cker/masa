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

import sys
import os
import argparse
from textwrap import dedent

import masa
import masa.utils
from masa import parse


def parse_args(args):
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description=dedent("""
 __  __    _    ____    _    
|  \/  |  / \  / ___|  / \   
| |\/| | / _ \ \___ \ / _ \  
| |  | |/ ___ \ ___) / ___ \ 
|_|  |_/_/   \_\____/_/   \_\\  freediver filtering software
    
    
"""))
    exclusive_opt = parser.add_mutually_exclusive_group()
    exclusive_opt.add_argument('--autonomie-absolue-piscine',
                        nargs='?',
                        type=masa.utils.parse_date,
                        const='today',
                        help="""list of emails with valid CACI or QS at the specified date (yyyy-mm-dd) 
and allow to dive in autonomie absolue in pool (default=today)""")
    exclusive_opt.add_argument('--autonomie-relative-piscine',
                        nargs='?',
                        const='today',
                        help="""list of emails with valid CACI or QS at the specified date (yyyy-mm-dd) 
and allow to dive in autonomie relative in pool (default=today)""")
    exclusive_opt.add_argument('--fosse',
                        nargs='?',
                        type=masa.utils.parse_date,
                        const='today',
                        help="""list of emails with valid CACI or QS at the specified date (yyyy-mm-dd) 
and allow to dive at VLG (default=today)""")
    exclusive_opt.add_argument('--profondeur',
                               nargs='?',
                               type=masa.utils.parse_date,
                               const='today',
                               help="""list of emails with valid CACI at the specified date (yyyy-mm-dd) 
(default=today)""")
    exclusive_opt.add_argument('--rifaa',
                        action='store_true',
                        default=False,
                        help="freedivers who held RIFAA"
                        )
    exclusive_opt.add_argument('--no-rifaa',
                        action='store_true',
                        default=False,
                        help="freedivers who do NOT held RIFAA"
                        )
    exclusive_opt.add_argument('--valid',
                        nargs='?',
                        type=masa.utils.parse_date,
                        const='today',
                        help="list of emails with valid CACI or QS at the specified date (yyyy-mm-dd) (default=today)")
    exclusive_opt.add_argument('--not-valid',
                        nargs='?',
                        type=masa.utils.parse_date,
                        const='today',
                        help="list of emails with NO valid CACI or QS at the specified date (yyyy-mm-dd) (default=today)")
    exclusive_opt.add_argument('--warning',
                        nargs='?',
                        type=int,
                        const=15,
                        help="""list of emails with valid CACI or QS today but
expire at today + delta time (in days) (default=15 days)""")
    exclusive_opt.add_argument('--all',
                        action='store_true',
                        default=False,
                        help="""list of emails of all freedivers""")
    ligne_opt = parser.add_mutually_exclusive_group()
    ligne_opt.add_argument('--l1',
                           dest='ligne_1',
                           action='store_true',
                           default=False,
                           help="""Filter only divers in Ligne 1. 
- This option must be combined with previous ones.
- This option is mutually exclusive with --L2"""
                           )
    ligne_opt.add_argument('--l2',
                           dest='ligne_2',
                           action='store_true',
                           default=False,
                           help="""Filter only divers in Ligne 2. 
- This option must be combined with previous ones.
- This option is mutually exclusive with --L1"""
                           )
    parser.add_argument('--data',
                        type=masa.utils.file,
                        help="""The path to the 'masa.tsv' data file, by default provide with release"""
                        )
    parser.add_argument("--version",
                        action="version",
                        version=masa.get_version_message()
                        )
    parser.add_argument('-v', "--verbose",
                        default=0,
                        action="count",
                        help="""increase verbosity
-v displays email in long version "Prenom Nom" <email>'
-vv displays all info Prenom Nom licence indoor/outdoor rifaa CACI|QS date email"""
                        )
    parsed_args = parser.parse_args(args)
    return parser, parsed_args


def main(args=None):
    args = sys.argv[1:] if args is None else args
    parser, parsed_args = parse_args(args)

    if parsed_args.data:
        data_file = parsed_args.data
    else:
        data_file = os.path.join(masa.__DATA__, 'masa.tsv')

    data = parse.parse_data(data_file)
    if parsed_args.autonomie_absolue_piscine:
        selection = parse.autonomie_absolue_piscine(data, target_date=parsed_args.autonomie_absolue_piscine)
    elif parsed_args.autonomie_relative_piscine:
        selection = parse.autonomie_relative_piscine(data, target_date=parsed_args.autonomie_relative_piscine)
    elif parsed_args.fosse:
        selection = parse.fosse(data, target_date=parsed_args.fosse)
    elif parsed_args.profondeur:
        selection = parse.profondeur(data, target_date=parsed_args.profondeur)
    elif parsed_args.rifaa:
        selection = parse.rifaa(data)
    elif parsed_args.no_rifaa:
        selection = parse.no_rifaa(data)
    elif parsed_args.valid:
        selection = parse.certif_valid_at(data, target_date=parsed_args.valid)
    elif parsed_args.not_valid:
        selection = parse.certif_not_valid_at(data, target_date=parsed_args.not_valid)
    elif parsed_args.warning:
        selection = parse.warning(data, time_delta=parsed_args.warning)
    elif parsed_args.all:
        selection = data
    else:
        print("Please select an option\n")
        parser.print_usage()
        sys.exit(2)

    if parsed_args.ligne_1:
        selection = parse.ligne(selection, ligne=1)
    elif parsed_args.ligne_2:
        selection = parse.ligne(selection, ligne=2)

    if parsed_args.verbose == 0:
        emails = parse.to_emails(selection, verbose=False)
        sep = ', '
    elif parsed_args.verbose == 1:
        emails = parse.to_emails(selection, verbose=True)
        sep = ', '
    else:
        emails = parse.to_string(selection)
        sep = '\n'

    print(sep.join(emails))

