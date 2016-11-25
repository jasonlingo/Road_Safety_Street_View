import random
import os
import sys
import pygmaps
import webbrowser
import time

from Settings import SHAPE_FILE
from Settings import SAMPLE_NUM
from Settings import STREET_VIEW_DIRECTORY
from Settings import SHAPE_TYPE_INDEX
from Settings import TARGET_ROAD_TYPES
from Shapefile import ShapeFileParser
from GoogleStreetView import GoogleStreetView, Coordinate

TIME_TO_PAUSE_REQUEST = 25

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


def getValidEndPoint(points):
    validPoints = []
    curtTime = 0
    for point in points:
        curtTime += 1
        if isValidPoint(point):
            validPoints.append(point)
        if curtTime == TIME_TO_PAUSE_REQUEST:
            curtTime = 0
            time.sleep(1)
    return validPoints


def isValidPoint(point):
    """
    Call Google Street Image View metadata API to check the existance
    of the street view image for the given point.
    :return:
    """
    for heading in HEADINGS:
        params = Coordinate.makeParameterDict(point[1], point[0], heading[1])
        if not GoogleStreetView.isValidPoint(params):
            return False
    return True


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


def plotSampledPointMap(points, mapName):
    """
    Plot samples points to the google map.
    :param points:
    :return:
    """
    centerLat, centerLng = getMapCenter(points)
    myMap = pygmaps.maps(centerLat, centerLng, 10)
    for point in points:
        myMap.addpoint(point[1], point[0], "b")

    # create map file
    mapFilename = "%s.html" % mapName
    myMap.draw('./' + mapFilename)

    # Open the map file on a web browser.
    url = "file://" + os.getcwd() + "/" + mapFilename
    webbrowser.open_new(url)


def makeDirectory(directory):
    """
    Check directory is existing. If not exist, then create it.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def sampleAndDownloadStreetImage(endPoints, sampleNum, targetDirectory):
    """
    Randomly select end points from the endPoint collection.
    For each selected end point, call Google map street view image api
    to get the street view images.
    :return:
    """
    print "download street images..."
    sampledPoints = random.sample(endPoints, sampleNum) if sampleNum < len(endPoints) else endPoints
    curtTime = 0
    progress = Progress(10)
    for point in sampledPoints:
        progress.printProgress()
        downloadSurroundingStreetView(point, targetDirectory)
        curtTime += 1
        if curtTime == TIME_TO_PAUSE_REQUEST:
            curtTime = 0
            time.sleep(1)
    return sampledPoints


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
        param = Coordinate.makeParameter(point[1], point[0], heading[1])
        GoogleStreetView.downloadStreetView(param, filename)


class Progress(object):

    def __init__(self, frequency):
        self.count = 0
        self.freq = frequency

    def printProgress(self):
        self.count += 1
        if self.count == self.freq:
            self.count = 0
            print ".",


if __name__ == "__main__":

    # parse shape file and add the desired shape types
    shapefile = ShapeFileParser(SHAPE_FILE, SHAPE_TYPE_INDEX)

    # retrieve end points of the shape types
    print "parse shapefile..."
    paths = shapefile.getShapeTypePath(TARGET_ROAD_TYPES)
    endPoints = getEndPoint(paths)
    print "endPoints: %d" % len(endPoints)
    endPoints = getValidEndPoint(endPoints)
    print "valid endPoints: %d" % len(endPoints)

    # make directory for street images
    makeDirectory(STREET_VIEW_DIRECTORY)

    # Sample street images
    sampledPoints = sampleAndDownloadStreetImage(endPoints, SAMPLE_NUM, STREET_VIEW_DIRECTORY)

    # plot images map
    # plotSampledPointMap(sampledPoints, "map")
