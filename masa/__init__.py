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
import datetime
import pkg_resources

import pandas as pd

__version__ = '{}'.format(strftime("%Y%m%d", localtime()))
__DATA__ = pkg_resources.resource_filename('masa', "data")


def parse_data(path):
    """

    :param str path: the path nto the data to parse
    :return: the masa data
    :rtype: :class:`pandas.DataFrame` object
    """
    data = pd.read_csv(path,
                       sep='\t',
                       comment='#',
                       parse_dates=['date'],
                       infer_datetime_format=True)
    return data


def to_emails(data, verbose=False):
    """
    :param data: the filter_apnee data to extract emails
    :type data: :class:`pandas.DataFrame` object
    :param bool verbose: If True return long version of email "Prenom Nom" <email>,
                         otherwise return only email address.
    :return: the list of emails of freedivers in data
    :rtype: list of string
    """
    if verbose:
        emails = [f'"{prenom} {nom}" <{email}>' for prenom, nom, email in
                  zip(data.prenom.to_list(), data.nom.to_list(), data.email.to_list())]
    else:
        emails = data.email.to_list()
    return emails


def to_string(data):
    """

    :param data: the data to format in string
    :type data: :class:`pandas.DataFrame` object
    :return: the data each row is formatted in str
    :rtype: :class:`pandas.Series`
    """
    def format(row):
        name = f"{row.prenom} {row.nom}"
        level = f"{row.indoor}/{row.outdoor}"
        if row.CACI:
            caci = 'CACI'
        elif row.QS:
            caci = 'QS'
        else:
            caci = 'NO certif'

        rifaa = 'RIFAA' if row.rifaa else 'NO RIFAA'
        return f"{name: <25}{level: <11}{rifaa: <10}{caci: <10}{row.date.strftime('%Y-%m-%d')}  L{row.ligne} {row.email}"

    return data.apply(format, axis=1)


def autonomie_absolue_piscine(data, target_date='today'):
    """
    
    :param data: the filter_apnee data to extract emails
    :type data: :class:`pandas.DataFrame` object
    :param str target_date: the target date at which we want to select the divers
    :return:
    :rtype: :class:`pandas.DataFrame` object
    """
    data = certif_valid_at(data, target_date=target_date)
    sel = data.loc[
        ((data.indoor.isin(('AP', 'ACP'))) & (data.rifaa)) | data.outdoor.isin(('ACEL', 'AEEL'))]
    return sel


def autonomie_relative_piscine(data, target_date='today'):
    """
    
    :param data: the filter_apnee data to extract emails
    :type data: :class:`pandas.DataFrame` object 
    :param str target_date: the target date at which we want to select the divers
    :return:
    :rtype: :class:`pandas.DataFrame` object
    """
    data = certif_valid_at(data, target_date=target_date)
    sel = data.loc[data.indoor.isin(('AP', 'ACP')) | data.outdoor.isin(('ACEL', 'AEEL'))]
    return sel


def fosse(data, target_date='today'):
    """
    
    :param data: the filter_apnee data to extract emails
    :type data: :class:`pandas.DataFrame` object
    :param str target_date: the target date at which we want to select the divers
    :return: the data of freediver who are allowed to go in fosse
    :rtype: :class:`pandas.DataFrame` object
    """
    data = certif_valid_at(data, target_date=target_date)
    sel = data.loc[(data.CACI) &
                   ((data.indoor.isin(('AP', 'ACP'))) | data.outdoor.isin(('AEL', 'ACEL', 'AEEL')))]
    return sel


def profondeur(data, target_date='today'):
    """

    :param data: the filter_apnee data to extract emails
    :type data: :class:`pandas.DataFrame` object
    :param str target_date: the target date at which we want to select the divers
    :return: the data of freediver who are allowed to practice in deep freedive
    :rtype: :class:`pandas.DataFrame` object
    """
    data = certif_valid_at(data, target_date=target_date)
    sel = data.loc[data.CACI]
    return sel


def rifaa(data):
    """

    :param data: the data related to the CACI
    :type data: :class:`pandas.DataFrame` object
    :return: The data for freediver who have a RIFAA
    :rtype: :class:`pandas.DataFrame` object
    """
    sel = data.loc[data.rifaa]
    return sel


def no_rifaa(data):
    """

    :param data: the data related to the CACI
    :type data: :class:`pandas.DataFrame` object
    :return: The data for freediver who have NOT RIFAA
    :rtype: :class:`pandas.DataFrame` object
    """
    sel = data.loc[-data.rifaa]
    return sel


def ligne(data, ligne):
    """

    :param data: the data related to the CACI
    :type data: :class:`pandas.DataFrame` object
    :return: The data for freedivers who dive in ligne *ligne*
    :rtype: :class:`pandas.DataFrame` object
    """
    if 0 < ligne < 3:
        sel = data.loc[data.ligne == ligne]
        return sel
    else:
        raise ValueError(f"bad value for ligne. ligne should be 0 < int ligne < 3 got : {ligne}")


def certif_valid_at(data, target_date='today'):
    """
    :param data: the data related to the CACI
    :type data: :class:`pandas.DataFrame` object
    :param str target_date: the date at which the CACI should be valid
    :return: the data for which the CACI or QS is valid
    :rtype: :class:`pandas.DataFrame` object
    """
    data = data.loc[(data.CACI) | (data.QS)]
    target_date = pd.to_datetime(target_date).normalize()
    # pandas timedelta does not support unit greater than days
    data = data.loc[target_date - data.date < pd.Timedelta('365 days')]
    return data


def certif_not_valid_at(data, target_date='today'):
    """

    :param data: the data related to the CACI
    :type data: :class:`pandas.DataFrame` object
    :param str target_date: the date at which the CACI should be valid
    :return:
    :rtype: :class:`pandas.DataFrame` object
    """
    data = data.loc[(data.CACI) | (data.QS)]
    target_date = pd.to_datetime(target_date).normalize()
    data = data.loc[target_date - data.date > pd.Timedelta('365 days')]
    return data


def warning(data, time_delta=15):
    """

    :param data: the data related to the CACI
    :type data: :class:`pandas.DataFrame` object
    :param int time_delta: the time delta to add to today to test CACI validity
    :return: the freedivers who have a valid CACI or QS today but which
             expire before *time_delta* days
    :rtype: :class:`pandas.DataFrame` object
    """
    today = datetime.date.today()
    delay = datetime.timedelta(days=time_delta)
    target_date = today + delay
    valid_today = certif_valid_at(data)
    expire_at_time_delta = certif_not_valid_at(data, target_date=target_date)
    to_warn = valid_today.loc[expire_at_time_delta.index]
    return to_warn


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