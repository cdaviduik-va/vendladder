"""
-
"""
from app.sc2.views import UserView


class MatchSubmitView(UserView):
    """
    Handles the submission of views
    """
    def get(self):
        """
        Handles the display of the match submission form
        """
        data = {}

        self.render_response('/sc2/matches/submit.html', **data)

    def post(self):
        """
        Handles the submission of the match form
        """
        data = {}

        self.render_response('/sc2/matches/submit_complete.html', **data)