from settings import SAMPLE_NUM
from settings import STREET_VIEW_DIRECTORY
from settings import TARGET_ROAD_TYPES
from settings import SHAPE_FILE
from settings import SHAPE_TYPE_INDEX
from settings import CSV_FILENAME
from settings import INIT_PICTURE_NUM
from shapefileUtil import ShapeType
from shapefileUtil import ShapeFileParser
from csv import outputCSV
from util import *


# def sampleImage():
#     """
#     Get some sample images for each road types.
#     """
#     types = ShapeType.getAllTypes()
#     for type in types:
#         filename = "../end_points/" + type + ".data"
#         targetDirectory = "../street_views/" + type + "/"
#         makeDirectory(targetDirectory)
#         points = readPointFile(filename)
#         sampleAndDownloadStreetImage(points, 8, 1, targetDirectory)


def getValidEndPointFromFile(roadTypes):
    validEndPoints = []
    for rdType in roadTypes:
        filename = "../end_points/%s.data" % rdType
        validEndPoints += readPointFile(filename)
    return validEndPoints


def main():

    targetRoadType = ShapeType.getAllTypes()
    validEndPoints = getValidEndPointFromFile(targetRoadType)

    # make directory for street images
    makeDirectory(STREET_VIEW_DIRECTORY)

    # Sample street images, the return is list of sample info
    sampleData = sampleAndDownloadStreetImage(validEndPoints, SAMPLE_NUM, INIT_PICTURE_NUM, STREET_VIEW_DIRECTORY)
    columnTitle = ["Sample Number", "Latitude", "Longitude", "Latitude + Longitude", "Heading", "Date", "File name"]
    sampleData.insert(0, columnTitle)

    # output to csv file
    outputCSV(sampleData, CSV_FILENAME)

    # plot images map
    # plotSampledPointMap(sampledPoints, "map")


# def checkPhotoDate():
#     directory = "../end_points"
#     types = ShapeType.getAllTypes()
#     shapefile = ShapeFileParser(SHAPE_FILE, SHAPE_TYPE_INDEX)
#     shapeRecord = shapefile.getShapeRecord()
#     typePoints = {}
#     for sr in shapeRecord:
#         if sr.record
#
#
#     for sr in shapeRecord:
#         print sr.record
#         print sr.shape.points



if __name__ == "__main__":
    pass