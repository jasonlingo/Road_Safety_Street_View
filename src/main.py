import random
import os
import sys
import pygmaps
import webbrowser

from Settings import SHAPE_FILE, SAMPLE_NUM, STREET_VIEW_DIRECTORY
from Shapefile import ShapeFileParser, ShapeType
from GoogleStreetView import GoogleStreetView, Coordinate

def getEndPoint(path):
    """
    Extract the end points (first and last) from each list of points
    :param path: (list of list of float)
    :return: a list of all end points
    """
    endPoints = []
    for points in path:
        endPoints.append(points[0])
        endPoints.append(points[-1])
    return endPoints


# def genFilename(point, heading):
#     """
#     Generate the file name according to the given point and heading.
#     The file name will be the format: lat_lng_heading.jpg
#     :param point: (float, float) longitude, latitude
#     :param heading: the direction
#     :return:
#     """
#     return "%f_%f_%s.jpg" % (point[1], point[0], heading[0])


HEADINGS = [["N", 0], ["E", 90], ["S", 180], ["W", 270]]
def downloadSurroundingStreetView(point, directory):
    """
    Call Google street view image api to get the four surrounding images at the
    given point.
    :param point: (float, float) longitude and latitude
    :param directory: the directory for saving the images
    """
    for heading in HEADINGS:
        filename = "%s/%f_%f_%s.jpg" % (directory, point[1], point[0], heading[0])
        coord = Coordinate.makeParameter(point[1], point[0], heading[1])
        GoogleStreetView.downloadStreetView(coord, filename)


def getMapCenter(points):
    """
    :param points: (float, float) longitude, latitude
    :return: (lat, lng)
    """
    maxLat = maxLng = -sys.maxint
    minLat = minLng = sys.maxint
    for point in points:
        maxLat = max(maxLat, point[1])
        maxLng = max(maxLng, point[0])
        minLat = min(minLat, point[1])
        minLng = min(minLng, point[0])
    centerLat = (minLat + maxLat) / 2.0
    centerLng = (minLng + maxLng) / 2.0
    return centerLat, centerLng


def plotSampledPointMap(points):
    """
    Plot samples points to the google map.
    :param points:
    :return:
    """
    centerLat, centerLng = getMapCenter(points)
    myMap = pygmaps.maps(centerLat, centerLng, 12)
    for point in points:
        myMap.addpoint(point[1], point[0], "#00FF00")

    # create map file
    mapFilename = "map.html"
    myMap.draw('./' + mapFilename)

    # Open the map file on a web browser.
    url = "file://" + os.getcwd() + "/" + mapFilename
    webbrowser.open_new(url)

if __name__ == "__main__":

    # parse shape file and add the desired shape types
    shapefile = ShapeFileParser(SHAPE_FILE)
    types = []
    types.append(ShapeType.SECONDARY)
    types.append(ShapeType.SECONDARY_LINK)

    # retrieve end points of the shape types
    print "parse shapefile"
    paths = shapefile.getShapeTypePoints(types)
    endPoints = getEndPoint(paths)

    # Check directory is existing. If not exist, then create it.
    if not os.path.exists(STREET_VIEW_DIRECTORY):
        os.makedirs(STREET_VIEW_DIRECTORY)

    # Randomly select end points from the endPoint collection.
    # For each selected end point, call Google map street view image api
    # to get the street view images.
    print "download street images"
    sampledPoints = random.sample(endPoints, SAMPLE_NUM) if SAMPLE_NUM < len(endPoints) \
                    else endPoints
    for point in sampledPoints:
        downloadSurroundingStreetView(point, STREET_VIEW_DIRECTORY)

    # plot images map
    plotSampledPointMap(sampledPoints)
