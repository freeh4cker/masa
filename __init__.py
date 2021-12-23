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
    data = data.loc[(data.CACI) | (data.QS)]
    today = pd.to_datetime('today').normalize()
    data = data.loc[today - data.date < pd.Timedelta(f"{delta} days")]
    return data

def valid(data, date=today):
    return _certif_valid(data, 365)

def warning(data):
    return _certif_valid(data, 350)