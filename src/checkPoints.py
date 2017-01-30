import random
import sys
from googleStreetView import GoogleStreetView
from config import HEADINGS

def readPoints(filename):
    points = []
    inputData = open(filename, 'r')
    for line in inputData.readlines():
        data = line.strip().split("|")
        points.append(data[0])
    inputData.close()
    return points


def getPointInfoToFile(points, filename):
    lines = []
    line = "%s==Actual Location:%s,%s|date:%s"

    counter = {}
    counter["no date"] = 0

    prog = 0
    for point in points:
        lngLat = [float(p) for p in point.split(",")]
        param = GoogleStreetView.makeParameterDict(lngLat[1], lngLat[0], HEADINGS[0])
        info = GoogleStreetView.getMetadata(param)
        if info["status"] == GoogleStreetView.OK:
            if 'date' in info:
                data = line % (point, info['location']['lng'], info['location']['lat'], info['date'])
            else:
                counter['no date'] += 1
                data = line % (point, info['location']['lng'], info['location']['lat'], "0000-00")
            lines.append(data)
        else:
            print "Point err:", point

        prog += 1
        if prog % 10 == 0:
            sys.stdout.write("\r%d" % prog)

    print "\nnumber of points that have no date: %d" % counter['no date']

    lines = "\n".join(lines)
    lines += "\n"
    output = open(filename, 'a')
    output.writelines(lines)
    output.close()


def getYearMonth(filename):
    f = open(filename, 'r')
    data = [line.strip("\n").split("==") for line in f.readlines()]
    yearMonth = [getYearMonthTuple(d) for d in data]
    f.close()
    return yearMonth


def getYearMonthTuple(date):
    ym = date[1].split("|")[1].split(":")[1].split("-")
    return int(ym[0]), int(ym[1])


def findYearMonthDist(yearMonth):
    counter = {}
    for ym in yearMonth:
        if ym not in counter:
            counter[ym] = 1
        else:
            counter[ym] += 1
    printDictByKeyOrder(counter)


def printDictByKeyOrder(counter):
    keys = counter.keys()
    keys.sort()
    for key in keys:
        print key, counter[key]


def findMaxMinYearMonth(yearMonth):
    ym = list(set(yearMonth))
    ym.sort()
    print "Min:", ym[0]
    print "max:", ym[-1]


def getPointInfo():
    inputFilename = "../validIntersectionPoints_nonduplicate.data"
    points = readPoints(inputFilename)

    outputFilename = "../point_info.data"
    start = 150000
    delta = 5000
    print "start=%d, delta=%d" % (start, delta)
    getPointInfoToFile(points[start:start + delta], outputFilename)


def readTargetPoints(filename):
    f = open(filename, 'r')
    points = [p.split("==")[0] for p in f.readlines()]
    return points


def check():
    # check what data is processed
    inputFilename = "../validIntersectionPoints_nonduplicate.data"
    orgPoints = set(readPoints(inputFilename)[:10])
    targetPoints = set(readTargetPoints("../point_info.data"))

    i = 0
    for p in targetPoints:
        if p not in orgPoints:
            print p
            i += 1
    print "total diff = %d" % i


if __name__ == "__main__":
    getPointInfo()
