"""
Deals with stuff with users... you know
"""
from app.utils import calculate_elo_rank
from constants import Seasons
from app.sc2.models.player import PlayerModel, PlayerRankModel


def create_player(battle_net_name, real_name=None, vendasta_email=None, score=None, season=None):
    """
    Creates a player from args provided.
    """
    season = season or Seasons.CURRENT_SEASON
    key = PlayerModel.build_key(battle_net_name)
    if key.get():
        raise ValueError('Player "%s" already exists. Please create a new player.' % battle_net_name)
    player = PlayerModel(key=key, name=real_name, vendasta_email=vendasta_email, seasons_participated=[season])
    player.put()

    player_rank = PlayerRankModel.get_or_create(battle_net_name, Seasons.CURRENT_SEASON)
    player_rank.score = int(score)
    player_rank.put()

    return player


def update_player(battle_net_name, **kwargs):
    score = kwargs.pop('score', None)
    season = kwargs.pop('season', Seasons.CURRENT_SEASON)

    player = PlayerModel.get_or_create(battle_net_name)
    for k, v in kwargs.iteritems():
        setattr(player, k, v)
    player.put()

    if score:
        player_rank = PlayerRankModel.get_or_create(battle_net_name, season)
        player_rank.score = int(score)
        player_rank.put()


def update_player_ranks(winning_player_ranks, losing_player_ranks):
    average_winning_score = sum([w_rank.score for w_rank in winning_player_ranks])
    average_losing_score = sum([l_rank.score for l_rank in losing_player_ranks])

    new_winning_score, new_losing_score = calculate_elo_rank(average_winning_score,
                                                                         average_losing_score)

    win_diff = new_winning_score - average_winning_score
    lose_diff = new_losing_score - average_losing_score

    for p_rank in winning_player_ranks:
        p_rank.games_won += 1
        p_rank.score += int(win_diff)
        p_rank.put()

    for p_rank in losing_player_ranks:
        p_rank.games_lost += 1
        p_rank.score += int(lose_diff)
        p_rank.put()


def get_player_details(battle_net_name, season=None):
    season = season or Seasons.CURRENT_SEASON
    player = PlayerModel.get_or_create(battle_net_name)
    player_rank = PlayerRankModel.get_or_create(battle_net_name, season)
    return PlayerDetails(player, player_rank)


def get_player_details_for_season():
    players = PlayerModel.lookup_for_season()
    all_player_details = []
    for player in players:
        player_rank = PlayerRankModel.get_or_create(player.battle_net_name, Seasons.CURRENT_SEASON)
        player_details = PlayerDetails(player, player_rank)
        all_player_details.append(player_details)
    return sorted(all_player_details, key=lambda player_details: player_details.score, reverse=True)


class PlayerDetails(object):
    """ Contains player and current season rank info. """

    def __init__(self, player, player_rank):
        self.player = player
        self.player_rank = player_rank
        self.score = self.player_rank.score

    def to_dict(self):
        player_dict = self.player.to_dict()
        player_dict.update(self.player_rank.to_dict())
        return player_dict
