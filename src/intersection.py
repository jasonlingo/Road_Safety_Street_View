from __future__ import division

import os
import sys
import math
import threading
import webbrowser
import pygmaps
from util import plotSampledPointMap
from util import haversine
from settings import SHAPE_TYPE_INDEX
from config import HEADINGS
from shapefileUtil import ShapeFileParser
from shapefileUtil import ShapeType
from GoogleStreetView import GoogleStreetView
from util import calcVectAngle
from util import getMapCenter

ALLOWED_DEGREE = 20
LIMIT1 = ALLOWED_DEGREE
LIMIT2 = 360 - ALLOWED_DEGREE
LIMIT3 = 180 - ALLOWED_DEGREE
LIMIT4 = 180 + ALLOWED_DEGREE


class PathPoint(object):

    def __init__(self, type, point):
        self.type = type
        self.point = point


class Intersection(object):

    def __init__(self, point):
        self.point = point
        self.pathPoints = set()
        self.segments = set()


class PathSegment(object):

    def __init__(self, type, point1, point2):
        self.type = type
        self.segment = (point1, point2)

    def findIntersectPoint(self, other):
        if PathSegment.isValidAngle(self.segment, other.segment):
            intersectPoint = PathSegment.lineIntersection(self.segment, other.segment)
            if intersectPoint and PathSegment.isValidIntersectionPoint(intersectPoint, self.segment, other.segment):
                return intersectPoint

    @classmethod
    def isValidAngle(cls, segment1, segment2):
        angle = calcVectAngle(segment1, segment2)
        if angle <= LIMIT1 or angle >= LIMIT2 or (LIMIT3 <= angle <= LIMIT4):
            return False
        else:
            return True

    @classmethod
    def isValidIntersectionPoint(cls, intersectionPoint, line1, line2):
        withinLine1 = PathSegment.isInTheMiddle(intersectionPoint, line1)
        withinLine2 = PathSegment.isInTheMiddle(intersectionPoint, line2)
        if withinLine1 > 0 or withinLine2 > 0:
            return nearbyPoints(intersectionPoint, line1 + line2, 0.001)
        else:
            return True

    @classmethod
    def isInTheMiddle(cls, point, line):
        middleX = (point[0] - line[0][0]) * (point[0] - line[1][0])
        middleY = (point[1] - line[0][1]) * (point[1] - line[1][1])
        if middleX > 0 or middleY > 0:
            return 1
        else:
            return -1

    @classmethod
    def lineIntersection(cls, line1, line2):
        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        div = det(xdiff, ydiff)
        if div == 0:
           return None

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return (x, y)

def nearbyPoints(mainPoint, points, dist):
    nearPointNum = 0
    for point in points:
        distBetween = haversine(mainPoint, point)
        if distBetween <= dist:
            # print distBetween, mainPoint, point
            nearPointNum += 1
    if nearPointNum >= 2:
        return True
    else:
        return False


def getMinMaxLatLng(allPaths):
    maxLat, maxLng = -sys.maxint, -sys.maxint
    minLat, minLng = sys.maxint, sys.maxint
    for path in allPaths:
        pathLngs = [point[0] for point in path.points]
        pathLats = [point[1] for point in path.points]
        maxPathLng = max(pathLngs)
        minPathLng = min(pathLngs)
        maxPathLat = max(pathLats)
        minPathLat = min(pathLats)
        maxLng = max(maxLng, maxPathLng)
        minLng = min(minLng, minPathLng)
        maxLat = max(maxLat, maxPathLat)
        minLat = min(minLat, minPathLat)
    return maxLng, minLng, maxLat, minLat


def genGrids(maxLng, minLng, maxLat, minLat, regionDiv):
    lngDiff = maxLng - minLng
    latDiff = maxLat - minLat
    unitLen = min(lngDiff, latDiff) / regionDiv

    numLngGrid = int(math.ceil(lngDiff / unitLen))
    numLatGrid = int(math.ceil(latDiff / unitLen))

    grids = []
    for _ in range(numLngGrid + 1):
        grids.append([set() for _ in range(numLatGrid + 1)])

    return grids, unitLen


def findIntersection(allPaths):
    print "Find intersections"

    pointDict = {}
    for path in allPaths:
        for point in path.points:
            pointKey = tuple(point)
            if pointKey in pointDict:
                intersection = pointDict[pointKey]
                intersection.pathPoints.add(PathPoint(path.type, point))
            else:
                pointDict[pointKey] = Intersection(point)

    intersections = {}
    for pointKey in pointDict:
        if len(pointDict[pointKey].pathPoints) > 1:
            intersections[pointKey] = pointDict[pointKey]

    return intersections



