"""
players.py Documentation
"""
import json
from app.sc2.models.player import PlayerModel
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
        data = {}

        #Grab the list of players
        players = PlayerModel.query().fetch()
        data['playersJson'] = json.dumps(players, default=jsonDateTimeHandler)

        self.render_response('sc2/players/index.html', **data)