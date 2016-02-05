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
    GOLD_THRESHOLD = 600
    PLATINUM_THRESHOLD = 700
    DIAMOND_THRESHOLD = 800
    MASTER_THRESHOLD = 900
    GRAND_MASTER_THRESHOLD = 1000


class Keys():
    WIN = 'win'
    RANDOM = 'random'
