import os


cwd = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
SQL_URI = 'mongodb://kianwei:thisisnotsecureatall@localhost/unifide-backend'
LOG_FILE = os.path.join(cwd, "log.txt")

#facebook app info


#twitter app info


#foursquare app info


# API Packages to be enabled
API_TO_REGISTER = (
    "facebook",
#    "friends",
)