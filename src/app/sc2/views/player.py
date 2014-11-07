"""
players.py Documentation
"""
import json
from app.sc2.domain.game import lookup_game_stats_for_player
from app.sc2.domain.player import get_player_details_for_season, get_player_details
from app.sc2.utils import jsonDateTimeHandler
from app.sc2.views import UserView


class PlayerIndex(UserView):
    """
    Lists the current players in the tournament
    """
    def get(self):
        """
        See above
        """
        players = get_player_details_for_season()
        data = {
            'playersJson': json.dumps(players, default=jsonDateTimeHandler)
        }
        self.render_response('sc2/players/index.html', **data)


class PlayerDetails(UserView):

    def get(self, battle_net_name):
        all_players = get_player_details_for_season()
        details = get_player_details(battle_net_name)
        player_rank = None
        player_ranks = [i+1 for i, p_details in enumerate(all_players) if p_details.player.battle_net_name == battle_net_name]
        if player_ranks:
            player_rank = player_ranks[0]
        data = {
            'details': details,
            'game_stats': lookup_game_stats_for_player(battle_net_name),
            'player_rank': player_rank
        }
        self.render_response('sc2/players/details.html', **data)
