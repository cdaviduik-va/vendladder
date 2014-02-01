"""
Player model
"""
from google.appengine.ext import ndb
from app.sc2.models import BaseModel
from constants import Seasons, Leagues


class PlayerModel(BaseModel):
    """
    Model for a StarCraft II player
    """
    battle_net_name = ndb.ComputedProperty(lambda self: self.key.id())
    name = ndb.StringProperty()
    vendasta_email = ndb.StringProperty()
    player_name = ndb.StringProperty()
    seasons_participated = ndb.StringProperty(repeated=True, choices=Seasons.VALID_SEASONS)

    @classmethod
    def build_key(cls, battle_net_name):
        if not battle_net_name:
            raise ValueError('battle_net_name is required.')
        return ndb.Key(cls._get_kind(), battle_net_name)

    @classmethod
    def get_or_create(cls, battle_net_name):
        key = cls.build_key(battle_net_name)
        player = key.get()
        if not player:
            player = cls(key=key, seasons_participated=[Seasons.CURRENT_SEASON])
            player.put()
        return player

    @classmethod
    def lookup_for_season(cls, season=Seasons.CURRENT_SEASON):
        return cls.query(cls.seasons_participated == season).fetch()

    @classmethod
    def _get_kind(cls):
        return "SCII_PlayerModel"


class PlayerRankModel(BaseModel):
    season = ndb.ComputedProperty(lambda self: self.key.id())
    battle_net_name = ndb.ComputedProperty(lambda self: self.key.parent().id())
    league = ndb.ComputedProperty(lambda self: self.compute_league())
    ratio = ndb.ComputedProperty(lambda self: self.compute_ratio())
    score = ndb.IntegerProperty(default=500)
    games_won = ndb.IntegerProperty(default=0)
    games_lost = ndb.IntegerProperty(default=0)

    @classmethod
    def build_key(cls, battle_net_name, season):
        if not battle_net_name:
            raise ValueError('battle_net_name is required.')
        if not season:
            raise ValueError('season is required.')
        parent = PlayerModel.build_key(battle_net_name)
        return ndb.Key(cls._get_kind(), season, parent=parent)

    @classmethod
    def get_or_create(cls, battle_net_name, season):
        key = cls.build_key(battle_net_name, season)
        player_rank = key.get()
        if not player_rank:
            player_rank = cls(key=key)
            player_rank.put()
        return player_rank

    def compute_league(self):
        if self.score < Leagues.SILVER_THRESHOLD:
            return Leagues.BRONZE
        if self.score < Leagues.GOLD_THRESHOLD:
            return Leagues.SILVER
        if self.score < Leagues.PLATINUM_THRESHOLD:
            return Leagues.GOLD
        if self.score < Leagues.DIAMOND_THRESHOLD:
            return Leagues.PLATINUM
        if self.score < Leagues.MASTER_THRESHOLD:
            return Leagues.DIAMOND
        if self.score < Leagues.GRAND_MASTER_THRESHOLD:
            return Leagues.MASTER
        return Leagues.GRAND_MASTER

    def compute_ratio(self):
        total_num_games = self.games_won + self.games_lost
        if not total_num_games:
            return 0
        return float(self.games_won) / total_num_games
