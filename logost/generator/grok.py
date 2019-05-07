GROK_PATTERN = dict()


def register_grok(name, regex):
    global GROK_PATTERN
    GROK_PATTERN[name] = regex


WORD = '[a-zA-Z0-9-]+'
register_grok('WORD', WORD)
USERNAME = '[a-zA-Z0-9._-]+'
register_grok('USERNAME', USERNAME)
USER = '%{USERNAME}'
register_grok('USER', USER)
INT = '[+-]?[0-9]+'
register_grok('INT', INT)

IP4 = '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
register_grok('IP4', IP4)

# Date/Time
# From 1900 to 2099
YEAR = '(19|20)\d\d'
register_grok('YEAR', YEAR)
MONTH = '(0[1-9]|1[0-2])'
register_grok('MONTH', MONTH)
MONTH_SHORT = '(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
register_grok('MONTH_SHORT', MONTH_SHORT)
DAY = '(0[1-9]|[12][0-9]|3[01])'
register_grok('DAY', DAY)
HOUR = '(0[1-9]|[1][0-9]|2[03])'
register_grok('HOUR', HOUR)
MINUTE = '[0-5]\d'
register_grok('MINUTE', MINUTE)
SECOND = '[0-5]\d'
register_grok('SECOND', SECOND)
ISO8601_TIMEZONE = '[+-]%{HOUR}00'
register_grok('ISO8601_TIMEZONE', ISO8601_TIMEZONE)

# HTTP
HTTP_PROTO = 'HTTP/1\.(0|1)'
register_grok('HTTP_PROTO', HTTP_PROTO)
HTTP_VERB = '(GET|POST|HEAD|OPTIONS|PUT|DELETE)'
register_grok('HTTP_VERB', HTTP_VERB)
HTTP_VERB_GETPOST = '(GET|POST)'
register_grok('HTTP_VERB_GETPOST', HTTP_VERB_GETPOST)

APACHE_START = '\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b - - \[(0[1-9]|[12][0-9]|3[01])/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/(19|20)\d\d:(0[1-9]|[1][0-9]|2[03]):[0-5]\d:[0-5]\d \+0[0-9]00\]'
