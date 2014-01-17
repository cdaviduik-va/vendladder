"""
Player model
"""
from google.appengine.ext import ndb


class PlayerModel(ndb.Model):
    """
    Model for a StarCraft II player
    """
    player_id = ndb.ComputedProperty(lambda self: self.key.id())
    name = ndb.StringProperty()
    vendasta_email = ndb.StringProperty()
    battle_net_name = ndb.StringProperty()
    skill_level = ndb.IntegerProperty()
    season = ndb.StringProperty()

    @classmethod
    def get_players_by_season(cls, season="Winter 1", keys_only=False):
        return cls.query(cls.season == season).get(keys_only=keys_only)

    @classmethod
    def _get_kind(cls):
        return "SCII_PlayerModel"