from Settings import STREET_VIEW_DIRECTORY, SHAPE_FILE, SHAPE_TYPE_INDEX
from Shapefile import ShapeFileParser, ShapeType
from main import getEndPoint, plotSampledPointMap

def plotAllEndPoints():
    targetType = ShapeType.ALL
    shapeFile = ShapeFileParser(SHAPE_FILE, SHAPE_TYPE_INDEX)
    types = []
    types.append(targetType)

    paths = shapeFile.getShapeTypePath(types)
    endPoints = getEndPoint(paths)

    print "total end points=%d" % len(endPoints)
    plotSampledPointMap(endPoints, targetType)


plotAllEndPoints()