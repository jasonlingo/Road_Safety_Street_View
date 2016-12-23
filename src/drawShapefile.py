import os
import sys
import webbrowser
import pygmaps
from shapefileUtil import ShapeFileParser
from shapefileUtil import ShapeType
from settings import SHAPE_TYPE_INDEX
from util import CustomedProgress
from intersection import getSegmentsFromPath


def drawMapFromSegments(filename):
    print "Draw shapefile..."
    shp = ShapeFileParser(filename, SHAPE_TYPE_INDEX)

    types = []
    types.append(ShapeType.PRIMARY)
    allPaths = shp.getPathWithType(types)
    centerLng, centerLat = findCenterFromPaths(allPaths)
    allSegments = getSegmentsFromPath(allPaths)

    plotSegmentOnMap(allSegments, centerLng, centerLat)


def plotSegmentOnMap(allSegs, centerLng, centerLat):

    def printFunc(n):
        sys.stdout.write("\r%d" % n)
    prog = CustomedProgress()
    prog.setThreshold(1000)
    prog.setPrintFunc(printFunc)

    myMap = pygmaps.maps(centerLat, centerLng, 10)

    colors = ["#ff3300", "#3333ff", "#0000", "#ff00ff", "#00e600", "#ff9900", "#66c2ff", "#ffff00"]
    colorIdx = 0

    for seg in allSegs:
        prog.printProgress()
        segPoint = getSegPoint(seg)
        myMap.addpath(segPoint, colors[colorIdx])
        # for point in seg.segment:
        #     myMap.addpoint(point[1], point[0], colors[colorIdx])
        colorIdx = (colorIdx + 1) % len(colors)

    # create map file
    mapFilename = "allPath.html"
    myMap.draw('./' + mapFilename)

    # Open the map file on a web browser.
    url = "file://" + os.getcwd() + "/" + mapFilename
    webbrowser.open_new(url)


def getSegPoint(segment):
    points = []
    for point in segment.segment:
        points.append((point[1], point[0]))
    return points


def drawShapefile(filename):
    print "Draw shapefile..."
    shp = ShapeFileParser(filename, SHAPE_TYPE_INDEX)

    types = []
    types.append(ShapeType.ALL)

    allPaths = shp.getPathWithType(types)
    plotMap(allPaths)


def plotMap(allPaths):
    print "Plot points..., total %d points" % len(allPaths)

    def printFunc(n):
        sys.stdout.write("\r%d" % n)
    prog = CustomedProgress()
    prog.setThreshold(1000)
    prog.setPrintFunc(printFunc)

    centerLng, centerLat = findCenterFromPaths(allPaths)
    myMap = pygmaps.maps(centerLat, centerLng, 10)

    colors = ["#ff3300", "#3333ff", "#0000", "#ff00ff", "#00e600", "#ff9900", "#66c2ff", "#ffff00"]
    colorIdx = 0
    for path in allPaths:
        prog.printProgress()
        pathPoint = getPath(path)
        myMap.addpath(pathPoint, colors[colorIdx])
        colorIdx = (colorIdx + 1) % len(colors)


    # create map file
    mapFilename = "allPath.html"
    myMap.draw('./' + mapFilename)

    # Open the map file on a web browser.
    url = "file://" + os.getcwd() + "/" + mapFilename
    webbrowser.open_new(url)


def findCenterFromPaths(allPaths):
    maxLat = maxLng = -sys.maxint
    minLat = minLng = sys.maxint
    for path in allPaths:
        for point in path.points:
            maxLat = max(maxLat, point[1])
            maxLng = max(maxLng, point[0])
            minLat = min(minLat, point[1])
            minLng = min(minLng, point[0])
    centerLat = (minLat + maxLat) / 2.0
    centerLng = (minLng + maxLng) / 2.0
    return centerLng, centerLat


def getPath(path):
    pathPoints = []
    for point in path.points:
        pathPoints.append((point[1], point[0]))
    return pathPoints


def getAllPathPoints(path):
    allLngs = []
    allLats = []
    for point in path:
        allLngs.append(point[0])
        allLats.append(point[1])
    return allLngs, allLats


if __name__=="__main__":
    filename = "../shapefile/Bangkok-shp/shape/roads.shp"
    drawMapFromSegments(filename)
