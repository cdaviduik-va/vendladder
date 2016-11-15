""" Slack integration """
from datetime import datetime
import logging
import json

from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import settings
from app.sc2.domain.player import get_pretty_name


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
    payload = json.dumps({
        'token': 'asdf',
        'channel': channel_id,
        'purpose': games_to_be_played,
    })

    headers = {
        'Content-type': 'application/json',
    }

    urlfetch.fetch(
        'https://slack.com/api/channels.setPurpose',
        payload=payload,
        method=urlfetch.POST,
        headers=headers
    )


@ndb.tasklet
def alert_match_closed_async(match):
    """
    Send a message to slack when a match is closed
    :param match: the match that was closed
    """
    if settings.IS_DEV_APPSERVER:
        # Don't post to slack if on local environment
        raise ndb.Return(None)

    headers = {
        'Content-type': 'application/json',
    }
    payload = json.dumps(get_message_data(match))

    rpc = urlfetch.create_rpc()
    urlfetch.make_fetch_call(
        rpc,
        'https://hooks.slack.com/services/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',
        payload=payload,
        method=urlfetch.POST,
        headers=headers
    )
    try:
        result = yield rpc
    except Exception as e:
        # not a huge deal if slack isn't notified, just don't bring down the rest of the request
        logging.error(e.message)
        result = None
    raise ndb.Return(result)


def get_message_data(match):
    """
    Returns a dict of info depending on how the match turned out
    """
    winner, loser = determine_match_winner_loser(match)
    winner_names = ' & '.join([get_pretty_name(n) for n in winner])
    loser_names = ' & '.join([get_pretty_name(n) for n in loser])

    if winner and loser:
        message = 'Congratulations on the victory {winner}!\nBetter luck next time {loser}.'.format(winner=winner_names,
                                                                                                    loser=loser_names)
        title = 'Match Played'
        colour = 'good'
        emoji = ':fallout-thumb:'
    else:
        match_string = get_vs_string_from_match(match)
        date_diff = datetime.now() - match.created
        if date_diff.days > 13:
            circumstance = 'inactivity'
            emoji = ':brucehrm:'
        else:
            circumstance = 'unforseen circumstances'
            emoji = ':disappoint:'
        message = 'Due to {circumstance} the match between {match} has been ' \
                  'closed.'.format(match=match_string, circumstance=circumstance)
        title = 'Match Closed'
        colour = 'danger'

    return {
        'username': 'SC2 Bot',
        'attachments': [{
            'fallback': title,
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


def get_vs_string_from_match(match):
    """ Given a list of winners and a list of losers returns a string formatted with the players of the match """
    team1_names = ' & '.join([get_pretty_name(n) for n in match.team1_names])
    team2_names = ' & '.join([get_pretty_name(n) for n in match.team2_names])
    match_string = '{team1} vs. {team2}'.format(team1=team1_names, team2=team2_names)
    return match_string
