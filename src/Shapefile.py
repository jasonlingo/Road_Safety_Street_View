import shapefile as shp
import pygmaps
import sys
import os
import webbrowser

class ShapeType(object):
    ALL = ""

    BRIDLEWAY = "bridleway"

    CONSTRUCTION = "construction"
    CYCLEWAY = "cycleway"

    ELEVATOR = "elevator"

    FOOTWAY = "footway"

    LIVING_STREET = "living_street"

    MOTORWAY = "motorway"
    MOTORWAY_LINK = "motorway_link"

    PATH = "path"
    PEDESTRIAN = "pedestrian"
    PLANNED = "planned"
    PRIMARY = "primary"
    PRIMARY_LINK = "primary_link"
    PROPOSED = "proposed"

    RACEWAY = "raceway"
    RESIDENTIAL = "residential"
    ROAD = "road"

    SECONDARY = "secondary"
    SECONDARY_LINK = "secondary_link"
    SERVICE = "service"
    SERVICES = "services"
    STEPS = "steps"

    TERTIARY = "tertiary"
    TERTIARY_LINK = "tertiary_link"
    TRACK = "track"
    TRUNK = "trunk"
    TRUNK_LINK = "trunk_link"

    UNCLASSIFIED = "unclassified"


class ShapeFileParser(object):

    SHAPE_TYPE_INDEX = 3

    def __init__(self, shapefile):
        self.shapefile = shapefile
        self.intersections = None
        self.shapeReader = shp.Reader(shapefile)

    def getShapeTypePoints(self, type):
        """
        Get the intersection and find the center of each of them.
        :param type: (list of str) the target types
        :return:
        """
        return [sr.shape.points for sr in self.shapeReader.iterShapeRecords()
                if sr.record[ShapeFileParser.SHAPE_TYPE_INDEX] in type or ShapeType.ALL in type]


# ===== testing =====
# file = "../shapefile/Bangkok-shp/shape/roads.shp"
# shpRead = ShapeFileParser(file)
# types = []
# types.append(ShapeType.ALL)
# # types.append(ShapeType.ROAD)
# # types.append(ShapeType.MOTORWAY)
# # types.append(ShapeType.MOTORWAY_LINK)
# # types.append(ShapeType.PATH)
# # types.append(ShapeType.PRIMARY)
# # types.append(ShapeType.PRIMARY_LINK)
# # types.append(ShapeType.SECONDARY)
# # types.append(ShapeType.SECONDARY_LINK)
# # types.append(ShapeType.TERTIARY)
# # types.append(ShapeType.TERTIARY_LINK)
#
# points = shpRead.getShapeTypePoints(types)
# print len(points)

# find the center of the map
# separate the first and last points of a road from other points
# maxLat = -sys.maxint
# minLat = sys.maxint
# maxLng = -sys.maxint
# minLng = sys.maxint
# endPoint = []
# middlePoint = []
# for point in points:
#     for i, p in enumerate(point):
#         maxLat = max(maxLat, p[1])
#         minLat = min(minLat, p[1])
#         maxLng = max(maxLng, p[0])
#         minLng = min(minLng, p[0])
#         if i == 0 or i == len(point):
#             endPoint.append(p)
#         else:
#             middlePoint.append(p)
#
# centerLat = (maxLat + minLat) / 2.0
# centerLng = (maxLng + minLng) / 2.0
#
# # plot map
# mymap = pygmaps.maps(centerLat, centerLng, 12)
#
# for point in endPoint:
#     mymap.addpoint(point[1], point[0], "#00FF00")
# # for point in middlePoint:
# #     mymap.addpoint(point[1], point[0], "#0000FF")
#
# mapFilename = "shapefileMap.html"
# mymap.draw('./' + mapFilename)
#
# # Open the map file on a web browser.
# url = "file://" + os.getcwd() + "/" + mapFilename
# webbrowser.open_new(url)