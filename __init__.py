import pandas as pd


def to_emails(data):
    emails = data.email.to_list()
    return emails


def autonomie_absolue_piscine(data):
    data = valid(data)
    sel = data.loc[
        ((data.indoor.isin(('AP', 'ACP'))) & (data.rifaa)) | data.outdoor.isin(('ACEL', 'AEEL'))]
    return sel


def autonomie_relative_piscine(data):
    data = valid(data)
    sel = data.loc[data.indoor.isin(('AP', 'ACP')) | data.outdoor.isin(('ACEL', 'AEEL'))]
    return sel


def fosse(data):
    data = valid(data)
    sel = data.loc[(data.indoor.isin(('AP', 'ACP'))) | data.outdoor.isin(('AEL', 'ACEL', 'AEEL'))]
    return sel


def rifaa(data):
    sel = data.loc[data.rifaa]
    return sel


def no_rifaa(data):
    sel = data.loc[-data.rifaa]
    return sel


def all(data):
    return to_emails(data)


def _certif_valid(data, delta):
    """

    :param data:
    :param int delta:
    :return:
    """
    data = data.loc[(data.CACI) | (data.QS)]
    today = pd.to_datetime('today').normalize()
    data = data.loc[today - data.date < pd.Timedelta(f"{delta} days")]
    return data


def _certif_valid_at(data, target_date='today'):
    """

    :param data:
    :param int delta:
    :return:
    """
    data = data.loc[(data.CACI) | (data.QS)]
    target_date = pd.to_datetime(target_date).normalize()
    data = data.loc[target_date - data.date < 365]
    return data


def valid(data, date='today'):
    return _certif_valid_at(data)


def warning(data):
    date= today + 2 weeks
    return _certif_valid_at(data, target_data=date)