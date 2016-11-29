from Settings import STREET_VIEW_DIRECTORY, SHAPE_FILE, SHAPE_TYPE_INDEX
from Shapefile import ShapeFileParser, ShapeType
from main import getEndPoint, plotSampledPointMap
import shapefile as shp

def plotAllEndPoints():
    targetType = ShapeType.ALL
    shapeFile = ShapeFileParser(SHAPE_FILE, SHAPE_TYPE_INDEX)
    types = []
    types.append(targetType)

    paths = shapeFile.getShapeTypePath(types)
    endPoints = getEndPoint(paths)

    print "total end points=%d" % len(endPoints)
    plotSampledPointMap(endPoints, targetType)


def countTotalRecord():
    shapefileReader = shp.Reader(SHAPE_FILE)
    count = {}
    for s in shapefileReader.iterShapeRecords():
        if s.record[SHAPE_TYPE_INDEX] not in count:
            count[s.record[SHAPE_TYPE_INDEX]] = 0
        count[s.record[SHAPE_TYPE_INDEX]] += 1
    total = 0
    for key in count:
        print "%s = %d" % (key, count[key] * 2)
        total += count[key] * 2
    print "total = %d" % total


# def plotPointMap(type, filename, input):
#     input = open(input, "r")
#     points = []
#     for line in input.readlines():
#         point = line.split(",")
#         point = [float(point[0]), float(point[1].strip("\n"))]
#         points.append(point)
#     input.close()
#     plotSampledPointMap(points, type)
#
# types = ShapeType.getAllTypes()
# for type in types:
#     plotPointMap(type, "../Road_Type_maps/" + type + ".html", "../end_points/" + type + ".data")
#
