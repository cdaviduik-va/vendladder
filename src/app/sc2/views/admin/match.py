"""
-
"""
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

        self.render_response('/sc2/admin/matches/schedule.html', **data)