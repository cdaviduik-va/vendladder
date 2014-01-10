"""
__init__.py Documentation
"""
import datetime


def jsonDateTimeHandler(obj):
    """
    Custom JSON serializer
    """
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.isoformat()
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    raise Exception('Unrecognized type: %r (value %r)' % (type(obj), obj))