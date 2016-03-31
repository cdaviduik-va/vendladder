""" Slack integration """
import urllib

from google.appengine.api import urlfetch

from app.sc2.utils.match_utils import get_vs_string_from_match
from app.sc2.utils.player_utils import prettify_name


# TODO:slack hook this up when auth stuff figured out
def update_channel_topic_with_open_games(channel_id, open_matches):
    """
    Sets the channel topic to the currently open games
    Need to wait until I check out the auth stuff before this will work
    """
    if open_matches:
        games_to_be_played = '\n'.join([get_vs_string_from_match(m) for m in open_matches])
    else:
        games_to_be_played = 'All games have been played! :boom:'

    # TODO: get auth token for slack
    payload = urllib.urlencode({
        'token': 'asdf',
        'channel': channel_id,
        'purpose': games_to_be_played,
    })

    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
    }

    urlfetch.fetch(
        'https://slack.com/api/channels.setPurpose',
        payload=payload,
        method=urlfetch.POST,
        headers=headers
    )


def alert_match_closed(match):
    """
    Send a message to slack when a match is closed
    :param match: the match that was closed
    """
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
    }
    winner, loser = determine_match_winner_loser(match)
    match_string = get_vs_string_from_match(match)

    info_dict = {
        "fallback": "A match was played/closed",
        "username": "SC2 Bot",
    }
    info_dict.update(get_message_data(winner, loser, match_string))

    payload = urllib.urlencode(info_dict)
    urlfetch.fetch(
        'https://hooks.slack.com/services/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',
        payload=payload,
        method=urlfetch.POST,
        headers=headers
    )


def get_message_data(winner, loser, match_string):
    """
    Returns a dict of info depending on how the match turned out
    """
    winner_names = ' & '.join([prettify_name(n) for n in winner])
    loser_names = ' & '.join([prettify_name(n) for n in loser])
    if winner and loser:
        message = 'Congratulations on the victory {winner}!\nBetter luck next time {loser}'.format(winner=winner_names,
                                                                                                   loser=loser_names)
        title = 'Match Played'
        colour = 'good'
        emoji = ':fallout-thumb:'
    else:
        message = 'Due to either inactivity or unforseen circumstances the match between {match} has been ' \
                  'closed.'.format(match=match_string)
        title = 'Match Closed'
        colour = 'danger'
        emoji = ':brucehrm:'

    return {
        'attachments': [{
            'color': colour,
            'fields': [{
                'title': title,
                'value': message,
            }]
        }],
        "icon_emoji": emoji,
    }


def determine_match_winner_loser(match):
    """
    Given a match the winner and loser of the match is determined
    :param match: The match that was played
    :multiple return: the list of the winners of the match followed by the list of the losers of the match, will return
    both as empty list if the match is closed without games played, will return winner as empty list and loser as list
    of all the names if a tie
    """
    if match.team2_wins > match.team1_wins:
        winner = match.team2_names
        loser = match.team1_names
    elif match.team1_wins > match.team2_wins:
        winner = match.team1_names
        loser = match.team2_names
    else:
        winner = []
        loser = []

    return winner, loser
