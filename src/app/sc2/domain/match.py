"""
Match domain module
"""
import itertools
from app.sc2.domain.season import lookup_current_season
from app.sc2.models.game import GameModel
from app.sc2.models.match import MatchModel
from app.sc2.models.player import PlayerRankModel


def create_match(team1, team2):
    """
    Create a new match for the current season where each team is a list of player battle_net_names.
    """
    all_players = team1 + team2
    if any([player for player in all_players if all_players.count(player) > 1]):
        raise ValueError('Player cannot be specified more than once in a match.')

    # ensure the same match does not already exist
    open_matches = lookup_open_matches()
    for match in open_matches:
        if sorted(team1) == sorted(match.team1_battle_net_names) or \
            sorted(team1) == sorted(match.team1_battle_net_names) or \
            sorted(team2) == sorted(match.team1_battle_net_names) or \
            sorted(team2) == sorted(match.team2_battle_net_names):
            raise ValueError('A match already exists with this team.')

    season_id = lookup_current_season(id_only=True)
    key = MatchModel.generate_key(all_players, season_id)
    match = MatchModel(key=key, team1_battle_net_names=team1, team2_battle_net_names=team2)
    match.put()
    return match


def close_match(match_id):
    season_id = lookup_current_season(id_only=True)
    key = MatchModel.build_key(match_id, season_id)
    match = key.get()
    match.is_open = False
    match.games_played = 0
    match.team1_wins = 0
    match.team2_wins = 0

    # update the match with some basic stats from the games played
    games = GameModel.lookup_for_match(match_id)
    for game in games:
        match.games_played += 1
        winning_battle_net_names = [player.battle_net_name for player in game.players if player.won]

        if any([bnet_name for bnet_name in match.team1_battle_net_names if bnet_name in winning_battle_net_names]):
            # team 1 win
            match.team1_wins += 1
        elif any([bnet_name for bnet_name in match.team2_battle_net_names if bnet_name in winning_battle_net_names]):
            # team 2 win
            match.team2_wins += 1

    match.put()


def lookup_matches():
    return MatchModel.lookup_for_season()


def lookup_open_matches():
    return MatchModel.lookup_open()


def lookup_games(limit=None):
    """ Return a list of games. """
    return GameModel.lookup_all(limit=limit)


def get_suggested_matches(team_size=2, exclude_players=None):
    """
    Compile list of players this season who have played least number of games then pair them up to
    create teams with a similar average score.
    """
    player_ranks = PlayerRankModel.lookup_for_current_season()
    if not player_ranks:
        return []

    exclude_players = exclude_players or []
    open_matches = lookup_open_matches()
    for match in open_matches:
        exclude_players += match.team1_battle_net_names
        exclude_players += match.team2_battle_net_names

    player_ranks = sorted(player_ranks, key=lambda player_rank: (player_rank.games_played, player_rank.score), reverse=True)
    all_teams = [team for team in itertools.combinations(player_ranks, team_size)]
    all_matches = [match for match in itertools.combinations(all_teams, 2)]
    potential_matches = []
    for team1, team2 in all_matches:
        team1_names = [player_rank.battle_net_name for player_rank in team1]
        team2_names = [player_rank.battle_net_name for player_rank in team2]
        if set(team1_names) & set(team2_names):
            # skip any matches where same player is on both team
            continue

        is_player_on_team = [player_name for player_name in exclude_players if player_name in team1_names or player_name in team2_names]
        if is_player_on_team:
            continue

        match = SuggestedMatch([player_rank for player_rank in team1], [player_rank for player_rank in team2])
        potential_matches.append(match)

    potential_matches = sorted(potential_matches, key=lambda match: (match.average_games_played, match.score_diff))
    return potential_matches


class SuggestedMatch(object):
    """ Represents a potential match between two teams. """

    def __init__(self, team1, team2):
        """ A team consists of a list of player ranks. """
        self.team1 = team1
        self.team2 = team2
        self.team1_average_score = sum([player_rank.score for player_rank in self.team1]) / len(self.team1)
        self.team2_average_score = sum([player_rank.score for player_rank in self.team2]) / len(self.team1)
        self.average_games_played = sum([player_rank.games_played for player_rank in self.team1 + self.team2]) / len(self.team1 + self.team2)
        self.score_diff = abs(self.team1_average_score - self.team2_average_score)

    def to_dict(self):
        return {
            'team1': [player_rank.battle_net_name for player_rank in self.team1],
            'team2': [player_rank.battle_net_name for player_rank in self.team2],
            'team1_average_score': self.team1_average_score,
            'team2_average_score': self.team2_average_score,
            'average_games_played': self.average_games_played,
            'score_diff': self.score_diff
        }