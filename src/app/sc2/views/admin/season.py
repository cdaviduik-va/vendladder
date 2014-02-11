"""
__init__.py Documentation
"""

from app.sc2.views import UserView
from app.sc2.domain.season import create_season, lookup_seasons, close_current_season


class ListSeasonsView(UserView):

    def get(self):
        data = {
            'seasons': lookup_seasons()
        }
        self.render_response('/sc2/admin/season/index.html', **data)


class SeasonCreateView(UserView):
    """
    Allows for the scheduling of matches
    """
    def get(self):
        """
        Handles the display of the match creation form
        """
        data = {}

        if self.request.GET.get('success'):
            data['alerts'] = [('success', 'Season created successfully!')]

        self.render_response('/sc2/admin/season/create.html', **data)

    def post(self):
        """
        Potentially creates seasons
        """
        season_name = self.request.POST.get("seasonname")
        start_date = self.request.POST.get("startdate")
        try:
            create_season(season_name, start_date)
            return self.redirect_to('sc2-admin-season-create', success=True)
        except ValueError as e:
            data = {
                'alerts': [('error', e.message)]
            }
        self.render_response('/sc2/admin/season/create.html', **data)


class SeasonCloseView(UserView):

    def post(self):
        close_current_season()
        self.redirect_to('sc2-admin-season')
