from Shapefile import ShapeFileParser
from Shapefile import ShapeType
from Settings import SHAPE_FILE
from Settings import SHAPE_TYPE_INDEX
from main import getEndPoint
from main import getValidEndPoint
from main import removeDuplicatePoint


def preprocessEndPoints(types):
    """
    Parse the shape file, get the target road types data and store the valid end points to files.
    :param types: list of road types
    """
    for type in types:
        print "======================="
        print "processing", type
        shapefile = ShapeFileParser(SHAPE_FILE, SHAPE_TYPE_INDEX)

        print "parsing shape file"
        paths = shapefile.getShapeTypePath([type])

        endPoints = getEndPoint(paths)
        endPoints = removeDuplicatePoint(endPoints)
        print "end points: %d" % len(endPoints)

        print "getting valid points"
        endPoints = getValidEndPoint(endPoints[100000:])
        print "valid points: %d" % len(endPoints)

        # output to file
        lines = []
        for point in endPoints:
            lines.append("%s, %s\n" % (str(point[0]), str(point[1])) )

        file = open("../end_points/" + type + ".data", "a")
        file.writelines(lines)
        file.close()


# if __name__ == "__main__":
#     types = []
#     types.append(ShapeType.RESIDENTIAL)
#     preprocessEndPoints(types)