class FindIntersectionThreading(threading.Thread):

    def __init__(self, allSegments, begin, end, intersections, threadName):
        threading.Thread.__init__(self)
        self.allSegments = allSegments
        self.begin = begin
        self.end = min(end, len(allSegments))
        self.intersections = intersections
        self.threadName = threadName

    def run(self):
        print "Starting" + self.threadName

        compNum = 0.0
        for i in range(self.begin, self.end):
            segment1 = self.allSegments[i]
            for j in range(i + 1, self.end):
                segment2 = self.allSegments[j]
                intersectPoint = segment1.findIntersectPoint(segment2)
                if intersectPoint is not None:
                    if intersectPoint in self.intersections:
                        intersection = self.intersections[intersectPoint]
                    else:
                        intersection = Intersection(intersectPoint)
                        self.intersections[intersectPoint] = intersection
                    intersection.segments.add(segment1)
                    intersection.segments.add(segment2)

            compNum += 1
            if compNum % 10 == 0:
                sys.stdout.write("\r%s %f" % (self.threadName, compNum / (self.end - self.begin)))
                sys.stdout.flush()


def findIntersectionFromSegments(allSegments, start, end, intersections, threadName):

    end = min(end, len(allSegments))

    compNum = 0
    # intersections = {}
    for i in range(start, end):
        segment1 = allSegments[i]
        for j in range(i + 1, end):

            segment2 = allSegments[j]
            intersectPoint = segment1.findIntersectPoint(segment2)
            if intersectPoint is not None:
                if intersectPoint in intersections:
                    intersection = intersections[intersectPoint]
                else:
                    intersection = Intersection(intersectPoint)
                    intersections[intersectPoint] = intersection
                intersection.segments.add(segment1)
                intersection.segments.add(segment2)

        compNum += 1
        if compNum % 1000 == 0:
            sys.stdout.write("\r%s %d" % (threadName, compNum))
            sys.stdout.flush()

    return intersections


def getSegmentsFromPath(allPaths):
    print "Get segments from paths"

    allSegments = []
    for path in allPaths:
        prePoint = path.points[0]
        for point in path.points[1:]:
            segment = PathSegment(path.type, prePoint, point)
            allSegments.append(segment)
            prePoint = point
    return allSegments

def experiment1():
    filename = "../shapefile/Bangkok-shp/shape/roads.shp"
    shp = ShapeFileParser(filename, SHAPE_TYPE_INDEX)

    types = []
    types.append(ShapeType.ALL)
    allPaths = shp.getPathWithType(types)

    # maxLng, minLng, maxLat, minLat = getMinMaxLatLng(allPaths)
    # regionDiv = 10
    # grids, unitLen = genGrids(maxLng, minLng, maxLat, minLat, regionDiv)

    intersections = findIntersection(allPaths)
    points = intersections.keys()
    print "total paths: %d" % len(points)

    validPoints = []
    i = 0
    for point in points:
        param = GoogleStreetView.makeParameterDict(point[1], point[0], HEADINGS[0])
        if GoogleStreetView.isValidPoint(param):
            validPoints.append(point)
        i += 1
        if i % 100 == 0:
            sys.stdout.write("\r%d" % i)

    print "total points: %d" % len(validPoints)

    plotSampledPointMap(validPoints, "intersections")


def experiment2():
    filename = "../shapefile/Bangkok-shp/shape/roads.shp"
    shp = ShapeFileParser(filename, SHAPE_TYPE_INDEX)

    types = []
    types.append(ShapeType.ALL)

    allPaths = shp.getPathWithType(types)
    allSegments = getSegmentsFromPath(allPaths)


    print "Find intersections from %d segments" % len(allSegments)
    totalCompNum = float(len(allSegments) * len(allSegments)) / 2
    print "total comparision: %d" % totalCompNum

    intersectionResuilt = []
    start = 0
    deltaNum = len(allSegments)
    threadNum = 1
    threads = []
    while start < len(allSegments):
        inter = {}
        th = FindIntersectionThreading(allSegments, start, start + deltaNum, inter, "Thread-" + str(threadNum))
        th.start()
        threads.append(th)

        start += deltaNum
        threadNum += 1
        intersectionResuilt.append(inter)

    # intersections = findIntersectionFromSegments(allSegments)

    for th in threads:
        th.join()

    print "end"

    # print "total intersections: %d" % len(intersections)

def insertSegments(grids, unitLen, minLng, minLat, allSegments):
    for pathSeg in allSegments:
        maxRow, minRow, maxCol, minCol = getGridRange(unitLen, minLng, minLat, pathSeg)
        for row in range(minRow, maxRow + 1):
            for col in range(minCol, maxCol + 1):
                try:
                    grids[row][col].add(pathSeg)
                except:
                    print row, col


def getGridRange(unitLen, minLng, minLat, pathSeg):
    row1, col1 = getRowCol(unitLen, minLng, minLat, pathSeg.segment[0])
    row2, col2 = getRowCol(unitLen, minLng, minLat, pathSeg.segment[1])
    maxRow = max(row1, row2)
    minRow = min(row1, row2)
    maxCol = max(col1, col2)
    minCol = min(col1, col2)
    return maxRow, minRow, maxCol, minCol


