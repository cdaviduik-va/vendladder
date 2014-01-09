"""
Main views
"""
from app.sc2.views import UserView

class MainView(UserView):
    """
    Home view for the Starcraft ladder
    """
    def get(self):
        """
        See above
        """
        data = {}

        self.render_response('sc2/home.html', **data)