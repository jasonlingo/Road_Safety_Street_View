import shapefile as shp
import pygmaps
import sys
import os
import webbrowser

class ShapeType(object):
    ALL = ""  # 174974 records

    BRIDLEWAY = "bridleway"  # 4 records

    CONSTRUCTION = "construction"  # 310 records
    CYCLEWAY = "cycleway"  # 252 records

    ELEVATOR = "elevator"  # 4 records

    FOOTWAY = "footway"  # 5762 records

    LIVING_STREET = "living_street"  # 3542 records

    MOTORWAY = "motorway"  # 812 records
    MOTORWAY_LINK = "motorway_link"  # 2062

    PATH = "path"  # 1794 records
    PEDESTRIAN = "pedestrian"  # 378 records
    PLANNED = "planned"  # 4 records
    PRIMARY = "primary"  # 3678 records
    PRIMARY_LINK = "primary_link"  # 1938 records
    PROPOSED = "proposed"  # 4 records

    RACEWAY = "raceway"  # 14 records
    RESIDENTIAL = "residential"  # 120238 records
    ROAD = "road"  # 306 records

    SECONDARY = "secondary" # 2404 records
    SECONDARY_LINK = "secondary_link"  # 1304 records
    SERVICE = "service"  # 19294 records
    SERVICES = "services"  # 20 records
    STEPS = "steps"  # 1242 records

    TERTIARY = "tertiary"  # 3186 records
    TERTIARY_LINK = "tertiary_link"  # 694
    TRACK = "track"  # 1018 records
    TRUNK = "trunk"  # 594 records
    TRUNK_LINK = "trunk_link"  # 634 records

    UNCLASSIFIED = "unclassified"  # 3664 records



class ShapeFileParser(object):

    def __init__(self, shapefile, shapeTypeIdx):
        """
        :param shapefile: (str) the file name of the given shape file
        :param shapeTypeIdx: (int) the index of the type store in the shape file
        """
        self.shapefile = shapefile
        self.shapeTypeIdx = shapeTypeIdx
        self.intersections = None
        self.shapeReader = shp.Reader(shapefile)

    def getShapeTypePath(self, type):
        """
        Get the points of paths for the given road types.
        :param type: (list of str) the target types
        :return: a list of paths
        """
        return [sr.shape.points for sr in self.shapeReader.iterShapeRecords()
                if sr.record[self.shapeTypeIdx] in type or ShapeType.ALL in type]


# ===== testing =====
# file = "../shapefile/Bangkok-shp/shape/roads.dbf"
# file = "../shapefile/thailand-latest-free.shp/gis.osm_roads_free_1.shp"
# file = "../shapefile/bangkok_thailand.osm2pgsql-shapefiles/bangkok_thailand_osm_point.shp"
# shpRead = ShapeFileParser(file)
#
# sread = shp.Reader(file)
# roadType = set()
# for sr in sread.iterRecords():
#     print sr
#     break
#     roadType.add(sr[2])
#
# print roadType

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
#
# # find the center of the map
# # separate the first and last points of a road from other points
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