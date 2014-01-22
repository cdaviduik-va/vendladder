"""
Deals with stuff with users... you know
"""
from google.appengine.ext import ndb
from google.appengine.ext.ndb import Key
from ..models.player import PlayerModel

def create_player(real_name, vend_email, bnet_name, skill_level, season, player_id = None):
    """
    Creates a player from args provided.
    """
    # coerce skill_level from string into an int
    skill_level_int = int(skill_level)
    player = PlayerModel(name=real_name, vendasta_email=vend_email,
                         battle_net_name=bnet_name, skill_level=skill_level_int,
                         season=season)
    if player_id:
        player.key = ndb.Key(PlayerModel._get_kind(), int(player_id))
    player_key = player.put()
    return player_key

def player_info(player_key):
    """
    Returns info based on a key provided
    """
    if isinstance(player_key, Key):
        return player_key.get()
    return PlayerModel.get_by_id(player_key)

def get_players_by_season(season="Winter 1", keys_only=False):
    """
    Returns all player models in a particular season (change default to be the current)
    """
    return PlayerModel.get_players_by_season(season, keys_only)
