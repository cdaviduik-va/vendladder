from webapp2 import Route, SimpleRoute
from webapp2_extras.routes import RedirectRoute

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

    # Starcraft II Tracker main routes
    RedirectRoute('/sc2/', handler='app.sc2.views.main.MainView', name='sc2-home', strict_slash=True),
    RedirectRoute('/sc2/game/submit/', handler='app.sc2.views.game.GameSubmitView', name='sc2-game-submit', strict_slash=True),

    RedirectRoute('/sc2/match/', handler='app.sc2.views.match.MatchHistoryView', name='sc2-match-history', strict_slash=True),
    RedirectRoute('/sc2/match/close/<match_id>/', handler='app.sc2.views.match.CloseMatchView', name='sc2-match-close', strict_slash=True),
    RedirectRoute('/sc2/player/', handler='app.sc2.views.player.PlayerIndex', name='sc2-player', strict_slash=True),
    RedirectRoute('/sc2/player/<battle_net_name>/', handler='app.sc2.views.player.PlayerDetails', name='sc2-player-details', strict_slash=True),
    RedirectRoute('/sc2/game/download/', handler='app.sc2.views.game.GameDownloadView', name='sc2-game-download', strict_slash=True),

    # SC2 Admin routes
    RedirectRoute('/sc2/admin/season/', handler='app.sc2.views.admin.season.ListSeasonsView', name='sc2-admin-season', strict_slash=True),
    RedirectRoute('/sc2/admin/season/create/', handler='app.sc2.views.admin.season.SeasonCreateView', name='sc2-admin-season-create', strict_slash=True),
    RedirectRoute('/sc2/admin/season/close/', handler='app.sc2.views.admin.season.SeasonCloseView', name='sc2-admin-season-close', strict_slash=True),
    RedirectRoute('/sc2/admin/match/create/', handler='app.sc2.views.admin.match.MatchCreateView', name='sc2-admin-match-create', strict_slash=True),
    RedirectRoute('/sc2/admin/player/create/', handler='app.sc2.views.admin.player.PlayerCreateView', name='sc2-admin-player-create', strict_slash=True),
    RedirectRoute('/sc2/admin/player/edit/<battle_net_name>/', handler='app.sc2.views.admin.player.PlayerEditView', name='sc2-admin-player-edit', strict_slash=True),

    # SC2 Angular
    RedirectRoute('/sc2/ng/', handler='app.sc2.views.main.AngularView'),

    # SC2 Apis
    Route('/sc2/api/game/submit/', handler='app.sc2.views.api.SubmitGameView'),
    Route('/sc2/api/user/getAuthLinks/', handler='app.sc2.views.api.GetUserAuthLinksView'),
    Route('/sc2/api/user/get/', handler='app.sc2.views.api.GetUserView'),

    # SC2 match resource
    Route('/sc2/api/match', handler='app.sc2.views.api.MatchResource'),
    Route('/sc2/api/match/suggested', handler='app.sc2.views.api.MatchResource:query_suggested'),
    Route('/sc2/api/match/forPlayer/<battle_net_name>', handler='app.sc2.views.api.MatchResource:query_for_player'),
    Route('/sc2/api/match/<action>', handler='app.sc2.views.api.MatchResource'),

    # SC2 player resource
    Route('/sc2/api/player', handler='app.sc2.views.api.PlayerResource'),
    Route('/sc2/api/player/getAuthed', handler='app.sc2.views.api.PlayerResource:get_authed'),
    Route('/sc2/api/player/queryOpponentsForPlayer/<battle_net_name>', handler='app.sc2.views.api.PlayerResource:query_opponents_for_player'),
    Route('/sc2/api/player/<battle_net_name>', handler='app.sc2.views.api.PlayerResource'),

    #General
    SimpleRoute('/sc2.+', handler='app.sc2.views.main.ErrorView'),
    SimpleRoute('/.+', handler='app.views.errorHandler'),
]