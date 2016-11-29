from Settings import SHAPE_FILE
from Settings import SAMPLE_NUM
from Settings import STREET_VIEW_DIRECTORY
from Settings import SHAPE_TYPE_INDEX
from Settings import TARGET_ROAD_TYPES
from Settings import CSV_FILENAME
from Settings import INIT_PICTURE_NUM
from Shapefile import ShapeFileParser
from CSV import outputCSV
from util import *


def sampleImage():
    """
    Get some sample images for each road types.
    """
    types = ShapeType.getAllTypes()
    for type in types:
        filename = "../end_points/" + type + ".data"
        targetDirectory = "../street_views/" + type + "/"
        makeDirectory(targetDirectory)
        points = readPointFile(filename)
        sampleAndDownloadStreetImage(points, 8, 1, targetDirectory)


def main():
    # parse shape file and add the desired shape types
    shapefile = ShapeFileParser(SHAPE_FILE, SHAPE_TYPE_INDEX)

    # retrieve end points of the shape types
    print "parse shapefile..."
    paths = shapefile.getShapeTypePath(TARGET_ROAD_TYPES)

    endPoints = getEndPoint(paths)
    print "endPoints: %d" % len(endPoints)
    # endPoints = getValidEndPoint(endPoints)
    print "valid endPoints: %d" % len(endPoints)

    # make directory for street images
    makeDirectory(STREET_VIEW_DIRECTORY)

    # Sample street images, the return is list of sample info
    sampleData = sampleAndDownloadStreetImage(endPoints, SAMPLE_NUM, INIT_PICTURE_NUM, STREET_VIEW_DIRECTORY)
    # columnTitle = ["Sample Number", "Latitude", "Longitude", "Latitude + Longitude", "Heading", "File name"]
    # sampleData.insert(0, columnTitle)

    # output to csv file
    outputCSV(sampleData, CSV_FILENAME)

    # plot images map
    # plotSampledPointMap(sampledPoints, "map")
