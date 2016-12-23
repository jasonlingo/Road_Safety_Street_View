from __future__ import division

import math
import pygmaps
from config import HEADINGS
from shapefileUtil import ShapeFileParser
from shapefileUtil import ShapeType
from googleStreetView import GoogleStreetView
from util import getMapCenter
from pathSegment import Intersection
from pathSegment import PathSegment
from pathSegment import getSegmentPoint
from pathSegment import getMinMaxLatLng
from drawShapefile import createMapHtmlandOpen



COLORS = ["#ff3300", "#3333ff", "#0000", "#ff00ff", "#00e600", "#ff9900", "#66c2ff", "#ffff00"]


def findIntersectionByGrid(shp, types, regionNum):
    """
    Divide the map into grids and register each segment to the grids that it expands.
    Find the intersections by checking each segment with nearby segments.
    :param shp: ShapefileParser
    :param types: list of type
    :param regionNum: the number of grids on the shorter edge of the map
    """
    allPaths = shp.getPathWithType(types)
    allSegments = getSegmentsFromPath(allPaths)

    maxLng, minLng, maxLat, minLat = getMinMaxLatLng(allPaths)
    grids, unitLen = genGrids(maxLng, minLng, maxLat, minLat, regionNum)
    insertSegments(grids, unitLen, minLng, minLat, allSegments)

    print "all segments: %d" % len(allSegments)

    intersections = findIntersectionFromGrids(grids, unitLen, minLng, minLat, allSegments)
    print "intersections: %d" % len(intersections)

    # validPoints = []
    # for point in intersections.keys():
    #     param = GoogleStreetView.makeParameterDict(point[1], point[0], HEADINGS[0])
    #     if GoogleStreetView.isValidPoint(param):
    #         validPoints.append(point)
    #
    # print "total points: %d" % len(validPoints)

    plotPointAndSegment(intersections.keys(), allSegments, "grid_segment_noCheck_motorway")


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


def plotPointAndSegment(points, segments, mapFilename):
    centerLat, centerLng = getMapCenter(points)
    myMap = pygmaps.maps(centerLat, centerLng, 10)

    for point in points:
        myMap.addpoint(point[1], point[0], "b")

    colorIdx = 0
    for seg in segments:
        pathPoint = getSegmentPoint(seg)
        myMap.addpath(pathPoint, COLORS[colorIdx])
        colorIdx = (colorIdx + 1) % len(COLORS)

    createMapHtmlandOpen(myMap, mapFilename)


def plotPointAndPath(points, paths, mapFilename):
    centerLat, centerLng = getMapCenter(points)
    myMap = pygmaps.maps(centerLat, centerLng, 10)

    for point in points:
        myMap.addpoint(point[1], point[0], "b")

    colorIdx = 0

    for path in paths:
        pathPoint = getPathPoint(path.points)
        myMap.addpath(pathPoint, COLORS[colorIdx])
        colorIdx = (colorIdx + 1) % len(COLORS)

    createMapHtmlandOpen(myMap, mapFilename)


def getPathPoint(points):
    pathPoints = []
    for point in points:
        pathPoints.append((point[1], point[0]))
    return pathPoints


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
    filename = "../shapefile/Bangkok-shp/shape/roads.shp"
    shp = ShapeFileParser(filename)

    types = []
    types.append(ShapeType.MOTORWAY)

    regionNum = 1000

    findIntersectionByGrid(shp, types, regionNum)
