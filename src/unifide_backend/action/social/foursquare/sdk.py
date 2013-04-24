#===============================================================================
# Extended Foursquare SDK to interface with 4SQ Venue API
#===============================================================================

__author__ = 'kianwei'

import urllib
import urllib2
import socket
import time

# Find a JSON parser
try:
    import simplejson as json
except ImportError:
    try:
        from django.utils import simplejson as json
    except ImportError:
        import json
_parse_json = json.loads


class FoursquareAPI(object):
    def __init__(self, access_token=None, timeout=None):
        self.access_token = access_token
        self.timeout = timeout

    def request(self, path, args=None, post_args=None):
        args = args or {}

        if self.access_token:
            if post_args is not None:
                post_args["oauth_token"] = self.access_token
                post_args["v"] = time.strftime("%Y%m%d")
            else:
                args["oauth_token"] = self.access_token
                args["v"] = time.strftime("%Y%m%d")
        post_data = None if post_args is None else urllib.urlencode(post_args)
        try:
            file = urllib2.urlopen("https://api.foursquare.com/v2/" + path + "?" +
                                   urllib.urlencode(args),
                                   post_data, timeout=self.timeout)
        except urllib2.HTTPError, e:
            response = _parse_json(e.read())
            raise FoursquareAPIError(response)
        except TypeError:
            # Timeout support for Python <2.6
            if self.timeout:
                socket.setdefaulttimeout(self.timeout)
            file = urllib2.urlopen("https://api.foursquare.com/v2/" + path + "?" +
                                   urllib.urlencode(args), post_data)
        try:
            response = _parse_json(file.read())
        finally:
            file.close()
        if response and isinstance(response, dict) and response.get("error"):
            raise FoursquareAPIError(response["error"]["type"],
                                response["error"]["message"])
        return response


class FoursquareAPIError(Exception):
    def __init__(self, result):
        #Exception.__init__(self, message)
        #self.type = type
        self.result = result
        try:
            self.type = result["error_code"]
        except:
            self.type = ""

        # OAuth 2.0 Draft 10
        try:
            self.message = result["error_description"]
        except:
            # OAuth 2.0 Draft 00
            try:
                self.message = result["error"]["message"]
            except:
                # REST server style
                try:
                    self.message = result["error_msg"]
                except:
                    self.message = result

        Exception.__init__(self, self.message)