""" Slack integration """
import urllib

from google.appengine.api import urlfetch

from app.sc2.domain.match import lookup_open_matches, get_match_player_string_from_match


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
