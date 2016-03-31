"""
Deals with stuff with users... you know
"""
import datetime
from collections import defaultdict
from google.appengine.ext import ndb

from app.sc2.domain.season import lookup_current_season
from app.sc2.models.game import GameModel
from app.sc2.models.season import SeasonModel
from app.sc2.models.player import PlayerModel, PlayerRankModel, DEFAULT_IMAGE_URL
from app.utils import calculate_elo_rank


def create_player(battle_net_name, real_name=None, vendasta_email=None, score=None):
    """
    Creates a player from args provided.
    """
    season_id = lookup_current_season().season_id
    key = PlayerModel.build_key(battle_net_name)
    if key.get():
        raise ValueError('Player "%s" already exists. Please create a new player.' % battle_net_name)
    player = PlayerModel(key=key, name=real_name, vendasta_email=vendasta_email, seasons_participated=[season_id])
    player.put()

    player_rank = PlayerRankModel.get_or_create(battle_net_name, season_id)
    player_rank.score = int(score)
    player_rank.put()

    return player


def update_player(battle_net_name, **kwargs):
    score = kwargs.pop('score', None)
    is_participating = kwargs.pop('is_participating', None)
    season_id = kwargs.pop('season_id', None) or lookup_current_season(id_only=True)

    player = PlayerModel.get_or_create(battle_net_name)
    player_rank = PlayerRankModel.get_or_create(battle_net_name, season_id)

    for k, v in kwargs.iteritems():
        setattr(player, k, v)

    if score:
        player_rank.score = int(score)

    if is_participating:
        if season_id not in player.seasons_participated:
            player.seasons_participated.append(season_id)
    elif season_id in player.seasons_participated:
        player.seasons_participated.remove(season_id)

    player_rank.is_participating = is_participating

    player.put()
    player_rank.put()


def update_player_ranks(winning_player_ranks, losing_player_ranks):
    average_winning_score = sum([w_rank.score for w_rank in winning_player_ranks]) / len(winning_player_ranks)
    average_losing_score = sum([l_rank.score for l_rank in losing_player_ranks]) / len(losing_player_ranks)

    new_winning_score, new_losing_score = calculate_elo_rank(average_winning_score, average_losing_score)
    win_diff = new_winning_score - average_winning_score
    lose_diff = new_losing_score - average_losing_score

    for p_rank in winning_player_ranks:
        # p_rank.games_won += 1
        p_rank.score += int(win_diff)
        p_rank.put()

    for p_rank in losing_player_ranks:
        # p_rank.games_lost += 1
        p_rank.score += int(lose_diff)
        p_rank.put()


def lookup_players_for_season(season_id=None):
    season_id = season_id or lookup_current_season(id_only=True)
    return PlayerModel.lookup_for_season(season_id=season_id)


def lookup_players_with_similar_score(battle_net_name, season_id=None, limit=5):
    target_player = get_player_details(battle_net_name)
    all_players = get_all_player_details_for_season()
    sorted_players = sorted([ap for ap in all_players if ap.battle_net_name != target_player.battle_net_name], key=lambda player: abs(target_player.score - player.score))
    return sorted_players[:limit]


def get_player_details(battle_net_name, season_id=None):
    return PlayerDetails.get_for_battle_net_name(battle_net_name)


def get_all_player_details_for_season(season_id=None):
    season_id = season_id or lookup_current_season(id_only=True)
    players = PlayerModel.lookup_for_season(season_id=season_id)
    all_player_details = []
    for player in players:
        player_rank = PlayerRankModel.get_or_create(player.battle_net_name, season_id)
        is_participating = season_id in player.seasons_participated
        player_details = PlayerDetails(player, player_rank, is_participating=is_participating)
        all_player_details.append(player_details)
    return sorted(all_player_details, key=lambda player_details: player_details.score, reverse=True)


def get_players_for_battle_net_names(bnet_names, season_id):
    return [get_player_details(bnet_name, season_id=season_id) for bnet_name in bnet_names]


def get_player_for_email(email):
    return PlayerDetails.get_for_email(email)


def get_player_stats(battle_net_name, season_id=None):
    player_details = get_player_details(battle_net_name, season_id=season_id)
    player_details_data = player_details.to_dict()

    season_id = season_id or player_details.player_rank.season_id

    games = GameModel.lookup_for_player_for_season(battle_net_name, season_id=season_id)

    season_keys = [SeasonModel.build_key(season_id) for season_id in player_details.player.seasons_participated]
    seasons = ndb.get_multi(season_keys)

    won_maps = []
    won_race = []
    map_names = []
    favourite_map = None
    favourite_race = None
    most_played_map = None
    streak = 0
    longest_streak = 0
    player_games_lost_map = defaultdict(int)
    average_game_length = 0
    nemesis = None
    for game in games:
        map_names.append(game.map_name)
        player_won_stats = [ps for ps in game.players if ps.battle_net_name == battle_net_name and ps.won]
        winners = [player.battle_net_name for player in game.players if player.won]

        if player_won_stats:
            player_stats = player_won_stats[0]
            won_maps.append(game.map_name)
            won_race.append(player_stats.race)
            streak += 1
        else:
            longest_streak = max(longest_streak, streak)
            streak = 0

        if battle_net_name in winners:
            # if player won then skip because we don't care
            continue

        for winner in winners:
            player_games_lost_map[winner] += 1

    longest_streak = max(longest_streak, streak)
    if won_maps:
        favourite_map = max(set(won_maps), key=won_maps.count)
    if won_race:
        favourite_race = max(set(won_race), key=won_race.count)
    if map_names:
        most_played_map = max(set(map_names), key=map_names.count)
    if player_games_lost_map:
        nemesis = get_player_details(max(player_games_lost_map, key=player_games_lost_map.get), season_id=season_id)
    if games:
        seconds = sum([game.game_length_seconds for game in games]) / len(games)
        average_game_length = str(datetime.timedelta(seconds=seconds))

    player_details_data['stats'] = {
        'seasons_participated': seasons,
        'average_game_length': str(average_game_length),
        'favourite_map': favourite_map,
        'favourite_race': favourite_race,
        'most_played_map': most_played_map,
        'longest_streak': longest_streak,
        'nemesis': nemesis,
    }
    return player_details_data


class PlayerDetails(object):
    """ Contains player and current season rank info. """

    def __init__(self, player, player_rank, is_participating=True):
        self.player = player
        self.player.image_url = self.player.image_url or DEFAULT_IMAGE_URL
        self.battle_net_name = self.player.battle_net_name
        self.player_rank = player_rank
        self.score = self.player_rank.score
        self.is_participating = is_participating

    def to_dict(self):
        player_dict = self.player.to_dict()
        player_dict.update(self.player_rank.to_dict())
        player_dict['is_participating'] = self.is_participating
        return player_dict

    @classmethod
    def get_for_battle_net_name(cls, battle_net_name, season_id=None):
        player = PlayerModel.get_or_create(battle_net_name)
        return cls.get_for_player(player, season_id=season_id)

    @classmethod
    def get_for_email(cls, email, season_id=None):
        player = PlayerModel.get_for_email(email)
        if not player:
            return None
        return cls.get_for_player(player, season_id=season_id)

    @classmethod
    def get_for_player(cls, player, season_id=None):
        season_id = season_id or lookup_current_season(id_only=True)
        player_rank = PlayerRankModel.get_or_create(player.battle_net_name, season_id)
        is_participating = season_id in player.seasons_participated
        return PlayerDetails(player, player_rank, is_participating=is_participating)
