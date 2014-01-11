"""
-
"""
import json
from app.sc2.models.player import PlayerModel
from app.sc2.views import UserView

class MatchCreateView(UserView):
    """
    Allows for the scheduling of matches
    """
    def get(self):
        """
        Handles the display of the match creation form
        """
        data = {}

        #Gather all of the players
        players = PlayerModel.query().fetch()
        rounds = []
        data['players'] = json.dumps([player.to_dict() for player in players])
        data['remaining_rounds'] = json.dumps([round.to_dict() for round in rounds])
        data['current_season'] = json.dumps([])

        #Render the page
        self.render_response('/sc2/admin/matches/create.html', **data)