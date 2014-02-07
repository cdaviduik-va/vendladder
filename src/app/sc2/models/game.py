"""
SC2 Game models.
"""
import hashlib
from google.appengine.ext import ndb
from app.sc2.models import BaseModel
from constants import Seasons


class PlayerStatsModel(BaseModel):
    """
    Models a player's performance within a game
    """
    battle_net_name = ndb.StringProperty()
    race = ndb.StringProperty()
    was_random = ndb.BooleanProperty()
    handicap = ndb.IntegerProperty()
    won = ndb.BooleanProperty()
    season = ndb.StringProperty(required=True, choices=Seasons.VALID_SEASONS)

    @classmethod
    def _get_kind(cls):
        return "SCII_PlayerStatsModel"


class GameModel(BaseModel):
    """
    Models a single game within a match
    """
    game_id = ndb.ComputedProperty(lambda self: self.key.id())
    map_name = ndb.StringProperty()
    game_time = ndb.DateTimeProperty()
    game_length_seconds = ndb.IntegerProperty()
    speed = ndb.StringProperty()
    release = ndb.StringProperty()
    players = ndb.StructuredProperty(PlayerStatsModel, repeated=True)
    type = ndb.StringProperty()
    round = ndb.KeyProperty()

    @classmethod
    def _get_kind(cls):
        return "SCII_GameModel"

    @classmethod
    def generate_key(cls, game_time, player_names):
        """ Generate a unique key based on the time the game was played. """
        if not game_time:
            raise ValueError('game_time required')
        if not player_names:
            raise ValueError('player_names required')

        player_names = sorted(player_names)
        string_to_hash = str(game_time) + ''.join(player_names)
        key_name = hashlib.md5(string_to_hash).hexdigest()
        return ndb.Key(cls._get_kind(), key_name)

    @classmethod
    def build_key(cls, game_id):
        """ Build a key from a previously generated game id key name. """
        return ndb.Key(cls._get_kind(), game_id)

    @classmethod
    def get_list(cls):
        query = cls.query().order(-cls.game_time)
        return query.fetch()


class ReplayModel(BaseModel):
    game_id = ndb.ComputedProperty(lambda self: self.key.id())
    replay_file = ndb.BlobProperty()

    @classmethod
    def _get_kind(cls):
        return "SCII_ReplayModel"

    @classmethod
    def build_key(cls, game_id):
        """ Build a key corresponding to the game this is a replay for. """
        return ndb.Key(cls._get_kind(), game_id)

    @classmethod
    def get_by_game_id(cls, game_id):
        """ Return the replay corresponding to the indicated game. """
        return cls.build_key(game_id).get()
