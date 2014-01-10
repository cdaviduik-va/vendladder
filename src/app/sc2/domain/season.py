"""
Do stuff with seasons
"""
import datetime
from google.appengine.ext.ndb import Key
from ..models.season import SeasonModel

def create_season(season_name, start_date):
    """
    Creates a season
    """
    date_pieces = start_date.split("-")
    real_start_date = datetime.date(int(date_pieces[0]), int(date_pieces[1]), int(date_pieces[2]))
    season = SeasonModel(season_name=season_name, start_date=real_start_date)
    return season.put()


def season_info(season_key):
    """
    Get info on a season
    """
    if isinstance(season_key, Key):
        return season_key.get()
    return season_key.get_by_id(season_key)