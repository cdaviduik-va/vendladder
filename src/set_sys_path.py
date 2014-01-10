"""
- define method to update sys.path, AND
- run method in this file.  This way, it is run only once.
"""
import os
import sys

def setSysPath():
    """
    Add lib as primary libraries directory
    """
    c = os.path.abspath(os.path.dirname(__file__))

    add = [
        ['lib'],
    ]

    for item in add:
        p = os.path.join(c, *item)
        if not p in sys.path:
            sys.path[1:1] = [p]

    remove = ['django', 'simplejson']

    # Remove unwanted paths
    for item in sys.path:
        for r in remove:
            if item.find(r) > 0:
                sys.path.remove(item)

setSysPath()
