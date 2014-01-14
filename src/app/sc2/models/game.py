"""
game.py Documentation
"""
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
    replay = ndb.BlobProperty()

    @classmethod
    def _get_kind(cls):
        return "SCII_GameModel"