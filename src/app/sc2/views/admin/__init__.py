"""
__init__.py Documentation
"""

from app.sc2.views import UserView

class MainAdminView(UserView):
    """
    Allows for the scheduling of matches
    """
    def get(self):
        """
        Handles the display of the match creation form
        """
        data = {}

        self.render_response('/sc2/admin/main.html', **data)