DEFAULT_SCORE = 500


class Leagues():
    """
    Corresponds to: http://en.wikipedia.org/wiki/Elo_rating_system#United_States_Chess_Federation_ratings
    """
    BRONZE = 'Recruit'
    SILVER = 'Corporal'
    GOLD = 'Sergeant'
    PLATINUM = 'Captain'
    DIAMOND = 'Commander'
    MASTER = 'Master'
    GRAND_MASTER = 'Executor'

    SILVER_THRESHOLD = 500
    GOLD_THRESHOLD = 800
    PLATINUM_THRESHOLD = 1200
    DIAMOND_THRESHOLD = 1600
    MASTER_THRESHOLD = 2000
    GRAND_MASTER_THRESHOLD = 2400


class Keys():
    WIN = 'win'
    RANDOM = 'random'
