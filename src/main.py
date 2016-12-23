import sys
import random
from settings import SAMPLE_NUM
from settings import STREET_VIEW_DIRECTORY
from settings import CSV_FILENAME
from settings import INIT_PICTURE_NUM
from config import HEADINGS
from shapefileUtil import ShapeType
from csv import outputCSV
from util import readPointFile
from util import makeDirectory
from util import Progress
from googleStreetView import GoogleStreetView

def getValidEndPointFromFile(roadTypes):
    validEndPoints = []
    for rdType in roadTypes:
        filename = "../end_points/%s.data" % rdType
        validEndPoints += readPointFile(filename)
    return validEndPoints


def sampleAndDownloadStreetImage(endPoints, sampleNum, picNum, targetDirectory):
    """
    Randomly select end points from the endPoint collection.
    For each selected end point, call Google map street view image api
    to get the street view images.
    :return:
    """
    print "download street images..."
    sampledPoints = random.sample(endPoints, sampleNum) if sampleNum < len(endPoints) else endPoints
    sampleData = []  # store (picture number, file name, lat and lng)
    progress = Progress(10)
    numStep = len(HEADINGS)
    for point in sampledPoints:
        progress.printProgress()
        result = downloadSurroundingStreetView(point, targetDirectory, picNum)
        sampleData += result
        picNum += numStep
    print ""
    return sampleData


def downloadSurroundingStreetView(point, directory, picNum):
    """
    Call Google street view image api to get the four surrounding images at the
    given point.
    :param point: (float, float) longitude and latitude
    :param directory: the directory for saving the images
    """
    # googleMapAddr = "https://www.google.com/maps/@%s,%s,15z"
    result = []
    for heading in HEADINGS:
        filename = "%s/%010d_%s_%s_%s.jpg" % (directory, picNum, str(point[1]), str(point[0]), heading[0])
        paramDict = GoogleStreetView.makeParameterDict(point[1], point[0], heading[1])
        metadata = GoogleStreetView.getMetadata(paramDict)
        try:
            result.append([picNum,
                           str(point[1]),
                           str(point[0]),
                           str(point[1]) + "," + str(point[0]),
                           heading[0],
                           metadata["date"],
                           filename.split("/")[-1]]
                          )
        except:
            print sys.exc_traceback
            print metadata
        param = GoogleStreetView.makeParameter(point[1], point[0], heading[1])
        GoogleStreetView.downloadStreetView(param, filename)
        picNum += 1
    return result


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


if __name__ == "__main__":
    pass