"""
SC2 Game models.
"""
import hashlib
from google.appengine.ext import ndb
from app.sc2.models import BaseModel
from app.sc2.models.match import MatchModel


class PlayerStatsModel(BaseModel):
    """
    Models a player's performance within a game
    """
    battle_net_name = ndb.StringProperty()
    race = ndb.StringProperty()
    was_random = ndb.BooleanProperty()
    handicap = ndb.IntegerProperty()
    won = ndb.BooleanProperty()
    season_id = ndb.StringProperty(required=True)

    @classmethod
    def _get_kind(cls):
        return "SCII_PlayerStatsModel"


class GameModel(BaseModel):
    """
    Models a single game within a match
    """
    game_id = ndb.ComputedProperty(lambda self: self.key.id())
    match_id = ndb.ComputedProperty(lambda self: self.key.parent().id())
    season_id = ndb.ComputedProperty(lambda self: self.key.parent().parent().id())
    map_name = ndb.StringProperty()
    game_time = ndb.DateTimeProperty()
    game_length_seconds = ndb.IntegerProperty()
    speed = ndb.StringProperty()
    # sc2 version
    release = ndb.StringProperty()
    players = ndb.StructuredProperty(PlayerStatsModel, repeated=True)
    # 1v1, 2v2, etc.
    type = ndb.StringProperty()

    @classmethod
    def _get_kind(cls):
        return "SCII_GameModel"

    @classmethod
    def generate_key(cls, game_time, player_names, match_id, season_id):
        """ Generate a unique key based on the time the game was played. """
        if not game_time:
            raise ValueError('game_time is required.')
        if not player_names:
            raise ValueError('player_names are required.')
        if not match_id:
            raise ValueError('match_id is required.')

        player_names = sorted(player_names)
        string_to_hash = str(game_time) + ''.join(player_names)
        key_name = hashlib.md5(string_to_hash).hexdigest()
        parent = MatchModel.build_key(match_id, season_id)
        return ndb.Key(cls._get_kind(), key_name, parent=parent)

    @classmethod
    def build_key(cls, game_id, match_id, season_id):
        """ Build a key from a previously generated game id key name. """
        parent = MatchModel.build_key(match_id, season_id)
        return ndb.Key(cls._get_kind(), game_id, parent=parent)

    @classmethod
    def lookup_for_match(cls, match_id):
        return cls.query(cls.match_id == match_id).fetch()

    @classmethod
    def lookup_all(cls, limit=None):
        query = cls.query().order(-cls.game_time)
        return query.fetch(limit=limit)

    @classmethod
    def lookup_for_player(cls, battle_net_name, limit=None):
        return cls.query(cls.players.battle_net_name == battle_net_name).order(-cls.game_time).fetch(limit=limit)


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
