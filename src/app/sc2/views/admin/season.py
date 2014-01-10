"""
__init__.py Documentation
"""

from app.sc2.views import UserView
from app.sc2.domain.season import create_season

class SeasonCreateView(UserView):
    """
    Allows for the scheduling of matches
    """
    def get(self):
        """
        Handles the display of the match creation form
        """
        data = {}

        self.render_response('/sc2/admin/season/create.html', **data)

    def post(self):
        """
        Potentially creates seasons
        """
        season_name = self.request.POST.get("seasonname")
        start_date = self.request.POST.get("startdate")
        new_season = create_season(season_name, start_date)
