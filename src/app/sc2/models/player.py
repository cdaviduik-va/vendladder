"""
Player model
"""
import uuid
from google.appengine.ext import ndb


class PlayerModel(ndb.Model):
    """
    Model for a StarCraft II player
    """
    name = ndb.StringProperty()
    vendasta_email = ndb.StringProperty()
    battle_net_name = ndb.StringProperty()
    skill_level = ndb.Integer()