from collections import defaultdict
import datetime
from google.appengine.ext import ndb
from webapp2 import cached_property
from app.sc2.domain.season import lookup_current_season
from app.sc2.models.game import GameModel
from app.sc2.models.player import PlayerModel, PlayerRankModel
from app.sc2.models.season import SeasonModel
from app.sc2.domain.player import get_all_player_details_for_season


class PlayerGameStats(object):

    def __init__(self, battle_net_name):
        self.battle_net_name = battle_net_name

    ### Data properties ###
    @cached_property
    def player(self):
        return PlayerModel.get_by_id(self.battle_net_name)

    @cached_property
    def player_rank(self):
        return PlayerRankModel.build_key(self.battle_net_name, self.current_season_id).get()

    @cached_property
    def current_season_id(self):
        return lookup_current_season(id_only=True)

    @cached_property
    def all_players(self):
        return get_all_player_details_for_season(season_id=self.current_season_id)

    @cached_property
    def games(self):
        return GameModel.lookup_for_player_for_season(self.battle_net_name, season_id=self.current_season_id)

    ### Stat Properties ###
    @property
    def score(self):
        return self.player_rank.score

    @property
    def rank(self):
        player_rank = None
        player_ranks = [i+1 for i, p_details in enumerate(self.all_players)
                        if p_details.player.battle_net_name == self.battle_net_name]
        if player_ranks:
            player_rank = player_ranks[0]
        return player_rank

    @property
    def seasons_participated(self):
        season_keys = [SeasonModel.build_key(season_id) for season_id in self.player.seasons_participated]
        return ndb.get_multi(season_keys)

    @property
    def average_game_length(self):
        seconds = sum([game.game_length_seconds for game in self.games]) / len(self.games)
        return datetime.timedelta(seconds=seconds)

    @property
    def most_played_map(self):
        map_names = [game.map_name for game in self.games]
        if not map_names:
            return None
        return max(set(map_names), key=map_names.count)

    @property
    def favourite_map(self):
        won_maps = []
        for game in self.games:
            if [ps for ps in game.players if ps.battle_net_name == self.battle_net_name and ps.won]:
                won_maps.append(game.map_name)
        if not won_maps:
            return None
        return max(set(won_maps), key=won_maps.count)

    @property
    def favourite_race(self):
        won_race = []
        for game in self.games:
            player_won_stats = [ps for ps in game.players if ps.battle_net_name == self.battle_net_name and ps.won]
            if len(player_won_stats):
                player_stats = player_won_stats[0]
                won_race.append(player_stats.race)
        if not won_race:
            return None
        return max(set(won_race), key=won_race.count)

    @property
    def longest_win_streak(self):
        streak = 0
        longest_streak = 0

        for game in self.games:
            for player in game.players:
                if player.battle_net_name != self.battle_net_name:
                    continue

                if player.won:
                    streak += 1
                else:
                    longest_streak = max(longest_streak, streak)
                    streak = 0

        return longest_streak

    @property
    def nemesis(self):
        # map of player to number of games lost against that player
        player_games_lost_map = defaultdict(int)

        for game in self.games:

            winners = [player.battle_net_name for player in game.players if player.won]
            if self.battle_net_name in winners:
                # if player won then skip because we don't care
                continue

            for winner in winners:
                player_games_lost_map[winner] += 1

        if not player_games_lost_map:
            return None
        return max(player_games_lost_map, key=player_games_lost_map.get)
