"""
Match domain module
"""
import itertools
from app.sc2.models.player import PlayerRankModel


def get_suggested_matches(team_size=2):
    """
    Compile list of players this season who have played least number of games then pair them up to
    create teams with a similar average score.
    """
    player_ranks = PlayerRankModel.lookup_for_current_season()
    if not player_ranks:
        return None

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
        match = Match([player_rank for player_rank in team1], [player_rank for player_rank in team2])
        potential_matches.append(match)

    potential_matches = sorted(potential_matches, key=lambda match: (match.average_games_played, match.score_diff))
    return potential_matches


class Match(object):
    """ Represents a match between two teams. """

    def __init__(self, team1, team2):
        """ A team consists of a list of player ranks. """
        self.team1 = team1
        self.team2 = team2
        self.team1_average_score = sum([player_rank.score for player_rank in self.team1]) / len(self.team1)
        self.team2_average_score = sum([player_rank.score for player_rank in self.team2]) / len(self.team1)
        self.average_games_played = sum([player_rank.games_played for player_rank in self.team1 + self.team2]) / len(self.team1 + self.team2)
        self.score_diff = abs(self.team1_average_score - self.team2_average_score)
