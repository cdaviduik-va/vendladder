"""
round.py Documentation
"""
from app.sc2.views import UserView


class RoundCreateView(UserView):
    """
    Allows for the scheduling of matches
    """
    def get(self):
        """
        Handles the display of the match creation form
        """
        data = {}

        self.render_response('/sc2/admin/round/create.html', **data)

    def post(self):
        """
        Potentially creates seasons
        """
        season_name = self.request.POST.get("seasonname")
        start_date = self.request.POST.get("startdate")

        data = {
            "season_created": True if new_season else False,
            "season_name": season_name
        }

        self.render_response('/sc2/admin/season/create.html', **data)