"""
Deals with stuff with users... you know
"""
from google.appengine.ext import ndb
from app.sc2.domain.season import lookup_current_season
from app.sc2.models.season import SeasonModel
from app.utils import calculate_elo_rank
from app.sc2.models.player import PlayerModel, PlayerRankModel


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


def lookup_players_for_season(season_id=None):
    season_id = season_id or lookup_current_season(id_only=True)
    return PlayerModel.lookup_for_season(season_id=season_id)


def get_player_details(battle_net_name, season_id=None):
    season_id = season_id or lookup_current_season(id_only=True)
    player = PlayerModel.get_or_create(battle_net_name)
    player_rank = PlayerRankModel.get_or_create(battle_net_name, season_id)
    is_participating = season_id in player.seasons_participated
    return PlayerDetails(player, player_rank, is_participating=is_participating)


def get_player_details_for_season():
    season_id = lookup_current_season(id_only=True)
    players = PlayerModel.lookup_for_season(season_id=season_id)
    all_player_details = []
    for player in players:
        player_rank = PlayerRankModel.get_or_create(player.battle_net_name, season_id)
        is_participating = season_id in player.seasons_participated
        player_details = PlayerDetails(player, player_rank, is_participating=is_participating)
        all_player_details.append(player_details)
    return sorted(all_player_details, key=lambda player_details: player_details.score, reverse=True)


class PlayerDetails(object):
    """ Contains player and current season rank info. """

    def __init__(self, player, player_rank, is_participating=True):
        self.player = player
        self.player_rank = player_rank
        self.score = self.player_rank.score
        self.is_participating = is_participating

    @property
    def seasons_participated(self):
        season_keys = [SeasonModel.build_key(season_id) for season_id in self.player.seasons_participated]
        return ndb.get_multi(season_keys)

    def to_dict(self):
        player_dict = self.player.to_dict()
        player_dict.update(self.player_rank.to_dict())
        player_dict['is_participating'] = self.is_participating
        return player_dict
