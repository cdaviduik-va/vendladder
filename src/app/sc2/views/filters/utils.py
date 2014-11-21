""" Utility filters for jinja. """

import re
import urlparse
from jinja2 import evalcontextfilter, Markup

@evalcontextfilter
def do_bookend(eval_ctx, content, prefix='', suffix=''):
    """ If the content is not None and not '' the prefix and suffix will be applied to the content.

    Useful for applying small tags conditionally on the value. E.g., instead of:

      {{ if myvalue }}{% myvalue %}<br/>{% endif %}

    you can do this:

      {{ myvalue|bookend(suffix='<br/>') }}

    """
    if not content:
        return ''
    result = '%s%s%s' % (prefix, content, suffix)
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

def do_re_sub(content, pattern, repl):
    """ Does an re.sub(pattern, repl, content) in the Python sense.

    @see http://docs.python.org/library/re.html#re.sub
    """
    return re.sub(pattern, repl, content)

def do_substring(content, split):
    """ Does a substring.

    @param content the string to substring
    @param split the split notation, a la Python, e.g., "0:1" or "2:" or ":-1"
    """
    first, last = split.split(':')
    if first != '' and last != '':
        return content[int(first):int(last)]
    if first != '':
        return content[int(first):]
    if last != '':
        return content[:int(last)]

def do_dateformat(value, date_format='%b %d, %Y'):
    """ formats a datetime object with the strftime function defaulting to MMM D, YYYY eg  Apr 8, 2011 """
    return value.strftime(date_format)

def do_datetimeformat(value, datetime_format='%b %d, %Y %H:%M:%S'):
    """ formats a datetime object with the strftime function defaulting to MMM D, YYYY HH:MM:SS eg  Apr 8, 2011 """
    return value and value.strftime(datetime_format)

def do_spliturlhost(url):
    """ Splits a url and returns the just the host """
    return urlparse.urlsplit(url)[1]

def do_ascii_only(unicode_str):
    """ Takes a unicode string and returns back only ascii characters """
    return unicode_str.encode("ascii", "ignore")
