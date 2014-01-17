"""
Main views
"""
import json
from app.sc2.models.game import GameModel
from app.sc2.utils import jsonDateTimeHandler
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

        data['games'] = json.dumps([game.to_dict(exclude=['replay']) for game in GameModel.get_list()],
                                   default=jsonDateTimeHandler)

        self.render_response('sc2/home.html', **data)