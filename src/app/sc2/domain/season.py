"""
Do stuff with seasons
"""
import datetime
from ..models.season import SeasonModel

def create_season(season_name, start_date):
    """
    Creates a season
    """
    real_start_date = start_date
    season = SeasonModel(season_name=season_name, start_date=real_start_date)
    return season.put()