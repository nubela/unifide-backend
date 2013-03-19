import os


cwd = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
MONGO_URI = 'mongodb://kianwei:thisisnotsecureatall@localhost/unifide-backend'
MONGO_DB = 'unifide-backend'
LOG_FILE = os.path.join(cwd, "log.txt")

#facebook app info
FB_APP_ID = "336489173138188"
FB_APP_SECRET = "b259ee37fdb0acb61feb1b1af0fdab57"
FB_REDIRECT_URI = "http://127.0.0.1"

#twitter app info


#foursquare app info


# API Packages to be enabled
API_TO_REGISTER = (
    "social_connect",
#    "friends",
)

#facebook test user
FB_TEST_USER = ""
FB_TEST_PASSWORD = ""