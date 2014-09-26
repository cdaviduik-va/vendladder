"""
Handlers for sc2 games.
"""
import json
import logging
from app.sc2.domain.match import lookup_open_matches
from app.sc2.models.game import ReplayModel, GameModel
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
        data = {
            'current_matches': lookup_open_matches(),
            'match_id': self.request.GET.get('match_id')
        }
        self.render_response('/sc2/game/submit.html', **data)

    def post(self):
        """
        Handles the submission of the match form
        """
        data = {}

        match_id = self.request.POST.get('match_id')
        # Grab the File (FieldStorage type)
        uploaded_file = self.request.POST.get('replay')

        # Process the file
        try:
            game = ReplayReader.ExtractGameInformation(uploaded_file.file, match_id)
        except ValueError, e:
            logging.exception('Failed to upload replay.')
            return self.abort(400, e.message)

        data['game'] = json.dumps(game.to_dict(exclude=['replay']), default=jsonDateTimeHandler, indent=2)

        data['winning_team'] = [player.battle_net_name for player in game.players if player.won]
        data['losing_team'] = [player.battle_net_name for player in game.players if not player.won]

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
        match_id = self.request.GET.get('matchId')
        season_id = self.request.GET.get('seasonId')
        game = GameModel.build_key(game_id, match_id, season_id).get()
        if not game:
            raise ValueError('Game with id "%s" match id "%s" and season id "%s" not found.' % game_id, match_id, season_id)

        filename = game.game_time.date().isoformat() + ' ' + ' '.join([player.battle_net_name for player in game.players]) + '.replay'
        replay = ReplayModel.get_by_game_id(game_id)
        self.response.headers['Content-Type'] = 'application/binary'
        self.response.headers['Content-Disposition'] = 'attachment; filename="%s"' % str(filename)
        self.response.out.write(replay.replay_file)