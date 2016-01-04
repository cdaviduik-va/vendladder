import json
import logging
from google.appengine.api import users
from webapp2 import RequestHandler, cached_property
from webob.multidict import MultiDict

from app.sc2.domain.match import lookup_games, lookup_matches, close_match, lookup_open_matches
from app.sc2.utils import jsonDateTimeHandler
from app.sc2.utils.replay_reader import ReplayReader


class BaseAjaxView(RequestHandler):

    @cached_property
    def request_data(self):
        if self.request.method == 'POST':
            return MultiDict(json.loads(self.request.body))
        else:
            return self.request.GET

    def serialize_data(self, data):
        if isinstance(data, dict):
            return data
        if isinstance(data, list):
            return [d.to_dict() for d in data if d]

        return data and data.to_dict()

    def render_response(self, data, status=200):
        serialized_data = self.serialize_data(data)
        self.render_serialized_response(serialized_data, status=status)

    def render_serialized_response(self, serialized_data, status=200):
        self.response.content_type = 'application/json'
        self.response.status = status
        self.response.write(json.dumps(serialized_data, default=jsonDateTimeHandler))


class BaseAuthAjaxView(BaseAjaxView):
    # TODO: check for auth in dispatch method
    pass


class LookupMatchesView(BaseAuthAjaxView):

    def get(self):
        limit = self.request_data.get('limit', 10)
        self.render_response(lookup_matches(limit=limit))


class LookupOpenMatchesView(BaseAuthAjaxView):

    def get(self):
        self.render_response(lookup_open_matches())


class CloseMatchView(BaseAuthAjaxView):

    def post(self):
        match_id = self.request_data['matchId']
        close_match(match_id)


class SubmitGameView(BaseAuthAjaxView):

    def post(self):
        logging.info('SUBMIT GAME VIEW')
        logging.info(self.request.POST)

        match_id = self.request.POST.get('matchId')
        replay = self.request.POST['file']

        try:
            game = ReplayReader.ExtractGameInformation(replay.file, match_id)
        except ValueError, e:
            logging.exception('Failed to upload replay.')
            return self.render_response({'message': e.message}, status=400)

        data = {
            'game': game.to_dict(exclude=['replay']),
            'winning_team': [player.battle_net_name for player in game.players if player.won],
            'losing_team': [player.battle_net_name for player in game.players if not player.won]
        }
        self.render_response(data)


class GetUserAuthLinksView(BaseAjaxView):

    def get(self):
        dest_url = '/sc2/ng/'
        return self.render_response({
            'login': users.create_login_url(dest_url),
            'logout': users.create_logout_url(dest_url)
        })


class GetUserView(BaseAjaxView):

    def get(self):
        return self.render_response(users.get_current_user())

    def serialize_data(self, data):
        if not data:
            return None
        return {
            'email': data.email(),
            'user_id': data.user_id(),
            'nickname': data.nickname(),
            'is_admin': users.is_current_user_admin()
        }
