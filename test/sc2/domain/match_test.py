from app.sc2.domain import match
from app.sc2.models.match import MatchModel

import mock
from unittest import TestCase


class GetMatchPlayerStringFromMatchTests(TestCase):
    @mock.patch('app.sc2.models.match.MatchModel.team1_names',
                new_callable=mock.PropertyMock(return_value=['Randy Savage', 'Hulk Hogan']))
    @mock.patch('app.sc2.models.match.MatchModel.team2_names',
                new_callable=mock.PropertyMock(return_value=['Stone Cold', 'Brett Hart']))
    def test_match_string_returned(self, team2_mock, team1_mock):
        expect = 'Randy S & Hulk H @ Stone C & Brett H;'
        m = MatchModel()
        self.assertEqual(expect, match.get_match_player_string_from_match(m))

    @mock.patch('app.sc2.models.match.MatchModel.team1_names',
                new_callable=mock.PropertyMock(return_value=['Sting', 'Hulk Hogan']))
    @mock.patch('app.sc2.models.match.MatchModel.team2_names',
                new_callable=mock.PropertyMock(return_value=['Stone Cold', 'Undertaker']))
    def test_match_string_works_with_mixed_names(self, team2_mock, team1_mock):
        expect = 'Sting & Hulk H @ Stone C & Undertaker;'
        m = MatchModel()
        self.assertEqual(expect, match.get_match_player_string_from_match(m))
