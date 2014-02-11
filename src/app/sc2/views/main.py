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
        return self.redirect_to('sc2-match-history')


class ErrorView(UserView):
    """
    Display an error message without going to the root homepage
    """
    def get(self):
        """
        Get function for ErrorView
        """
        path = self.request.path_qs[1:]
        self.render_response("sc2/error.html", error_message=path)