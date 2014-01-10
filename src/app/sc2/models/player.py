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

    def build_key(self):
        return str(uuid.uuid4())