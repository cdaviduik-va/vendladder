import json
from app.sc2.domain.match import lookup_games, lookup_open_matches, close_match
from app.sc2.utils import jsonDateTimeHandler
from app.sc2.views import UserView


class MatchHistoryView(UserView):
    """
    List previous match details
    """
    def get(self):
        """
        See above
        """
        data = {
            'current_matches': lookup_open_matches(),
            'games': json.dumps([game.to_dict() for game in lookup_games(limit=10)], default=jsonDateTimeHandler)
        }
        self.render_response('sc2/match/history.html', **data)


class CloseMatchView(UserView):

    def post(self, match_id):
        close_match(match_id)
