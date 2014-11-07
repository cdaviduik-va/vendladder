import datetime
from app.sc2.models.game import GameModel


def lookup_game_stats_for_player(battle_net_name):
    games = GameModel.lookup_for_player(battle_net_name)
    game_stats = GameStats(battle_net_name, games)
    return game_stats


class GameStats(object):

    def __init__(self, battle_net_name, games):
        self.battle_net_name = battle_net_name
        self.games = games
        # self.player_stats = [player_stats for player_stats in [game.players for game in self.games] if player_stats.battle_net_name == battle_net_name]


    @property
    def average_game_length(self):
        seconds = sum([game.game_length_seconds for game in self.games]) / len(self.games)
        return datetime.timedelta(seconds=seconds)

    @property
    def most_played_map(self):
        map_names = [game.map_name for game in self.games]
        return max(set(map_names), key=map_names.count)

    @property
    def favourite_map(self):
        won_maps = []
        for game in self.games:
            if [ps for ps in game.players if ps.battle_net_name == self.battle_net_name and ps.won]:
                won_maps.append(game.map_name)
        return max(set(won_maps), key=won_maps.count)

    @property
    def favourite_race(self):
        won_race = []
        for game in self.games:
            player_won_stats = [ps for ps in game.players if ps.battle_net_name == self.battle_net_name and ps.won]
            if len(player_won_stats):
                player_stats = player_won_stats[0]
                won_race.append(player_stats.race)
        return max(set(won_race), key=won_race.count)


    # most popular map, map with most wins, most common game type, favourite race
