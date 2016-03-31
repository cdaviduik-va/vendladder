""" Slack integration """
import urllib

from google.appengine.api import urlfetch

from app.sc2.domain.match import lookup_open_matches, get_match_player_string_from_match
# from app.sc2.domain.player import prettify_name


def update_channel_topic_with_open_games(channel_id):
    open_matches = lookup_open_matches()
    if open_matches:
        games_to_be_played = '\n'.join([get_match_player_string_from_match(m) for m in open_matches])
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
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
    }
    winner, loser = determine_match_winner(match)

    # winner_names = [prettify_name(n) for n in winner]
    winner_names = winner
    # loser_names = [prettify_name(n) for n in loser]
    loser_names = loser
    winner_string = ' & '.join(winner_names)
    loser_string = ' & '.join(loser_names)

    if winner and loser:
        message = 'Congratulations on the victory {winner}!\nBetter luck next time {loser}'.format(winner=winner_string,
                                                                                                   loser=loser_string)
        fields = [{
            'title': 'Match Played',
            'value': message,
        }]
        colour = 'good'
    else:
        match_string = get_match_player_string_from_match(match)
        message = 'Due to either inactivity or unforseen circumstances the match between {match} has been ' \
                  'closed.'.format(match=match_string)
        fields = [{
            'title': 'Match Closed',
            'value': message,
        }]
        colour = 'bad'

    payload = urllib.urlencode({
        "fallback": "Some fallback text, not sure what for",
        "channel": "@cberenik",
        "username": "SC2 Bot",
        "attachments": [{
            'color': colour,
            'fields': fields,
        }],
        "icon_emoji": ":ghost:"
    })
    urlfetch.fetch(
        'https://hooks.slack.com/services/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',
        payload=payload,
        method=urlfetch.POST,
        headers=headers
    )


def determine_match_winner(match):
    if match.team2_wins > match.team1_wins:
        winner = match.team2_names
        loser = match.team1_names
    elif match.team1_wins > match.team2_wins:
        winner = match.team1_names
        loser = match.team2_names
    else:
        winner = None
        loser = None

    return winner, loser
