"""
-
"""
import json
from app.sc2.domain.match import get_suggested_matches
from app.sc2.models.player import PlayerModel
from app.sc2.utils import jsonDateTimeHandler
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
        data['is_debug'] = self.request.GET.get('is_debug')
        data['players'] = json.dumps([player.to_dict() for player in players], default=jsonDateTimeHandler)
        data['remaining_rounds'] = json.dumps([round.to_dict() for round in rounds])
        data['current_season'] = json.dumps([])

        data['suggested_matches'] = get_suggested_matches()

        #Render the page
        self.render_response('/sc2/admin/matches/create.html', **data)