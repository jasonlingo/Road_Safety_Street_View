import urllib
import json
import requests
from collections import namedtuple
from Settings import GOOGLE_API_KEY
from pprint import pprint



class GoogleStreetView(object):

    # the api request address
    STREET_IMAGE_API = "https://maps.googleapis.com/maps/api/streetview?" \
                             "size=640x640&" \
                             "location=%f,%f&" \
                             "heading=%f&" \
                             "pov=%f&" \
                             "pitch=%f&" \
                             "key=" + GOOGLE_API_KEY

    # the metadata request address
    METADATA_API = "https://maps.googleapis.com/maps/api/streetview/metadata?"
                             # "size=640x640&" \
                             # "location=%f,%f&" \
                             # "heading=%f&" \
                             # "pov=%f&" \
                             # "pitch=%f&" \
                             # "key=" + GOOGLE_API_KEY

    @classmethod
    def isValidPoint(cls, params):
        response = requests.get(url=cls.METADATA_API, params=params)
        data = json.loads(response.text)
        return data["status"] == "OK"


    @classmethod
    def downloadStreetView(cls, params, imgPathAndFilename):
        """
        Download street view image according to the given parameters and
        store it to the given file path.
        :param params: (tuple) lat, lng, heading, pov
        :param outputName: (str) the output path and file name
        """
        requestUrl = cls.STREET_IMAGE_API % params
        urllib.urlretrieve(requestUrl, imgPathAndFilename)


class Coordinate(object):

    # For passing the parameters to the API
    StreetViewParam = namedtuple("StreetViewParam", ["lat", "lng", "heading", "pov", "pitch"])

    @classmethod
    def makeParameter(cls, lat, lng, heading, fov=90, pitch=0):
        """
        Make a StreetViewParam tuple according to the given values.
        There is a default value for fov and pitch. If other value

        :param lat: (float) latitude
        :param lng: (float) longitude
        :param heading: (float) the direction:
                        0 or 360 = North; 90 = East; 180 = South; 270 = West
        :param fov: (float) width of the view (0 - 120)
        :param pitch: (float) up or down angle (0 - 90)
        :return: a StreetViewParam tuple
        """
        return cls.StreetViewParam(lat, lng, heading, fov, pitch)

    @classmethod
    def makeParameterDict(cls, lat, lng, heading, fov=90, pitch=0):
        params = dict(
            size="640x640",
            location=str(lat) + "," + str(lng),
            heading=str(heading),
            fov=str(fov),
            pitch=str(pitch),
            key=GOOGLE_API_KEY
        )
        return params


# ===== testing =====
# cwd = os.getcwd()
# filename = cwd + "/" + "test.jpg"
# coord = Coordinate.makeParameter(46.414382, 10.013988, 150)
# GoogleStreetView.downloadStreetView(coord, filename)
# print coord


