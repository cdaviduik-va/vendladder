import os

import set_sys_path # Must be done first to set up path

from webapp2 import WSGIApplication, uri_for
from app.sc2.views.filters.vurl import do_vurl
from app.sc2.views.filters.utils import do_bookend, do_re_sub, do_substring, do_dateformat, do_datetimeformat, \
    do_spliturlhost, do_ascii_only
from urls import ROUTES

TEMPLATE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'templates')

CONFIG = {
    'webapp2_extras.jinja2': {
        'filters' : {
            'vurl' : do_vurl,
            'bookend': do_bookend,
            're_sub': do_re_sub,
            'substring': do_substring,
            'dateformat': do_dateformat,
            'datetimeformat': do_datetimeformat,
            'splithost': do_spliturlhost,
            'ascii_only': do_ascii_only,
        },
        'globals': {
            'uri_for': uri_for
        },
        'template_path': TEMPLATE_DIR
    }
}


app = WSGIApplication(ROUTES, config=CONFIG)
