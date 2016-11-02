import urllib
import os
from collections import namedtuple
from Settings import GOOGLE_API_KEY


class GoogleStreetView(object):

    # the api request address
    GOOGLE_STREET_VIEW_API = "https://maps.googleapis.com/maps/api/streetview?" \
                             "size=640x640&" \
                             "location=%f,%f&" \
                             "heading=%f&" \
                             "pov=%f&" \
                             "pitch=%f&" \
                             "key=" + GOOGLE_API_KEY

    @classmethod
    def downloadStreetView(cls, params, imgPathAndFilename):
        """
        Download street view image according to the given parameters and
        store it to the given file path.
        :param params: (tuple) lat, lng, heading, pov
        :param outputName: (str) the output path and file name
        """
        requestUrl = cls.GOOGLE_STREET_VIEW_API % params
        urllib.urlretrieve(requestUrl, imgPathAndFilename)


class Coordinate(object):

    # For passing the parameters to the API
    StreetViewParam = namedtuple("StreetViewParam", ["lat", "lng", "heading", "pov", "pitch"])

    @classmethod
    def makeParam(cls, lat, lng, heading, fov=90, pitch=0):
        return cls.StreetViewParam(lat, lng, heading, fov, pitch)


cwd = os.getcwd()
filename = cwd + "/" + "test.jpg"
coord = Coordinate.makeParam(46.414382, 10.013988, 151.78)
GoogleStreetView.downloadStreetView(coord, filename)



