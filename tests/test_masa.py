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

import datetime

import pandas as pd
import pandas.api.types

from masa import parse
from tests import MasaTest


class TestMasa(MasaTest):

    def setUp(self) -> None:
        self.path = self.find_data('masa.tsv')

    def generate_date(self, date, nb):
        serie = pd.Series([pd.to_datetime(date).normalize() for _ in range(nb)])
        return serie

    def test_parse_data(self):
        data = parse.parse_data(self.path)
        self.assertEqual(data.shape, (10, 11))
        self.assertEqual(data.columns.to_list(),
                         ['nom', 'prenom', 'email', 'licence', 'indoor', 'outdoor', 'rifaa', 'CACI', 'QS', 'date', 'ligne']
                         )
        self.assertTrue(pandas.api.types.is_datetime64_dtype(data.date.dtypes))

    def test_to_emails(self):
        data = parse.parse_data(self.path)
        got_emails = parse.to_emails(data)
        self.assertListEqual(
            got_emails,
            ['toto@rien.org', 'titi@ap.org', 'titi.no_riffa@ap.org', 'tutu@acp.org', 'tata@ael.org', 'truc@aeel.org', 'bidule@acel.org',
             'foo@aeel.org', 'bar@aeel.qs', 'null@aeel.void']
        )
        got_emails = parse.to_emails(data, verbose=True)
        self.assertListEqual(
            got_emails,
            ['"rien TOTO" <toto@rien.org>', '"ap-rien TITI" <titi@ap.org>', '"ap-rien-no-riffa TITI" <titi.no_riffa@ap.org>', '"acp-rien TUTU" <tutu@acp.org>',
             '"rien-ael TATA" <tata@ael.org>', '"ap-ael truc" <truc@aeel.org>', '"ap-acel bidule" <bidule@acel.org>',
             '"ap-aeel foo" <foo@aeel.org>', '"ap-aeel bar" <bar@aeel.qs>', '"ap-aeel nulle" <null@aeel.void>']
        )

    def test_to_string(self):
        data = parse.parse_data(self.path)
        data_str = parse.to_string(data)
        expected = [
            "rien TOTO                A-13-000001  rien/rien  NO RIFAA  CACI      2021-01-01  L1 toto@rien.org",
            "ap-rien TITI             A-13-000011  AP/rien    RIFAA     CACI      2021-02-01  L1 titi@ap.org",
            "ap-rien-no-riffa TITI    A-13-000111  AP/rien    NO RIFAA  CACI      2021-02-01  L1 titi.no_riffa@ap.org",
            "acp-rien TUTU            A-13-001111  ACP/rien   NO RIFAA  CACI      2021-03-01  L2 tutu@acp.org",
            "rien-ael TATA            A-13-011111  rien/AEL   RIFAA     CACI      2021-04-01  L2 tata@ael.org",
            "ap-ael truc              A-13-111111  AP/AEL     NO RIFAA  CACI      2021-05-01  L1 truc@aeel.org",
            "ap-acel bidule           A-13-000002  AP/ACEL    NO RIFAA  CACI      2021-06-01  L2 bidule@acel.org",
            "ap-aeel foo              A-13-000012  AP/AEEL    RIFAA     CACI      2021-07-01  L2 foo@aeel.org",
            "ap-aeel bar              A-13-000122  AP/AEEL    RIFAA     QS        2021-08-01  L2 bar@aeel.qs",
            "ap-aeel nulle            A-13-001222  AP/AEEL    RIFAA     NO certif 2021-08-01  L2 null@aeel.void",
        ]
        self.maxDiff = None
        self.assertListEqual(data_str.to_list(),
                             expected)

    def test_autonomie_absolue_piscine(self):
        data = parse.parse_data(self.path)
        today = self.generate_date('today', len(data))
        data.date = today
        aap = parse.autonomie_absolue_piscine(data)
        self.assertEqual(list(aap.index),
                         [1, 6, 7, 8])

        today = datetime.date.today()
        delta = datetime.timedelta(days=366)
        expired_date = today + delta
        arp = parse.autonomie_absolue_piscine(data, target_date=str(expired_date))
        self.assertEqual(list(arp.index),
                         [])

    def test_autonomie_relative_piscine(self):
        data = parse.parse_data(self.path)
        today = self.generate_date('today', len(data))
        data.date = today
        arp = parse.autonomie_relative_piscine(data)
        self.assertEqual(list(arp.index),
                         [1, 2, 3, 5, 6, 7, 8])                                                                      #

        today = datetime.date.today()
        delta = datetime.timedelta(days=366)
        expired_date = today + delta
        arp = parse.autonomie_relative_piscine(data, target_date=str(expired_date))
        self.assertEqual(list(arp.index),
                         [])

    def test_fosse(self):
        data = parse.parse_data(self.path)
        today = self.generate_date('today', len(data))
        data.date = today
        fosse = parse.fosse(data)
        self.assertEqual(list(fosse.index),
                         [1, 2, 3, 4, 5, 6, 7])
        today = datetime.date.today()
        delta = datetime.timedelta(days=366)
        expired_date = today - delta
        expired_date = pd.to_datetime(expired_date).normalize()
        data.loc[1, 'date'] = expired_date
        fosse = parse.fosse(data)
        self.assertEqual(list(fosse.index),
                         [2, 3, 4, 5, 6, 7])

    def test_profondeur(self):
        data = parse.parse_data(self.path)
        today = self.generate_date('today', len(data))
        data.date = today
        fosse = parse.profondeur(data)
        self.assertEqual(list(fosse.index),
                         [0, 1, 2, 3, 4, 5, 6, 7])
        today = datetime.date.today()
        delta = datetime.timedelta(days=366)
        expired_date = today - delta
        expired_date = pd.to_datetime(expired_date).normalize()
        data.loc[1, 'date'] = expired_date
        fosse = parse.profondeur(data)
        self.assertEqual(list(fosse.index),
                         [0, 2, 3, 4, 5, 6, 7])

    def test_riffa(self):
        data = parse.parse_data(self.path)
        rifaa = parse.rifaa(data)
        self.assertListEqual(
            list(rifaa.index),
            [1, 4, 7, 8, 9])

    def test_no_riffa(self):
        data = parse.parse_data(self.path)
        no_rifaa = parse.no_rifaa(data)
        self.assertListEqual(
            list(no_rifaa.index),
            [0, 2, 3, 5, 6])

    def test_ligne(self):
        data = parse.parse_data(self.path)
        l1 = parse.ligne(data, 1)
        self.assertListEqual(
            list(l1.index),
            [0, 1, 2, 5])

        with self.assertRaises(ValueError) as ctx:
            parse.ligne(data, 0)
        self.assertEqual(str(ctx.exception),
                         "bad value for ligne. ligne should be 0 < int ligne < 3 got : 0")

    def test_certif_valid_at(self):
        data = parse.parse_data(self.path)
        today = self.generate_date('today', len(data))
        data.date = today
        valid = parse.certif_valid_at(data)
        self.assertEqual(list(valid.index),
                         [0, 1, 2, 3, 4, 5, 6, 7, 8])
        today = datetime.date.today()
        delta = datetime.timedelta(days=50)
        valid_date = today + delta
        valid_date = pd.to_datetime(valid_date).normalize()
        data.loc[1, 'date'] = valid_date
        target = today + datetime.timedelta(days=366)
        valid = parse.certif_valid_at(data, target_date=str(target))
        self.assertEqual(list(valid.index),
                         [1])

    def test_certif_not_valid_at(self):
        data = parse.parse_data(self.path)
        today = self.generate_date('today', len(data))
        data.date = today
        not_valid = parse.certif_not_valid_at(data)
        self.assertEqual(list(not_valid.index),
                         [])
        today = datetime.date.today()
        delta = datetime.timedelta(days=50)
        valid_date = today + delta
        valid_date = pd.to_datetime(valid_date).normalize()
        data.loc[1, 'date'] = valid_date
        target = today + datetime.timedelta(days=366)
        not_valid = parse.certif_not_valid_at(data, target_date=str(target))
        self.assertEqual(list(not_valid.index),
                         [0, 2, 3, 4, 5, 6, 7, 8])

    def test_warning(self):
        data = parse.parse_data(self.path)
        new_date = self.generate_date('today', len(data))
        delta = datetime.timedelta(days=360)
        warning_date = datetime.date.today() - delta
        warning_date = pd.to_datetime(warning_date).normalize()
        new_date[1] = warning_date
        data.date = new_date
        warning = parse.warning(data)
        self.assertEqual(list(warning.index), [1])
