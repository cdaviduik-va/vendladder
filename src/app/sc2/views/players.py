"""
players.py Documentation
"""
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

        self.render_response('sc2/players/index.html', **data)