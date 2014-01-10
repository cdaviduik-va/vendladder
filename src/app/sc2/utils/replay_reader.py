from app.sc2.models.game import PlayerPerformanceModel
import sc2reader


class ReplayReader():
    """
    Class to extract useful information about a set of replay files
    """
    @classmethod
    def ExtractGameInformation(cls, file_name):
        """
        Creates a Game object from a replay file
        """
        sc2reader.configure(debug=True)
        replay = sc2reader.load_replay(file_name, load_level=4)

        #Gather the player performance stats
        playerStats = []
        for player in replay.players:
            if player.is_human and not player.is_observer and not player.is_referee:
                player_performance = PlayerPerformanceModel()
                player_performance.name = player.name
                player_performance.was_random = player.pick_race.lower() == 'random'
                player_performance.race = player.play_race
                player_performance.won = player.result.lower() == 'win'
                player_performance.handicap = player.handicap

                print "Player: %s (%s) - %s" % (player.name, player.play_race)

        #Gather the game stats
