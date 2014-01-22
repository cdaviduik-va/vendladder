import sc2reader

from app.sc2.models.game import PlayerPerformanceModel, GameModel, ReplayModel


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
                playerStats.append(player_performance)
                print "Player: %s (%s) - %s" % (player.name, player.play_race, player.result)

        #Gather the game stats
        game = GameModel()
        game.game_length_seconds = replay.real_length.seconds
        game.game_time = replay.start_time
        game.release = replay.release_string
        game.map_name = replay.map_name
        game.speed = replay.speed
        game.players = playerStats
        game.type = replay.real_type
        player_names = [player.name for player in replay.players]
        game.key = GameModel.generate_key(game.game_time, player_names)
        game.put()

        replay_entity = ReplayModel()
        file_name.seek(0)
        replay_entity.replay_file = file_name.read()
        replay_entity.key = ReplayModel.build_key(game.game_id)
        replay_entity.put()

        #Return the game model
        return game
