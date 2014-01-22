"""
Handlers for sc2 games.
"""
import json
from app.sc2.models.game import ReplayModel
from app.sc2.utils import jsonDateTimeHandler
from app.sc2.utils.replay_reader import ReplayReader
from app.sc2.views import UserView


class GameSubmitView(UserView):
    """
    Handles the submission of views
    """
    def get(self):
        """
        Handles the display of the match submission form
        """
        data = {}

        self.render_response('/sc2/game/submit.html', **data)

    def post(self):
        """
        Handles the submission of the match form
        """
        data = {}

        # Grab the File (FieldStorage type)
        uploaded_file = self.request.POST.get('replay')

        # Process the file
        game = ReplayReader.ExtractGameInformation(uploaded_file.file)

        data['game'] = json.dumps(game.to_dict(exclude=['replay']), default=jsonDateTimeHandler, indent=2)

        data['winning_team'] = [player.name for player in game.players if player.won]
        data['losing_team'] = [player.name for player in game.players if not player.won]

        self.render_response('/sc2/game/submit_complete.html', **data)

class GameDownloadView(UserView):
    """
    Handles the submission of views
    """
    def get(self):
        """
        Handles the display of the match submission form
        """
        game_id = self.request.GET.get('id')
        replay = ReplayModel.get_by_game_id(game_id)
        self.response.headers['Content-Type'] = 'application/binary'
        self.response.headers['Content-Disposition'] = 'attachement; filename="game.SC2Replay"'
        self.response.out.write(replay.replay_file)