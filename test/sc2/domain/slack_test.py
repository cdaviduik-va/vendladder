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
        mocker = mock.patch('app.sc2.domain.slack.lookup_open_matches', return_value=[self.match])
        self.open_matches_patcher = mocker.start()
        self.addCleanup(mocker.stop)

    def test_makes_call_to_slack(self):
        slack.update_channel_topic_with_open_games(self.match)
        self.assertEqual(1, self.urlfetch_patcher.call_count)
