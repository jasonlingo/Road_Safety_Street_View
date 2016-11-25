from Shapefile import ShapeType

# ===== Google API ==================================================
GOOGLE_API_KEY = "AIzaSyCMU-JFJ4epxPSNuhUPShc7ZCEaKSxY4C0"
"""Google Maps api key"""

NO_IMAGE_FILE_NAME = "../img/NO_IMAGE.jpg"
"""The image replied by Google Street View API when there is no image for the request."""


# ===== Shape file ==================================================
SHAPE_FILE = "../shapefile/Bangkok-shp/shape/roads.shp"
SHAPE_TYPE_INDEX = 3
# SHAPE_FILE = "../shapefile/bangkok_thailand.imposm-shapefiles/bangkok_thailand_osm_roads.shp"
# SHAPE_TYPE_INDEX = 2


# ===== Directories =================================================
STREET_VIEW_DIRECTORY = "../street_views"


# ===== Settings ====================================================
SAMPLE_NUM = 10
"""total number of samples"""

TARGET_ROAD_TYPES = []
TARGET_ROAD_TYPES.append(ShapeType.CYCLEWAY)


