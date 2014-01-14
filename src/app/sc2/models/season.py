"""
season.py Documentation
"""
from google.appengine.ext import ndb



class SeasonModel(ndb.Model):
    """
    Models a season
    """
    season_name = ndb.StringProperty()
    start_date = ndb.DateProperty()

    @classmethod
    def _get_kind(cls):
        return "SCII_SeasonModel"