import os

import set_sys_path # Must be done first to set up path

from webapp2 import WSGIApplication, Route, SimpleRoute
from app.sc2.views.filters.vurl import do_vurl

ROUTES = [
    #Foosball Ladder
    Route('/',              handler='app.views.mainView'),
    Route('/player',        handler='app.views.playerView'),
    Route('/newPlayer',     handler='app.views.newPlayerView'),
    Route('/selector',      handler='app.views.selectorView'),
    Route('/ladder',        handler='app.views.ladder.ladderView'),
    Route('/recordGame',    handler='app.views.reportView'),
    Route('/reportGame',    handler='app.views.reportView'),
    Route('/settings',      handler='app.views.settingsView'),
    Route('/compare',       handler='app.views.compareView'),
    Route('/playerView',    handler='app.views.playerStatsView'),
    Route('/about',         handler='app.views.aboutView'),
    Route('/leaderboard',   handler='app.views.leaderboardView'),
    Route('/matchHistory',  handler='app.views.matchHistoryView'),
    Route('/matchHistoryCalc', handler='app.views.matchHistoryCalc'),
    Route('/ladder-redirect', handler='app.views.ladderRedirect'),

    #Starcraft II Tracker
    SimpleRoute('/sc2/?', handler='app.sc2.views.main.MainView'),
    SimpleRoute('/sc2/game/submit/?', handler='app.sc2.views.game.GameSubmitView'),

    SimpleRoute('/sc2/admin/match/create/?', handler='app.sc2.views.admin.match.MatchCreateView'),

    #General
    SimpleRoute('/.+',      handler='app.views.errorHandler'),
]

TEMPLATE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'templates')

CONFIG = {
    'webapp2_extras.jinja2': {
        'filters' : {
            'vurl' : do_vurl
        },
        'template_path': TEMPLATE_DIR
    }
}


app = WSGIApplication(ROUTES, config=CONFIG)
