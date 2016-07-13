import unittest

from app.sc2.domain.match import teams_include_players


class TeamIncludePlayersTests(unittest.TestCase):

    def setUp(self):
        self.include_players = ['FutureNights', 'Toad']
        self.team1_names = ['FutureNights', 'Yatser']
        self.team2_names = ['Toad', 'Nirion']

    def test_returns_true_if_no_included_players_specified(self):
        result = teams_include_players(self.team1_names, self.team2_names)
        self.assertTrue(result)

    def test_returns_true_if_teams_include_specified_players(self):
        result = teams_include_players(self.team1_names, self.team2_names, self.include_players)
        self.assertTrue(result)

    def test_returns_false_if_teams_do_not_include_specified_players(self):
        self.include_players.append('Badger')
        result = teams_include_players(self.team1_names, self.team2_names, self.include_players)
        self.assertFalse(result)
