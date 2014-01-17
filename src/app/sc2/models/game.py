"""
SC2 Game models.
"""
import hashlib
from google.appengine.ext import ndb


class PlayerPerformanceModel(ndb.Model):
    """
    Models a player's performance within a game
    """
    name = ndb.StringProperty()
    race = ndb.StringProperty()
    was_random = ndb.BooleanProperty()
    handicap = ndb.IntegerProperty()
    won = ndb.BooleanProperty()

    @classmethod
    def _get_kind(cls):
        return "SCII_PlayerPerformanceModel"

class GameModel(ndb.Model):
    """
    Models a single game within a match
    """
    map_name = ndb.StringProperty()
    game_time = ndb.DateTimeProperty()
    game_length_seconds = ndb.IntegerProperty()
    speed = ndb.StringProperty()
    release = ndb.StringProperty()
    players = ndb.StructuredProperty(PlayerPerformanceModel, repeated=True)
    type = ndb.StringProperty()
    round = ndb.KeyProperty()
    game_id = ndb.ComputedProperty(lambda self: self.key.id())

    @classmethod
    def _get_kind(cls):
        return "SCII_GameModel"

    @classmethod
    def generate_key(cls, game_time):
        """ Generate a unique key based on the time the game was played. """
        hashed_game_time = hashlib.md5(str(game_time)).hexdigest()
        key_name = 'GM-' + hashed_game_time
        return ndb.Key(cls._get_kind(), key_name)

    @classmethod
    def build_key(cls, game_id):
        """ Build a key from a previously generated game id key name. """
        return ndb.Key(cls._get_kind(), game_id)

    @classmethod
    def get_list(cls):
        query = cls.query().order(-cls.game_time)
        return query.fetch()

class ReplayModel(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    replay_id = ndb.ComputedProperty(lambda self: self.key.id())
    game_id = ndb.ComputedProperty(lambda self: self.key.parent().id())
    replay_file = ndb.BlobProperty()

    @classmethod
    def _get_kind(cls):
        return "SCII_ReplayModel"

    @classmethod
    def build_key(cls, game_id):
        """ Build a key corresponding to the game this is a replay for. """
        game_hash = game_id.partition('-')[2]
        parent_key = GameModel.build_key(game_id)
        key_name = 'RP-' + game_hash
        return ndb.Key(cls._get_kind(), key_name, parent=parent_key)

    @classmethod
    def get_by_game_id(cls, game_id):
        """ Return the replay corresponding to the indicated game. """
        return cls.build_key(game_id).get()
