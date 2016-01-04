import logging
import sc2reader

from constants import Keys
from app.sc2.models.player import PlayerModel, PlayerRankModel
from app.sc2.models.game import PlayerStatsModel, GameModel, ReplayModel
from app.sc2.domain.match import create_match, get_match
from app.sc2.domain.season import lookup_current_season


class ReplayReader():
    """
    Class to extract useful information about a set of replay files
    """
    @classmethod
    def ExtractGameInformation(cls, file_name, match_id=None):
        """
        Creates a Game object from a replay file.
        If match_id is not specified a new match will be created based on data from provided replay.
        """
        sc2reader.configure(debug=True)
        replay = sc2reader.load_replay(file_name, load_level=4)

        # TODO: delete this logging
        logging.info('Game Type: ' + replay.game_type)
        logging.info('Category: ' + replay.category)
        for rplayer in replay.players:
            logging.info('Archon Leader Id: ' + str(rplayer.archon_leader_id))

        season_id = lookup_current_season().season_id

        #Gather the player performance stats
        all_player_stats = []
        winning_player_ranks = []
        losing_player_ranks = []
        is_archon_mode = False

        # compile list of players while filtering out ai/observers/referees
        replay_players = [replay_player for replay_player in replay.players
                          if replay_player.is_human and not replay_player.is_observer and not replay_player.is_referee]

        for replay_player in replay_players:
            player_stats = PlayerStatsModel()
            player_stats.battle_net_name = replay_player.name
            player_stats.was_random = replay_player.pick_race.lower() == Keys.RANDOM
            player_stats.race = replay_player.play_race
            if not replay_player.result:
                raise ValueError('Replay must be uploaded by winning player(s).')
            player_stats.won = replay_player.result.lower() == Keys.WIN
            player_stats.handicap = replay_player.handicap
            player_stats.season_id = season_id
            all_player_stats.append(player_stats)

            # create player and rank for this season if one does not exist
            PlayerModel.get_or_create(battle_net_name=replay_player.name)
            player_rank = PlayerRankModel.get_or_create(player_stats.battle_net_name, season_id)
            player_rank.last_game_played = replay.start_time

            if replay.game_type == '2v2':
                player_rank.last_2v2_game_played = replay.start_time

            if player_stats.won:
                winning_player_ranks.append(player_rank)
            else:
                losing_player_ranks.append(player_rank)
            logging.debug("Player: %s (%s) - %s" % (replay_player.name, replay_player.play_race, replay_player.result))

            if replay_player.archon_leader_id:
                # if one of the players is an archon leader than game was played in archon mode
                is_archon_mode = True

            player_rank.put()

        # if no match was provided then create a new one from replay information
        if match_id:
            match = get_match(match_id, season_id)
        else:
            match = create_match([rank.battle_net_name for rank in winning_player_ranks],
                                 [rank.battle_net_name for rank in losing_player_ranks])

        player_names = [player.name for player in replay.players]
        game_key = GameModel.generate_key(replay.start_time, player_names, match.match_id, season_id)
        existing_game = game_key.get()
        if existing_game:
            raise ValueError('This replay has already been uploaded.')

        #Gather the game stats
        game = GameModel(key=game_key)
        game.game_length_seconds = replay.real_length.seconds
        game.game_time = replay.start_time
        game.release = replay.release_string
        game.map_name = replay.map_name
        game.speed = replay.speed
        game.players = all_player_stats
        game.type = replay.real_type
        game.is_archon_mode = is_archon_mode
        game.put()

        replay_entity = ReplayModel()
        file_name.seek(0)
        replay_entity.replay_file = file_name.read()
        replay_entity.key = ReplayModel.build_key(game.game_id)
        replay_entity.put()

        # update_player_ranks(winning_player_ranks, losing_player_ranks)

        match.games_played += 1
        winning_battle_net_names = [player.battle_net_name for player in game.players if player.won]
        if any([bnet_name for bnet_name in match.team1_battle_net_names if bnet_name in winning_battle_net_names]):
            match.team1_wins += 1
        elif any([bnet_name for bnet_name in match.team2_battle_net_names if bnet_name in winning_battle_net_names]):
            match.team2_wins += 1
        match.put()

        #Return the game model
        return game
