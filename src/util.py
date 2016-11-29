import random
import os
import sys
import pygmaps
import webbrowser
from config import HEADINGS
from GoogleStreetView import GoogleStreetView
from GoogleStreetView import Coordinate


def getEndPoint(path):
    """
    Extract the end points (first and last) from each list of points
    :param path: (list of list of float)
    :return: a list of all end points
    """
    endPoints = []
    for points in path:
        endPoints.append(points[0])
        if len(points) >= 2:
            endPoints.append(points[-1])
    return endPoints


def getValidEndPoint(points):
    validPoints = []
    progress = Progress(10)
    for point in points:
        progress.printProgress()
        if isValidPoint(point):
            validPoints.append(point)
    print ""
    return validPoints


def isValidPoint(point):
    """
    Call Google Street Image View metadata API to check the existance
    of the street view image for the given point.
    :return:
    """
    params = Coordinate.makeParameterDict(point[1], point[0], HEADINGS[0][1])
    return GoogleStreetView.isValidPoint(params)


def removeDuplicatePoint(points):
    pointSet = set()
    uniquePoints = []
    for point in points:
        tuplePoints = tuple(point)
        if tuplePoints not in pointSet:
            uniquePoints.append(point)
            pointSet.add(tuplePoints)
    return uniquePoints


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


def sampleAndDownloadStreetImage(endPoints, sampleNum, picNum, targetDirectory):
    """
    Randomly select end points from the endPoint collection.
    For each selected end point, call Google map street view image api
    to get the street view images.
    :return:
    """
    print "download street images..."
    sampledPoints = random.sample(endPoints, sampleNum) if sampleNum < len(endPoints) else endPoints
    sampleData = []  # store (picture number, file name, lat and lng)
    progress = Progress(10)
    numStep = len(HEADINGS)
    for point in sampledPoints:
        progress.printProgress()
        result = downloadSurroundingStreetView(point, targetDirectory, picNum)
        sampleData += result
        picNum += numStep
    print ""
    return sampleData


def downloadSurroundingStreetView(point, directory, picNum):
    """
    Call Google street view image api to get the four surrounding images at the
    given point.
    :param point: (float, float) longitude and latitude
    :param directory: the directory for saving the images
    """
    googleMapAddr = "https://www.google.com/maps/@%s,%s,15z"
    result = []
    for heading in HEADINGS:
        filename = "%s/%010d_%s_%s_%s.jpg" % (directory, picNum, str(point[1]), str(point[0]), heading[0])
        result.append( [picNum, str(point[1]), str(point[0]), str(point[1]) + "," + str(point[0]), heading[0], filename.split("/")[-1]] )
        param = Coordinate.makeParameter(point[1], point[0], heading[1])
        GoogleStreetView.downloadStreetView(param, filename)
        picNum += 1
    return result


def readPointFile(filename):
    """
    Read points file and return them as a list of points
    :param filename:
    :return: a list of points (lng, lat)
    """
    file = open(filename, "r")
    points = []
    for line in file.readlines():
        point = [float(p.strip(",")) for p in line.split()]
        points.append(point)
    return points


class Progress(object):

    def __init__(self, frequency):
        self.count = 0
        self.freq = frequency

    def printProgress(self):
        self.count += 1
        if self.count == self.freq:
            self.count = 0
            print ".",
