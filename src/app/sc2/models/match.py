"""
match.py Documentation
"""
import hashlib

from google.appengine.ext import ndb

from app.sc2.models import BaseModel
from app.sc2.models.player import PlayerModel
from app.sc2.models.season import SeasonModel


class MatchModel(BaseModel):
    """
    Models a match
    """
    match_id = ndb.ComputedProperty(lambda self: self.key.id())
    season_id = ndb.ComputedProperty(lambda self: self.key.parent().id())
    team1_battle_net_names = ndb.StringProperty(repeated=True)
    team2_battle_net_names = ndb.StringProperty(repeated=True)
    team1_wins = ndb.IntegerProperty(default=0)
    team2_wins = ndb.IntegerProperty(default=0)
    games_played = ndb.IntegerProperty(default=0)
    is_open = ndb.BooleanProperty(default=True)

    @property
    def team1_names(self):
        players = [PlayerModel.build_key(bnet_name).get() for bnet_name in self.team1_battle_net_names]
        return [player.name or player.battle_net_name for player in players]

    @property
    def team2_names(self):
        players = [PlayerModel.build_key(bnet_name).get() for bnet_name in self.team2_battle_net_names]
        return [player.name or player.battle_net_name for player in players]

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
    def lookup_for_season(cls, season_id=None, is_open=None, limit=None):
        season_id = season_id or SeasonModel.lookup_open().season_id
        if not season_id:
            raise ValueError('season_id is required')

        query = cls.query(cls.season_id == season_id)
        if is_open is not None:
            query = query.filter(cls.is_open == is_open)

        return query.order(-cls.created).fetch(limit=limit)

    @classmethod
    def lookup_for_battle_net_name(cls, battle_net_name):
        query = cls.query(ndb.OR(cls.team1_battle_net_names == battle_net_name,
                                 cls.team2_battle_net_names == battle_net_name))
        query = query.filter(cls.is_open == True)
        return query.order(-cls.created).fetch()

    @classmethod
    def lookup_open(cls):
        return cls.lookup_for_season(is_open=True)

    @classmethod
    def _get_kind(cls):
        return "SCII_MatchModel"

    def _post_put_hook(self, future):
        """ post put hook """
        # future.check_success()
        # if not self.is_open:
        # from app.sc2.domain.slack import update_channel_topic_with_open_games
        # TODO:slack add channel topic setting here