def getRowCol(unitLen, minLng, minLat, point):
    row = int((point[0] - minLng) / unitLen)
    col = int((point[1] - minLat) / unitLen)
    return row, col


def gridMethod():
    filename = "../shapefile/Bangkok-shp/shape/roads.shp"
    shp = ShapeFileParser(filename, SHAPE_TYPE_INDEX)

    types = []
    types.append(ShapeType.MOTORWAY)


    allPaths = shp.getPathWithType(types)
    allSegments = getSegmentsFromPath(allPaths)

    maxLng, minLng, maxLat, minLat = getMinMaxLatLng(allPaths)
    regionDiv = 1000
    grids, unitLen = genGrids(maxLng, minLng, maxLat, minLat, regionDiv)
    insertSegments(grids, unitLen, minLng, minLat, allSegments)

    print "all segments: %d" % len(allSegments)
    intersections = findIntersectionFromGrids(grids, unitLen, minLng, minLat, allSegments)
    print "intersections: %d" % len(intersections)
    # _ = raw_input("continue?")
    # validPoints = []
    # for point in intersections.keys():
    #     param = GoogleStreetView.makeParameterDict(point[1], point[0], HEADINGS[0])
    #     if GoogleStreetView.isValidPoint(param):
    #         validPoints.append(point)
    #
    # print "total points: %d" % len(validPoints)

    # plotSampledPointMap(intersections.keys(), "gridMap_noCheck")
    plotPointAndSegment(intersections.keys(), allSegments, "grid_segment_noCheck_motorway")
    # plotPointAndPath(intersections.keys(), allPaths, "grid_path_noCheck")


def plotPointAndSegment(points, segments, mapFilename):
    centerLat, centerLng = getMapCenter(points)
    myMap = pygmaps.maps(centerLat, centerLng, 10)

    for point in points:
        myMap.addpoint(point[1], point[0], "b")

    colors = ["#ff3300", "#3333ff", "#0000", "#ff00ff", "#00e600", "#ff9900", "#66c2ff", "#ffff00"]
    colorIdx = 0

    for seg in segments:
        pathPoint = getSegPoint(seg)
        myMap.addpath(pathPoint, colors[colorIdx])
        colorIdx = (colorIdx + 1) % len(colors)


    # create map file
    mapFilename = "%s.html" % mapFilename
    myMap.draw('./' + mapFilename)

    # Open the map file on a web browser.
    url = "file://" + os.getcwd() + "/" + mapFilename
    webbrowser.open_new(url)


def plotPointAndPath(points, paths, mapFilename):
    centerLat, centerLng = getMapCenter(points)
    myMap = pygmaps.maps(centerLat, centerLng, 10)

    for point in points:
        myMap.addpoint(point[1], point[0], "b")

    colors = ["#ff3300", "#3333ff", "#0000", "#ff00ff", "#00e600", "#ff9900", "#66c2ff", "#ffff00"]
    colorIdx = 0

    for path in paths:
        pathPoint = getPathPoint(path.points)
        myMap.addpath(pathPoint, colors[colorIdx])
        colorIdx = (colorIdx + 1) % len(colors)


    # create map file
    mapFilename = "%s.html" % mapFilename
    myMap.draw('./' + mapFilename)

    # Open the map file on a web browser.
    url = "file://" + os.getcwd() + "/" + mapFilename
    webbrowser.open_new(url)


def getPathPoint(points):
    pathPoints = []
    for point in points:
        pathPoints.append((point[1], point[0]))
    return pathPoints


def getSegPoint(segment):
    points = []
    for point in segment.segment:
        points.append((point[1], point[0]))
    return points

def findIntersectionFromGrids(grids, unitLen, minLng, minLat, allSegments):
    intersections = {}
    for pathSeg in allSegments:
        candidatePathSeg = findCandidatePathSeg(grids, unitLen, minLng, minLat, pathSeg)
        for otherPathSeg in candidatePathSeg:
            if otherPathSeg != pathSeg:
                intersectPoint = pathSeg.findIntersectPoint(otherPathSeg)
                if intersectPoint is not None:
                    if intersectPoint in intersections:
                        intersection = intersections[intersectPoint]
                    else:
                        intersection = Intersection(intersectPoint)
                        intersections[intersectPoint] = intersection
                    intersection.segments.add(pathSeg)
                    intersection.segments.add(otherPathSeg)

    return intersections


def findCandidatePathSeg(grids, unitLen, minLng, minLat, pathSeg):
    maxRow, minRow, maxCol, minCol = getGridRange(unitLen, minLng, minLat, pathSeg)
    candidates = set()
    for row in range(minRow, maxRow + 1):
        for col in range(minCol, maxCol + 1):
            candidates.update(grids[row][col])
    return candidates


if __name__=="__main__":
    gridMethod()
    # experiment1()
