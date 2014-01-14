"""
round.py Documentation
"""
from google.appengine.ext import ndb


class RoundModel(ndb.Model):
    """
    Models a round of a season
    """
    start_date = ndb.DateProperty()
    duration_days = ndb.IntegerProperty()
    season = ndb.KeyProperty()

    @classmethod
    def _get_kind(cls):
        return "SCII_RoundModel"