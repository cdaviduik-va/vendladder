"""
Player model
"""
from datetime import datetime
from google.appengine.ext import ndb
from app.sc2.models import BaseModel
from app.sc2.models.season import SeasonModel
from constants import Leagues

DEFAULT_IMAGE_URL = 'https://www.vendasta.com/__v965/static/images/team/user-icon.jpg'


class PlayerModel(BaseModel):
    """
    Model for a StarCraft II player
    """
    battle_net_name = ndb.ComputedProperty(lambda self: self.key.id())
    name = ndb.StringProperty()
    vendasta_email = ndb.StringProperty()
    player_name = ndb.StringProperty()
    image_url = ndb.StringProperty(default=DEFAULT_IMAGE_URL)
    seasons_participated = ndb.StringProperty(repeated=True)

    @classmethod
    def build_key(cls, battle_net_name):
        if not battle_net_name:
            raise ValueError('battle_net_name is required.')
        return ndb.Key(cls._get_kind(), battle_net_name)

    @classmethod
    def get_or_create(cls, battle_net_name):
        current_season = SeasonModel.lookup_open()
        key = cls.build_key(battle_net_name)
        player = key.get()
        if not player:
            player = cls(key=key, seasons_participated=[current_season.season_id])
            player.put()
        return player

    @classmethod
    def lookup_for_season(cls, season_id=None):
        if not season_id:
            raise ValueError('season_id is required.')
        return cls.query(cls.seasons_participated == season_id).fetch()

    @classmethod
    def _get_kind(cls):
        return "SCII_PlayerModel"


class PlayerRankModel(BaseModel):
    season_id = ndb.ComputedProperty(lambda self: self.key.id())
    battle_net_name = ndb.ComputedProperty(lambda self: self.key.parent().id())
    league = ndb.ComputedProperty(lambda self: self.compute_league())
    ratio = ndb.ComputedProperty(lambda self: self.compute_ratio())
    score = ndb.IntegerProperty(default=500)
    games_won = ndb.IntegerProperty(default=0)
    games_lost = ndb.IntegerProperty(default=0)
    games_played = ndb.ComputedProperty(lambda self: self.compute_games_played())
    is_participating = ndb.BooleanProperty(default=True)
    last_game_played = ndb.DateTimeProperty()
    last_2v2_game_played = ndb.DateTimeProperty()

    @classmethod
    def build_key(cls, battle_net_name, season_id):
        if not battle_net_name:
            raise ValueError('battle_net_name is required.')
        if not season_id:
            raise ValueError('season_id is required.')
        parent = PlayerModel.build_key(battle_net_name)
        return ndb.Key(cls._get_kind(), season_id, parent=parent)

    @classmethod
    def get_or_create(cls, battle_net_name, season_id):
        key = cls.build_key(battle_net_name, season_id)
        player_rank = key.get()
        if not player_rank:
            player_rank = cls(key=key)
            player_rank.put()
        return player_rank

    @classmethod
    def lookup_for_current_season(cls):
        season_id = SeasonModel.lookup_open().season_id
        return cls.query(cls.season_id == season_id).fetch()

    @classmethod
    def lookup_for_battle_net_name(cls, battle_net_name):
        return cls.query(cls.battle_net_name == battle_net_name).fetch()

    @classmethod
    def _get_kind(cls):
        return "SCII_PlayerRankModel"

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
        if not self.games_played:
            return 0
        return float(self.games_won) / self.games_played

    def compute_games_played(self):
        return self.games_won + self.games_lost

    def get_last_game_played(self, team_size=2):
        last_game_played = self.last_game_played
        if team_size == 2 and self.last_2v2_game_played:
            last_game_played = self.last_2v2_game_played
        return last_game_played or datetime.min
