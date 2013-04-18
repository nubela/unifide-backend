import os


cwd = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
MONGO_URI = 'mongodb://kianwei:thisisnotsecureatall@localhost/unifide-backend'
MONGO_DB = 'unifide-backend'
LOG_FILE = os.path.join(cwd, "log.txt")

#facebook app info
FB_APP_ID = "336489173138188"
FB_APP_SECRET = "b259ee37fdb0acb61feb1b1af0fdab57"
FB_REDIRECT_URI = "http://127.0.0.1:5000/"
FB_PERMS = ["manage_pages", "publish_stream"]
FB_REALTIME_TOKEN = "thisisnotsecureatall1987"

#twitter app info
TW_CONSUMER_KEY = "dB4v3wKk52LIRz6SRSZTJQ"
TW_CONSUMER_SECRET = "IkfpGDZteinlSBY3iNKwrtuEarB6sZA8U6rbZXJ7h4U"
TW_REDIRECT_URI = "http://127.0.0.1:5000/"
ADD_USER_MAX_TWEET = 800

#foursquare app info
FSQ_CLIENT_ID = "DMJY0SMIR5050PMBOL2JKLQWO2R4NCMILNSHMM5VBDJH2AQH"
FSQ_CLIENT_SECRET = "0EYFVQNM2KTF4V11BS2PZKOPWV2DOBUG1GUHV3D5HOH0SPQO"
FSQ_REDIRECT_URI = "http://127.0.0.1:5000/"

# API Packages to be enabled
API_TO_REGISTER = (
    "social_connect",
    "account",
    "campaign"
)

#facebook test user
FB_TEST_USER = ""
FB_TEST_PASSWORD = ""