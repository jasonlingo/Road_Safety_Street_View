import random
from settings import SAMPLE_NUM
from settings import STREET_VIEW_DIRECTORY
from settings import CSV_FILENAME
from settings import INIT_PICTURE_NUM
from config import HEADINGS
from csv_utils import outputCSV
from util import readPointFile
from util import makeDirectory
from util import Progress
from util import plotSampledPointMap
from googleStreetView import GoogleStreetView
from googleDrive import GDriveUpload

def getValidEndPointFromFile(roadTypes):
    validEndPoints = []
    for rdType in roadTypes:
        filename = "../end_points/%s.data" % rdType
        validEndPoints += readPointFile(filename)
    return validEndPoints


def sampleAndDownloadStreetImage(endPoints, sampleNum, picNum, ptrNum, targetDirectory, intersectionPointInfo):
    """
    Randomly select end points from the endPoint collection.
    For each selected end point, call Google map street view image api
    to get the street view images.
    :return:
    """
    print "downloading street images..."
    sampledPoints = random.sample(endPoints, sampleNum) if sampleNum < len(endPoints) else endPoints
    sampleData = []  # store (picture number, file name, lat and lng)
    progress = Progress(10)
    sampleNumDelta = len(HEADINGS)
    for point in sampledPoints:
        progress.printProgress()

        result = downloadSurroundingStreetView(point, targetDirectory, picNum, ptrNum, intersectionPointInfo)
        sampleData += result
        picNum += sampleNumDelta
        ptrNum += 1
    print ""
    return sampleData


def downloadSurroundingStreetView(point, directory, picNum, ptrNum, intersectionPointInfo):
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

        result.append([picNum,
                       ptrNum,
                       str(point[1]) + "," + str(point[0]),
                       heading[0],
                       metadata["date"],
                       filename.split("/")[-1],
                       ",".join(intersectionPointInfo[(point[0], point[1])])]
                      )

        param = GoogleStreetView.makeParameter(point[1], point[0], heading[1])
        GoogleStreetView.downloadStreetView(param, filename)
        picNum += 1
    return result


def readPointFile(filename):
    # 100.619244706,13.8110460033==Actual Location:100.61920895,13.8114677028|date:2015-12

    pointInfo = {}
    f = open(filename, 'r')
    for data in f.readlines():
        point, info = data.split("==")
        lng, lat = [float(p) for p in point.split(",")]
        pointInfo[(lng, lat)] = parseInfoToDict(info)
    f.close()

    return pointInfo


def parseInfoToDict(info):
    infoDict = {}
    for data in info.strip("\n").split("|"):
        key, val = data.split(":")
        if key == "date":
            infoDict[key] = [int(d) for d in val.split("-")]
        else:
            infoDict[key] = val
    return infoDict


def readIntersectionPointInfo(filename):
    intersectionPointInfo = {}
    f = open(filename, 'r')
    for data in f.readlines():
        data = data.strip("\n").split("|")
        key = convertKey(data[0])
        val = data[1:]
        intersectionPointInfo[key] = val
    return intersectionPointInfo


def convertKey(lngLat):
    lng, lat = [float(p) for p in lngLat.split(",")]
    return (lng, lat)


def filterPointByYear(pointInfo, maxYear, minYear):
    points = []
    for point in pointInfo:
        if minYear <= pointInfo[point]["date"][0] <= maxYear:
            points.append(point)
    return points


def divideGPS(point):
    lat, lng = point.split(",")
    return (float(lng), float(lat))


def sampling():
    intersectionPointFile = "../validIntersectionPoints_nonduplicate.data"
    pointInfoFile = "../point_info.data"

    pointInfo = readPointFile(pointInfoFile)
    intersectionPointInfo = readIntersectionPointInfo(intersectionPointFile)

    maxYear = 2012
    minYear = 2011
    filteredPoints = filterPointByYear(pointInfo, maxYear, minYear)

    # make directory for street images
    makeDirectory(STREET_VIEW_DIRECTORY)

    IMG_NAME_COL_NUM = 5
    LAT_LNG_COL_NUM = 2

    # Sample street images, the return is list of sample info
    sampleData = sampleAndDownloadStreetImage(filteredPoints, SAMPLE_NUM, INIT_PICTURE_NUM, INIT_PICTURE_NUM, STREET_VIEW_DIRECTORY, intersectionPointInfo)
    imageNames = [STREET_VIEW_DIRECTORY + "/" + data[IMG_NAME_COL_NUM] for data in sampleData]
    links = GDriveUpload(imageNames, "Sampled_Image")

    for i in xrange(len(sampleData)):
        imageName = STREET_VIEW_DIRECTORY + "/" + sampleData[i][IMG_NAME_COL_NUM]
        sampleData[i].append(links[imageName])

    columnTitle = ["Sample Number", "Sampled Point Number", "Latitude + Longitude", "Heading", "Date", "Image Name", "Road Types", "Web Link"]
    sampleData.insert(0, columnTitle)

    # output to csv file
    outputCSV(sampleData, CSV_FILENAME)

    # plot images map
    sampledPoints = set([divideGPS(d[LAT_LNG_COL_NUM]) for d in sampleData[1:]])
    plotSampledPointMap(list(sampledPoints), STREET_VIEW_DIRECTORY + "/map")


if __name__ == "__main__":
    sampling()

