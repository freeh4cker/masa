from time import strftime, localtime
import pkg_resources

import pandas as pd

__version__ = '{}'.format(strftime("%Y%m%d", localtime()))
DATA = pkg_resources.resource_filename('masa', "data")


def to_emails(data):
    """
    :param data:
    :return: the list of emails of freedivers in data
    :rtype: list of string
    """
    emails = data.email.to_list()
    return emails


def autonomie_absolue_piscine(data, date='today'):
    data = certif_valid_at(data, target_date=date)
    sel = data.loc[
        ((data.indoor.isin(('AP', 'ACP'))) & (data.rifaa)) | data.outdoor.isin(('ACEL', 'AEEL'))]
    return sel


def autonomie_relative_piscine(data, date='today'):
    data = certif_valid_at(data, target_date=date)
    sel = data.loc[data.indoor.isin(('AP', 'ACP')) | data.outdoor.isin(('ACEL', 'AEEL'))]
    return sel


def fosse(data, date='today'):
    data = certif_valid_at(data, target_date=date)
    sel = data.loc[(data.indoor.isin(('AP', 'ACP'))) | data.outdoor.isin(('AEL', 'ACEL', 'AEEL'))]
    return sel


def rifaa(data):
    """

    :param data:
    :return: The data for freediver who have a RIFAA
    """
    sel = data.loc[data.rifaa]
    return sel


def no_rifaa(data):
    """

    :param data:
    :return: The data for freediver who have NOT RIFAA
    """
    sel = data.loc[-data.rifaa]
    return sel


def all(data):
    """
    return the
    :param data:
    :return:
    """
    return to_emails(data)


# def _certif_valid(data, delta):
#     """
#
#     :param data:
#     :param int delta:
#     :return:
#     """
#     data = data.loc[(data.CACI) | (data.QS)]
#     today = pd.to_datetime('today').normalize()
#     data = data.loc[today - data.date < pd.Timedelta(f"{delta} days")]
#     return data


def certif_valid_at(data, target_date='today'):
    """
    :param data: the data related to the caci
    :type data: pandas.DataFrame
    :param str target_date: the date at which the caci should be valid
    :return: the data for which the caci is valid
    :rtype: pandas.DataFrame
    """
    data = data.loc[(data.CACI) | (data.QS)]
    target_date = pd.to_datetime(target_date).normalize()
    data = data.loc[target_date - data.date < 365]
    return data


def warning(data):
    date= "today + 2 weeks"
    return certif_valid_at(data, target_data=date)