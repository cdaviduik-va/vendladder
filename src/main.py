import os

import set_sys_path # Must be done first to set up path

from webapp2 import WSGIApplication, uri_for
from app.sc2.views.filters.vurl import do_vurl
from urls import ROUTES

TEMPLATE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'templates')

CONFIG = {
    'webapp2_extras.jinja2': {
        'filters' : {
            'vurl' : do_vurl
        },
        'globals': {
            'uri_for': uri_for
        },
        'template_path': TEMPLATE_DIR
    }
}


app = WSGIApplication(ROUTES, config=CONFIG)
