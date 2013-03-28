import dateutil.parser as dateparser


def unix_time(dt):
    return dateparser.parse(dt).strftime('%s')