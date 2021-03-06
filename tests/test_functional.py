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

import masa.scripts.masa_email as masa_email
from tests import MasaTest


class TestFunctional(MasaTest):

    def setUp(self) -> None:
        self.path = self.find_data('masa.tsv')

    def test_autonomie_absolue_piscine(self):
        cmd = "masa --autonomie-absolue-piscine 2021-12-30"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'titi@ap.org, bidule@acel.org, foo@aeel.org, bar@aeel.qs')

        cmd = "masa --autonomie-absolue-piscine 2022-07-31"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'bar@aeel.qs')

    def test_autonomie_relative_piscine(self):
        cmd = "masa --autonomie-relative-piscine 2021-12-30"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'titi@ap.org, titi.no_riffa@ap.org, tutu@acp.org, '
                         'truc@aeel.org, bidule@acel.org, foo@aeel.org, bar@aeel.qs')

    def test_fosse(self):
        cmd = "masa --fosse 2021-12-30"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'titi@ap.org, titi.no_riffa@ap.org, tutu@acp.org, tata@ael.org, '
                         'truc@aeel.org, bidule@acel.org, foo@aeel.org')

        cmd = "masa --fosse 2022-06-30"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'foo@aeel.org')

    def test_profondeur(self):
        cmd = "masa --profondeur 2021-12-30"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'toto@rien.org, titi@ap.org, titi.no_riffa@ap.org, tutu@acp.org, tata@ael.org, '
                         'truc@aeel.org, bidule@acel.org, foo@aeel.org')

        cmd = "masa --profondeur 2022-06-30"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'foo@aeel.org')

    def test_rifaa(self):
        cmd = 'masa --rifaa'
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'titi@ap.org, tata@ael.org, foo@aeel.org, bar@aeel.qs, null@aeel.void')
        
    def test_no_rifaa(self):
        cmd = 'masa --no-rifaa'
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'toto@rien.org, titi.no_riffa@ap.org, tutu@acp.org, truc@aeel.org, bidule@acel.org')

    def test_valid(self):
        cmd = "masa --valid 2021-12-30"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'toto@rien.org, titi@ap.org, titi.no_riffa@ap.org, tutu@acp.org, tata@ael.org, truc@aeel.org, '
                         'bidule@acel.org, foo@aeel.org, bar@aeel.qs')

        cmd = "masa --valid 2022-06-30"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'foo@aeel.org, bar@aeel.qs')

    def test_not_valid(self):
        cmd = "masa --not-valid 2021-12-30"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         '')

        cmd = "masa --not-valid 2022-01-15"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'toto@rien.org')

    def test_no_option(self):
        cmd = "masa"
        real_exit = masa_email.sys.exit
        masa_email.sys.exit = self.fake_exit
        try:
            with self.catch_io(out=True):
                with self.assertRaises(TypeError) as ctx:
                    masa_email.main(args=cmd.split()[1:])
                    usage = sys.stdout.getvalue().strip()
                    self.assertEqual(str(ctx.exception), '2')
                    self.assertEqual(usage,
                             """Please select an option

usage: masa [-h] [--autonomie-absolue-piscine [AUTONOMIE_ABSOLUE_PISCINE] | --autonomie-relative-piscine [AUTONOMIE_RELATIVE_PISCINE] | --fosse
            [FOSSE] | --rifaa | --no-rifaa | --valid [VALID] | --not-valid [NOT_VALID] | --warning [WARNING] | --all] [--version] [-v]""")

        finally:
            masa_email.sys.exit = real_exit

    def test_bad_date(self):
            cmd = "masa --valid 2022-30-01"
            real_exit = masa_email.sys.exit
            masa_email.sys.exit = self.fake_exit
            try:
                with self.catch_io(err=True):
                    with self.assertRaises(TypeError) as ctx:
                        masa_email.main(args=cmd.split()[1:])
                        usage = sys.stderr.getvalue().strip()
                        self.assertEqual(str(ctx.exception), '2')
                        self.assertEqual(usage,
                                         """usage: masa [-h] [--autonomie-absolue-piscine [AUTONOMIE_ABSOLUE_PISCINE] | --autonomie-relative-piscine [AUTONOMIE_RELATIVE_PISCINE] | --fosse [FOSSE] | --rifaa |
            --no-rifaa | --valid [VALID] | --not-valid [NOT_VALID] | --warning [WARNING] | --all] [--version] [-v]
masa: error: argument --valid: cannot parse '2022-30-01' as date: month must be in 1..12: 2022-30-01""")

            finally:
                masa_email.sys.exit = real_exit

    def test_all(self):
        cmd = "masa --all"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'toto@rien.org, titi@ap.org, titi.no_riffa@ap.org, tutu@acp.org, tata@ael.org, truc@aeel.org, '
                         'bidule@acel.org, foo@aeel.org, bar@aeel.qs, null@aeel.void')

    def test_ligne(self):
        cmd = "masa --all --l1"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'toto@rien.org, titi@ap.org, titi.no_riffa@ap.org, truc@aeel.org')

        cmd = "masa --all --l2"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'tutu@acp.org, tata@ael.org, bidule@acel.org, foo@aeel.org, bar@aeel.qs, null@aeel.void')

    def test_verbose(self):
        cmd = "masa --all -v"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         '"rien TOTO" <toto@rien.org>, "ap-rien TITI" <titi@ap.org>, '
                         '"ap-rien-no-riffa TITI" <titi.no_riffa@ap.org>, '
                         '"acp-rien TUTU" <tutu@acp.org>, '
                         '"rien-ael TATA" <tata@ael.org>, '
                         '"ap-ael truc" <truc@aeel.org>, '
                         '"ap-acel bidule" <bidule@acel.org>, '
                         '"ap-aeel foo" <foo@aeel.org>, '
                         '"ap-aeel bar" <bar@aeel.qs>, '
                         '"ap-aeel nulle" <null@aeel.void>')

        cmd = "masa --all -vv"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails, """rien TOTO                A-13-000001  rien/rien  NO RIFAA  CACI      2021-01-01  L1 toto@rien.org
ap-rien TITI             A-13-000011  AP/rien    RIFAA     CACI      2021-02-01  L1 titi@ap.org
ap-rien-no-riffa TITI    A-13-000111  AP/rien    NO RIFAA  CACI      2021-02-01  L1 titi.no_riffa@ap.org
acp-rien TUTU            A-13-001111  ACP/rien   NO RIFAA  CACI      2021-03-01  L2 tutu@acp.org
rien-ael TATA            A-13-011111  rien/AEL   RIFAA     CACI      2021-04-01  L2 tata@ael.org
ap-ael truc              A-13-111111  AP/AEL     NO RIFAA  CACI      2021-05-01  L1 truc@aeel.org
ap-acel bidule           A-13-000002  AP/ACEL    NO RIFAA  CACI      2021-06-01  L2 bidule@acel.org
ap-aeel foo              A-13-000012  AP/AEEL    RIFAA     CACI      2021-07-01  L2 foo@aeel.org
ap-aeel bar              A-13-000122  AP/AEEL    RIFAA     QS        2021-08-01  L2 bar@aeel.qs
ap-aeel nulle            A-13-001222  AP/AEEL    RIFAA     NO certif 2021-08-01  L2 null@aeel.void""")

    def test_data_file(self):
        data_path = self.find_data('masa.tsv')
        cmd = f"masa --all --l1 --data {data_path}"
        with self.catch_io(out=True):
            masa_email.main(args=cmd.split()[1:])
            emails = sys.stdout.getvalue().strip()
        self.assertEqual(emails,
                         'toto@rien.org, titi@ap.org, titi.no_riffa@ap.org, truc@aeel.org')