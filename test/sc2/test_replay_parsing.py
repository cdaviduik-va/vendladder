"""
test_replay_parsing.py Documentation
"""
import os
from app.sc2.utils.replay_reader import ReplayReader
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
            #if player.is_human:
            print "Player: %s (%s) - %s" % (player.name, player.play_race, player.result)

    def testModelCreation(self):
        data = ReplayReader.ExtractGameInformation('data/Akilon Wastes (2).SC2Replay')
        print data

