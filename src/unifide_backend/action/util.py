import bz2
import dateutil.parser as dateparser
from datetime import datetime
from HTMLParser import HTMLParser


def unix_time(dt):
    return dateparser.parse(dt).strftime('%s')


def key_check(dict, key):
    return dict[key] if key in dict else None


def unreadable(s):
    """
    Encodes a string (usually a password) into a non-human readable form
    IE: So as not to represent passwords in its raw form
    """
    return bz2.compress(s)


def readable(s):
    """
    Decodes a string from its encoded form from unreadable()
    """
    return bz2.decompress(s)


def generator_to_list(gen):
    """
    WARNING: USE THIS ONLY IF YOU KNOW THAT THE GENERATOR IS OF FINITE LENGTH
    Converts a generator into a list
    """
    lis = []
    while True:
        try:
            item = gen.next()
            lis += [item]
        except StopIteration:
            break
    return lis


def isoformat(epoch):
    return datetime.utcfromtimestamp(epoch).isoformat()


def replace_newline(str):
    return str.replace('<br>', '\n')


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(HTMLParser().unescape(html))
    return s.get_data()