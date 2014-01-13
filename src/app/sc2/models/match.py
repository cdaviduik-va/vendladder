"""
match.py Documentation
"""
from google.appengine.ext import ndb



class MatchModel(ndb.Model):
    """
    Models a match
    """
    best_of = ndb.IntegerProperty()
    start_date = ndb.DateProperty()
    window_days = ndb.IntegerProperty()
    team1_players = ndb.StringProperty(repeated=True)
    team2_players = ndb.StringProperty(repeated=True)

    @classmethod
    def _get_kind(cls):
        return "SCII_MatchModel"