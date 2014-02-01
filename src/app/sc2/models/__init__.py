"""
The model module!
"""

from google.appengine.ext import ndb


class BaseModel(ndb.Model):

    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)