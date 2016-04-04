from datetime import datetime, timedelta

from google.appengine.ext import testbed

from app.sc2.domain import slack
from app.sc2.models.match import MatchModel

import mock
from unittest import TestCase


class AlertMatchClosedOtwTests(TestCase):
    def setUp(self):
        super(AlertMatchClosedOtwTests, self).setUp()
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_urlfetch_stub()

        patcher = mock.patch('app.sc2.models.match.MatchModel.team1_names',
                             new_callable=mock.PropertyMock(return_value=['Randy Savage', 'Hulk Hogan']))

        self.team1_patcher = patcher.start()
        self.addCleanup(patcher.stop)

        patcher = mock.patch('app.sc2.models.match.MatchModel.team2_names',
                             new_callable=mock.PropertyMock(return_value=['Stone Cold', 'Brett Hart']))
        self.team2_patcher = patcher.start()
        self.addCleanup(patcher.stop)

        payload = '{"username": "SC2 Bot", "icon_emoji": ":fallout-thumb:", "fallback": "A match was played/closed", "attachments": [{"color": "good", "fields": [{"value": "Congratulations on the victory Randy S & Hulk H!\nBetter luck next time Stone C & Brett H.", "title": "Match Played"}]}], "channel": "@cberenik"}'
        patcher = mock.patch('json.dumps', return_value=payload)
        self.json_mock = patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self):
        self.testbed.deactivate()

    def test_message_sent_to_slack(self):
        response = slack.alert_match_closed_async(MatchModel(team1_wins=2, team2_wins=1)).get_result()
        self.assertEqual(200, response.status_code)


class UpdateChannelTopicTests(TestCase):
    def setUp(self):
        super(UpdateChannelTopicTests, self).setUp()
        patcher = mock.patch('app.sc2.domain.slack.urlfetch.fetch')
        self.urlfetch_patcher = patcher.start()
        self.addCleanup(patcher.stop)

        patcher = mock.patch('app.sc2.models.match.MatchModel.team1_names',
                             new_callable=mock.PropertyMock(return_value=['Randy Savage', 'Hulk Hogan']))
        self.team1_patcher = patcher.start()
        self.addCleanup(patcher.stop)

        patcher = mock.patch('app.sc2.models.match.MatchModel.team2_names',
                             new_callable=mock.PropertyMock(return_value=['Stone Cold', 'Brett Hart']))
        self.team2_patcher = patcher.start()
        self.addCleanup(patcher.stop)
        self.match = MatchModel()

    def test_makes_call_to_slack(self):
        slack.update_channel_topic_with_open_games('channel-id', [self.match])
        self.assertEqual(1, self.urlfetch_patcher.call_count)


