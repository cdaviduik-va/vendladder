"""
Match domain module
"""
import time
import itertools
import logging

from app.sc2.domain.player import update_player_ranks, prettify_name
from app.sc2.domain.season import lookup_current_season
from app.sc2.models.game import GameModel
from app.sc2.models.match import MatchModel
from app.sc2.models.player import PlayerRankModel

DEFAULT_TEAM_SIZE = 2

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
            raise ValueError('A match already exists with the team: ' + '& '.join(match.team1_battle_net_names) + ' vs. ' + '& '.join(match.team2_battle_net_names))

    # TODO: put slack notification send here
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

    if match.team2_wins != match.team1_wins:
        # do not update rank if match was a tie
        team1_player_ranks = [PlayerRankModel.build_key(bnet_name, match.season_id).get()
                              for bnet_name in match.team1_battle_net_names]
        team2_player_ranks = [PlayerRankModel.build_key(bnet_name, match.season_id).get()
                              for bnet_name in match.team2_battle_net_names]

        # assume team1 won by default
        winning_team_games_won = match.team1_wins
        losing_team_games_won = match.team2_wins
        winning_player_ranks = team1_player_ranks
        losing_player_ranks = team2_player_ranks
        if match.team2_wins > match.team1_wins:
            # actually team2 won
            winning_team_games_won = match.team2_wins
            losing_team_games_won = match.team1_wins
            winning_player_ranks = team2_player_ranks
            losing_player_ranks = team1_player_ranks

        # update number of games won/lost
        for p_rank in winning_player_ranks:
            p_rank.games_won += winning_team_games_won
            p_rank.games_lost += losing_team_games_won

        for p_rank in losing_player_ranks:
            p_rank.games_won += losing_team_games_won
            p_rank.games_lost += winning_team_games_won

        update_player_ranks(winning_player_ranks, losing_player_ranks)

    ### NOTE: Match stats are now calculated when games are uploaded instead of when match is closed.
    # Want to hang on to this code for a bit yet though in case a bug is found.

    # match.games_played = 0
    # match.team1_wins = 0
    # match.team2_wins = 0
    #
    # # update the match with some basic stats from the games played
    # games = GameModel.lookup_for_match(match_id)
    # for game in games:
    #     match.games_played += 1
    #     winning_battle_net_names = [player.battle_net_name for player in game.players if player.won]
    #
    #     if any([bnet_name for bnet_name in match.team1_battle_net_names if bnet_name in winning_battle_net_names]):
    #         # team 1 win
    #         match.team1_wins += 1
    #     elif any([bnet_name for bnet_name in match.team2_battle_net_names if bnet_name in winning_battle_net_names]):
    #         # team 2 win
    #         match.team2_wins += 1

    match.put()


def get_match(match_id, season_id):
    return MatchModel.build_key(match_id, season_id).get()


def lookup_matches(limit=None):
    return MatchModel.lookup_for_season(limit=limit)


def lookup_open_matches():
    return MatchModel.lookup_open()


def lookup_games(limit=None):
    """ Return a list of games. """
    return GameModel.lookup_all(limit=limit)

def log_time_diff(start_time):
    logging.debug('--- %s seconds ---', (time.time() - start_time))

