"""
Filter to version urls.

To use: {{ "/your/static/url/here"|vurl }}
"""
import settings

def do_vurl(url):
    """ Adds versioning to the url to avoid caching problems in static resources (eg images, js, css) """
    version_number = settings.STATIC_VERSION_NUMBER
    if version_number:
        vurl = '/__v%s%s' % (version_number, url)
    else:
        vurl = url
    return vurl
