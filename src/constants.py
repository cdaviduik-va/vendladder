DEFAULT_SCORE = 500


class Seasons():
    SEASON_1_2014 = 'SEASON-1-2014'
    VALID_SEASONS = frozenset([SEASON_1_2014])

    CURRENT_SEASON = SEASON_1_2014


class Leagues():
    """
    Corresponds to: http://en.wikipedia.org/wiki/Elo_rating_system#United_States_Chess_Federation_ratings
    """
    BRONZE = 'Bronze'
    SILVER = 'Silver'
    GOLD = 'Gold'
    PLATINUM = 'Platinum'
    DIAMOND = 'Diamond'
    MASTER = 'Master'
    GRAND_MASTER = 'Grand Master'

    SILVER_THRESHOLD = 800
    GOLD_THRESHOLD = 1200
    PLATINUM_THRESHOLD = 1600
    DIAMOND_THRESHOLD = 2000
    MASTER_THRESHOLD = 2200
    GRAND_MASTER_THRESHOLD = 2400


class Keys():
    WIN = 'win'
    RANDOM = 'random'
