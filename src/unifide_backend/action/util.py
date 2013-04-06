import dateutil.parser as dateparser


def unix_time(dt):
    return dateparser.parse(dt).strftime('%s')

def key_check(dict, key):
    return dict[key] if key in dict else None