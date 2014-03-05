"""
Do stuff with seasons
"""
import datetime
from google.appengine.ext.ndb import Key
from app.sc2.models.season import SeasonModel


def create_season(season_name, start_date):
    """
    Creates a season
    """
    if SeasonModel.lookup_open():
        raise ValueError('Cannot create a new season when one is already open. You must end the current season first.')

    date_pieces = start_date.split("-")
    real_start_date = datetime.date(int(date_pieces[0]), int(date_pieces[1]), int(date_pieces[2]))
    key = SeasonModel.generate_key(season_name, real_start_date)
    season = SeasonModel(key=key, season_name=season_name, start_date=real_start_date)
    return season.put()


def lookup_seasons():
    return SeasonModel.lookup_all()


def lookup_current_season(id_only=False):
    season = SeasonModel.lookup_open()
    if id_only:
        return season.season_id
    return season


def close_current_season():
    season = SeasonModel.lookup_open()
    if not season:
        return

    season.is_open = False
    season.put()


def season_info(season_key):
    """
    Get info on a season
    """
    if isinstance(season_key, Key):
        return season_key.get()
    return season_key.get_by_id(season_key)