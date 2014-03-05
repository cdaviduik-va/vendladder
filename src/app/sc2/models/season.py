"""
season.py Documentation
"""
from google.appengine.ext import ndb
from app.sc2.models import BaseModel


class SeasonModel(BaseModel):
    """
    Models a season
    """
    season_id = ndb.ComputedProperty(lambda self: self.key.id())
    season_name = ndb.StringProperty()
    start_date = ndb.DateProperty()
    is_open = ndb.BooleanProperty(default=True)

    @classmethod
    def generate_key(cls, season_name, start_date):
        if not season_name:
            raise ValueError('season_name is required.')
        if not start_date:
            raise ValueError('start_date is required.')
        key_name = '%s-%s' % (start_date.isoformat(), season_name.replace(' ', ''))
        return ndb.Key(cls, key_name)

    @classmethod
    def build_key(cls, season_id):
        if not season_id:
            raise ValueError('season_id is required.')
        return ndb.Key(cls, season_id)

    @classmethod
    def lookup_open(cls):
        return cls.query(cls.is_open == True).get()

    @classmethod
    def _get_kind(cls):
        return "SCII_SeasonModel"