class DetermineMatchWinnerLoserTests(TestCase):
    def setUp(self):
        super(DetermineMatchWinnerLoserTests, self).setUp()
        patcher = mock.patch('app.sc2.models.match.MatchModel.team1_names',
                             new_callable=mock.PropertyMock(return_value=['Randy Savage', 'Hulk Hogan']))
        self.team1_patcher = patcher.start()
        self.addCleanup(patcher.stop)

        patcher = mock.patch('app.sc2.models.match.MatchModel.team2_names',
                             new_callable=mock.PropertyMock(return_value=['Stone Cold', 'Brett Hart']))
        self.team2_patcher = patcher.start()
        self.addCleanup(patcher.stop)
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
    @mock.patch('app.sc2.models.match.MatchModel.team1_names',
                new_callable=mock.PropertyMock(return_value=['Randy Savage', 'Steve Austin']))
    @mock.patch('app.sc2.models.match.MatchModel.team2_names',
                new_callable=mock.PropertyMock(return_value=['Ric Flair', 'Vince McMahon']))
    def test_winner_data_returned(self, team2_mock, team1_mock):
        expect = {
            'attachments': [{
                'color': 'good',
                'fields': [{
                    'value': 'Congratulations on the victory Randy S & Steve A!\nBetter luck next time Ric F & Vince M.',
                    'title': 'Match Played'
                }]
            }],
            'icon_emoji': ':fallout-thumb:'
        }

        result = slack.get_message_data(MatchModel(team1_wins=2, team2_wins=1))
        self.assertDictEqual(expect, result)

    @mock.patch('app.sc2.models.match.MatchModel.team1_names',
                new_callable=mock.PropertyMock(return_value=['Randy Savage', 'Steve Austin']))
    @mock.patch('app.sc2.models.match.MatchModel.team2_names',
                new_callable=mock.PropertyMock(return_value=['Ric Flair', 'Vince McMahon']))
    def test_closed_data_returned(self, team2_mock, team1_mock):
        expect = {
            'attachments': [{
                'color': 'danger',
                'fields': [{
                    'value': 'Due to unforseen circumstances the match between Randy S & Steve A '
                             'vs. Ric F & Vince M has been closed.',
                    'title': 'Match Closed'
                }]
            }],
            'icon_emoji': ':disappoint:'
        }

        result = slack.get_message_data(MatchModel(team1_wins=0, team2_wins=0, created=datetime.now()))
        self.assertDictEqual(expect, result)

    @mock.patch('app.sc2.models.match.MatchModel.team1_names',
                new_callable=mock.PropertyMock(return_value=['Randy Savage', 'Steve Austin']))
    @mock.patch('app.sc2.models.match.MatchModel.team2_names',
                new_callable=mock.PropertyMock(return_value=['Ric Flair', 'Vince McMahon']))
    def test_closed_after_13_days_data_returned(self, team2_mock, team1_mock):
        expect = {
            'attachments': [{
                'color': 'danger',
                'fields': [{
                    'value': 'Due to inactivity the match between Randy S & Steve A '
                             'vs. Ric F & Vince M has been closed.',
                    'title': 'Match Closed'
                }]
            }],
            'icon_emoji': ':brucehrm:'
        }

        start_date = datetime.now() - timedelta(days=14)

        result = slack.get_message_data(MatchModel(team1_wins=0, team2_wins=0, created=start_date))
        self.assertDictEqual(expect, result)


class GetVsStringFromMatchTests(TestCase):
    @mock.patch('app.sc2.models.match.MatchModel.team1_names',
                new_callable=mock.PropertyMock(return_value=['Randy Savage']))
    @mock.patch('app.sc2.models.match.MatchModel.team2_names',
                new_callable=mock.PropertyMock(return_value=['Steve Austin']))
    def test_single_player_match_formats_correctly(self, team2_mock, team1_mock):
        expect = "Randy S vs. Steve A"
        result = slack.get_vs_string_from_match(MatchModel())
        self.assertEqual(expect, result)

    @mock.patch('app.sc2.models.match.MatchModel.team1_names',
                new_callable=mock.PropertyMock(return_value=['Randy Savage', 'Steve Austin']))
    @mock.patch('app.sc2.models.match.MatchModel.team2_names',
                new_callable=mock.PropertyMock(return_value=['Ric Flair', 'Vince McMahon']))
    def test_two_player_match_formats_correctly(self, team2_mock, team1_mock):
        expect = "Randy S & Steve A vs. Ric F & Vince M"
        result = slack.get_vs_string_from_match(MatchModel())
        self.assertEqual(expect, result)

    @mock.patch('app.sc2.models.match.MatchModel.team1_names',
                new_callable=mock.PropertyMock(return_value=['Randy Savage', 'Steve Austin', 'Undertaker']))
    @mock.patch('app.sc2.models.match.MatchModel.team2_names',
                new_callable=mock.PropertyMock(return_value=['Ric Flair', 'Vince McMahon', ' Triple H']))
    def test_three_player_match_formats_correctly(self, team2_mock, team1_mock):
        expect = 'Randy S & Steve A & Undertaker vs. Ric F & Vince M & Triple H'
        result = slack.get_vs_string_from_match(MatchModel())
        self.assertEqual(expect, result)

    @mock.patch('app.sc2.models.match.MatchModel.team1_names',
                new_callable=mock.PropertyMock(return_value=['Randy Savage', 'Hulk Hogan']))
    @mock.patch('app.sc2.models.match.MatchModel.team2_names',
                new_callable=mock.PropertyMock(return_value=['Ric Flair', 'Sting']))
    def test_match_string_works_with_mixed_length_names(self, team2_mock, team1_mock):
        expect = 'Randy S & Hulk H vs. Ric F & Sting'
        result = slack.get_vs_string_from_match(MatchModel())
        self.assertEqual(expect, result)
