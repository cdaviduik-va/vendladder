from app.sc2.domain import slack
from app.sc2.models.match import MatchModel

import mock
from unittest import TestCase


class UpdateChannelTopicTests(TestCase):
    def setUp(self):
        super(UpdateChannelTopicTests, self).setUp()
        mocker = mock.patch('app.sc2.domain.slack.urlfetch.fetch')
        self.urlfetch_patcher = mocker.start()
        self.addCleanup(mocker.stop)

        mocker = mock.patch('app.sc2.models.match.MatchModel.team1_names',
                            new_callable=mock.PropertyMock(return_value=['Randy Savage', 'Hulk Hogan']))
        self.team1_patcher = mocker.start()
        self.addCleanup(mocker.stop)

        mocker = mock.patch('app.sc2.models.match.MatchModel.team2_names',
                            new_callable=mock.PropertyMock(return_value=['Stone Cold', 'Brett Hart']))
        self.team2_patcher = mocker.start()
        self.addCleanup(mocker.stop)
        self.match = MatchModel()

    def test_makes_call_to_slack(self):
        slack.update_channel_topic_with_open_games('channel-id', [self.match])
        self.assertEqual(1, self.urlfetch_patcher.call_count)


class DetermineMatchWinnerLoserTests(TestCase):
    def setUp(self):
        super(DetermineMatchWinnerLoserTests, self).setUp()
        mocker = mock.patch('app.sc2.models.match.MatchModel.team1_names',
                            new_callable=mock.PropertyMock(return_value=['Randy Savage', 'Hulk Hogan']))
        self.team1_patcher = mocker.start()
        self.addCleanup(mocker.stop)

        mocker = mock.patch('app.sc2.models.match.MatchModel.team2_names',
                            new_callable=mock.PropertyMock(return_value=['Stone Cold', 'Brett Hart']))
        self.team2_patcher = mocker.start()
        self.addCleanup(mocker.stop)
        self.match = MatchModel()

    def test_chooses_team1_as_winner_when_they_win(self):
        self.match.team1_wins = 2
        self.match.team2_wins = 1
        expect = (['Randy Savage', 'Hulk Hogan'], ['Stone Cold', 'Brett Hart'])
        self.assertEqual(expect, slack.determine_match_winner_loser(self.match))

    def test_chooses_team2_as_winner_when_they_win(self):
        self.match.team1_wins = 0
        self.match.team2_wins = 3
        expect = (['Stone Cold', 'Brett Hart'], ['Randy Savage', 'Hulk Hogan'])
        self.assertEqual(expect, slack.determine_match_winner_loser(self.match))

    def test_winners_and_losers_is_empty_when_no_matches_played(self):
        self.match.team1_wins = 0
        self.match.team2_wins = 0
        winner, loser = slack.determine_match_winner_loser(self.match)
        self.assertListEqual([], winner)
        self.assertListEqual([], loser)


class GetMessageDataTests(TestCase):
    def test_winner_data_returned(self):
        winners = ['Randy Savage', 'Steve Austin']
        losers = ['Ric Flair', 'Vince McMahon']
        match_string = 'Randy S & Steve A @ Ric F & Vince M'

        expect = {
            'attachments': [{
                'color': 'good',
                'fields': [{
                    'value': 'Congratulations on the victory Randy S & Steve A!\nBetter luck next time Ric F & Vince M',
                    'title': 'Match Played'
                }]
            }],
            'icon_emoji': ':fallout-thumb:'
        }

        result = slack.get_message_data(winners, losers, match_string)
        self.assertDictEqual(expect, result)

    def test_closed_data_returned(self):
        winners = []
        losers = []
        match_string = 'Randy S & Steve A @ Ric F & Vince M'

        expect = {
            'attachments': [{
                'color': 'danger',
                'fields': [{
                    'value': 'Due to either inactivity or unforseen circumstances the match between Randy S & Steve A '
                             '@ Ric F & Vince M has been closed.',
                    'title': 'Match Closed'
                }]
            }],
            'icon_emoji': ':brucehrm:'
        }

        result = slack.get_message_data(winners, losers, match_string)
        self.assertDictEqual(expect, result)
