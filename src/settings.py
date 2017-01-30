
# ===== Google API ==================================================
GOOGLE_API_KEY = "AIzaSyDBni3ing7ysqOkGN-E_c82SdDDvtpVdXg"
"""Google Maps api key"""

NO_IMAGE_FILE_NAME = "../img/NO_IMAGE.jpg"
"""The image replied by Google Street View API when there is no image for the request."""

CLIENT_ID = "1078817381252-4tpe82e7k8r18sucmc9jq5d63pvqi1i6.apps.googleusercontent.com"

CLIENT_SECRET_FILE = "../client_secret.json"

# ===== Shape file ==================================================
SHAPE_FILE = "../shapefile/Bangkok-shp/shape/roads.dbf"
SHAPE_TYPE_INDEX = 3
# SHAPE_FILE = "../shapefile/bangkok_thailand.imposm-shapefiles/bangkok_thailand_osm_roads.shp"
# SHAPE_TYPE_INDEX = 2

# ===== Directories =================================================
STREET_VIEW_DIRECTORY = "../street_views"

# ===== File names ==================================================
CSV_FILENAME = STREET_VIEW_DIRECTORY + "/samples.csv"

# ===== Settings ====================================================
SAMPLE_NUM = 1500
"""total number of samples"""

INIT_PICTURE_NUM = 1
"""Initial picture number"""

PATH_DEGREE = 30
"""The limitation on the angle of two segments to prevent intersection points from the same path"""


