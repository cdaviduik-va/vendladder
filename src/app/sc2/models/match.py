"""
match.py Documentation
"""
from google.appengine.ext import ndb



class MatchModel(ndb.Model):
    """
    Models a match
    """
    best_of = ndb.IntegerProperty()
    games = ndb.StructuredProperty(GameModel, repeated=True)