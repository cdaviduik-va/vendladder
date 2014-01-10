"""
test_replay_parsing.py Documentation
"""
import os
from fixtures.appengine import GaeTestCase
import sc2reader


class TestReplayParsing(GaeTestCase):
    def test_canOpenReplay(self):
        sc2reader.configure(debug=True)
        print os.getcwd()
        replay = sc2reader.load_replay('data/Akilon Wastes (2).SC2Replay')
        print replay

    def test_canExtractPlayers(self):
        sc2reader.configure(debug=True)
        print os.getcwd()
        replay = sc2reader.load_replay('data/Akilon Wastes (2).SC2Replay', load_level=4)
        for player in replay.players:
            if player.is_human:
                print "Player: %s (%s) - %s" % (player.name, player.play_race)