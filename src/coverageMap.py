from util import plotSampledPointMap


def readPointAndType(filename):
    f = open(filename, 'r')
    typePoints = {}
    for line in f.readlines():
        data = line.strip("\n").split("|")
        for type in data[1:]:
            if type not in typePoints:
                typePoints[type] = set()
            typePoints[type].add(data[0])
    f.close()
    return typePoints


def readDatePoints(filename):
    f = open(filename, 'r')
    yearPoints = {}
    for line in f.readlines():
        point, info = line.strip("\n").split("==")
        year = getDate(info)[0]
        if year not in yearPoints:
            yearPoints[year] = set()
        yearPoints[year].add(point)
    f.close()
    return yearPoints


def getDate(info):
    yearMonth = info.split("|")[1].split(":")[1].split("-")
    return tuple([d for d in yearMonth])


def convertPoints(pointStrs):
    points = []
    for pointStr in pointStrs:
        point = pointStr.split(",")
        points.append((float(point[0]), float(point[1])))
    return points

if __name__ == "__main__":

    # get point date
    yearPoints = readDatePoints("../point_info.data")

    total = 0
    for year in yearPoints:
        points = convertPoints(yearPoints[year])
        plotSampledPointMap(points, year)
        print year, len(yearPoints[year])
        total += len(yearPoints[year])
    print "total=", total


