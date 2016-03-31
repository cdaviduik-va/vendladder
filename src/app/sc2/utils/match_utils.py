""" utils for match """
from app.sc2.utils.player_utils import prettify_name


def get_vs_string_from_match(match):
    """ Given a match and returns a formatted string that contains the players"""
    return get_vs_string_from_names(match.team1_names, match.team2_names)


def get_vs_string_from_names(team1, team2):
    """ Given a list of winners and a list of losers returns a string formatted with the players of the match """
    team1_names = ' & '.join([prettify_name(n) for n in team1])
    team2_names = ' & '.join([prettify_name(n) for n in team2])
    match_string = '{team1} @ {team2}'.format(team1=team1_names, team2=team2_names)
    return match_string
