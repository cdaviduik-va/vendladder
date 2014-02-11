"""
match.py Documentation
"""
from google.appengine.ext import ndb
import hashlib
from app.sc2.models import BaseModel
from app.sc2.models.season import SeasonModel


class MatchModel(BaseModel):
    """
    Models a match
    """
    match_id = ndb.ComputedProperty(lambda self: self.key.id())
    season_id = ndb.ComputedProperty(lambda self: self.key.parent().id())
    team1_battle_net_names = ndb.StringProperty(repeated=True)
    team2_battle_net_names = ndb.StringProperty(repeated=True)
    team1_wins = ndb.IntegerProperty()
    team2_wins = ndb.IntegerProperty()
    games_played = ndb.IntegerProperty()
    is_open = ndb.BooleanProperty(default=True)

    @classmethod
    def build_key(cls, match_id, season_id):
        if not match_id:
            raise ValueError('match_id is required.')
        parent = SeasonModel.build_key(season_id)
        return ndb.Key(cls._get_kind(), match_id, parent=parent)

    @classmethod
    def generate_key(cls, battle_net_names, season_id):
        if not battle_net_names:
            raise ValueError('battle_net_names are required.')
        battle_net_names = sorted(battle_net_names)
        key_name = hashlib.md5(''.join(battle_net_names)).hexdigest()
        parent = SeasonModel.build_key(season_id)
        return ndb.Key(cls._get_kind(), key_name, parent=parent)

    @classmethod
    def lookup_for_season(cls, season_id=None):
        season_id = season_id or SeasonModel.lookup_open()
        if not season_id:
            raise ValueError('season_id is required')
        return cls.query(cls.season_id == season_id).fetch()

    @classmethod
    def lookup_open(cls):
        return cls.query(cls.is_open == True).fetch()


    @classmethod
    def _get_kind(cls):
        return "SCII_MatchModel"
