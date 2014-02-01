"""
players.py Documentation
"""
import json
from app.sc2.domain.player import get_player_details_for_season
from app.sc2.utils import jsonDateTimeHandler
from app.sc2.views import UserView


class PlayerIndex(UserView):
    """
    Lists the current players in the tournament
    """
    def get(self):
        """
        See above
        """
        players = get_player_details_for_season()
        data = {
            'playersJson': json.dumps(players, default=jsonDateTimeHandler)
        }
        self.render_response('sc2/players/index.html', **data)