def get_suggested_matches(team_size=DEFAULT_TEAM_SIZE, include_players=None, exclude_players=None, ignore_open=False, limit=20):
    """
    Compile list of players this season who have played least number of games then pair them up to
    create teams with a similar average score.
    """
    start_time = time.time()
    logging.debug('GETTING SUGGESTED MATCHES')
    logging.debug('TEAM SIZE: %d', team_size)
    logging.debug('INCLUDE PLAYERS: %s', include_players)
    logging.debug('EXCLUDE PLAYERS: %s', exclude_players)
    logging.debug('IGNORE OPEN: %s', str(ignore_open))

    player_ranks = PlayerRankModel.lookup_for_current_season()
    if not player_ranks:
        return []

    include_players = include_players or []
    exclude_players = exclude_players or []
    if not ignore_open:
        open_matches = lookup_open_matches()
        for match in open_matches:
            exclude_players += match.team1_battle_net_names
            exclude_players += match.team2_battle_net_names

    # remove players that are not participating or on list of excludes
    valid_player_ranks = []
    for player_rank in player_ranks:
        if not player_rank.is_participating:
            continue

        if player_rank.battle_net_name in exclude_players:
            continue

        valid_player_ranks.append(player_rank)

    player_ranks = sorted(valid_player_ranks, key=lambda player_rank: player_rank.get_last_game_played(team_size=team_size))

    def avg(player_ranks):
        return sum([player_rank.score for player_rank in player_ranks]) / len(player_ranks)

    all_teams = [team for team in itertools.combinations(player_ranks, team_size)
                 if len(set([pr.battle_net_name for pr in team])) == len(team)]
    logging.debug('Number of teams: %d', len(all_teams))
    log_time_diff(start_time)

    all_matches = [SuggestedMatch(t1, t2) for t1, t2 in itertools.combinations(all_teams, 2)]
    all_matches = sorted(all_matches, key=lambda match: match.score_diff)

    logging.debug('Number of matches: %d', len(all_matches))
    log_time_diff(start_time)

    # we only need a handful of matches so grabbing the first 1000 with the smalled score diff should be more than enough
    all_matches = all_matches[:1000]

    potential_matches = []
    for match in all_matches:
        team1 = match.team1
        team2 = match.team2
        team1_names = [player_rank.battle_net_name for player_rank in team1]
        team2_names = [player_rank.battle_net_name for player_rank in team2]

        if set(team1_names) & set(team2_names):
            # skip any matches where same player is on both team
            continue

        if include_players and not (set(team1_names) & set(include_players) or set(team2_names) & set(include_players)):
            # skip teams if players are not in "include" list
            continue

        potential_matches.append(match)

    potential_matches = sorted(potential_matches, key=lambda match: (match.score_diff, match.average_time_since_last_game))
    logging.debug('Number of potential matches: %d', len(potential_matches))
    log_time_diff(start_time)
    return potential_matches[:limit]


class SuggestedMatch(object):
    """ Represents a potential match between two teams. """

    def __init__(self, team1, team2):
        """ A team consists of a list of player ranks. """
        self.team1 = team1
        self.team2 = team2
        self.season_id = self.team1[0].season_id
        self.score_diff = abs(self.team1_average_score - self.team2_average_score)
    @property
    def team1_average_score(self):
        return sum([player_rank.score for player_rank in self.team1]) / len(self.team1)

    @property
    def team2_average_score(self):
        return sum([player_rank.score for player_rank in self.team2]) / len(self.team2)

    @property
    def average_games_played(self):
        return sum([player_rank.games_played for player_rank in self.team1 + self.team2]) / len(self.team1 + self.team2)

    @property
    def average_time_since_last_game(self):
        last_games_played = [player_rank.last_game_played for player_rank in self.team1 + self.team2 if player_rank.last_game_played]
        average_time_since_last_game = 0
        if len(last_games_played) > 0:
            average_time_since_last_game = sum([time.mktime(last_game_played.timetuple()) for last_game_played in last_games_played]) / len(last_games_played)
        return average_time_since_last_game

    def to_dict(self):
        team1_battle_net_names = [player_rank.battle_net_name for player_rank in self.team1]
        team2_battle_net_names = [player_rank.battle_net_name for player_rank in self.team2]
        return {
            'season_id': self.season_id,
            'team1': [player_rank.battle_net_name for player_rank in self.team1],
            'team2': [player_rank.battle_net_name for player_rank in self.team2],
            'team1_battle_net_names': team1_battle_net_names,
            'team2_battle_net_names': team2_battle_net_names,
            'team1_average_score': self.team1_average_score,
            'team2_average_score': self.team2_average_score,
            'average_games_played': self.average_games_played,
            'score_diff': self.score_diff
        }


def get_match_player_string_from_match(match):
    team1_names = [prettify_name(n) for n in match.team1_names]
    team2_names = [prettify_name(n) for n in match.team2_names]

    match_string = '{p1} & {p2} @ {p3} & {p4};'.format(
        p1=team1_names[0],
        p2=team1_names[1],
        p3=team2_names[0],
        p4=team2_names[1],
    )
    return match_string
