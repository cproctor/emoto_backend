import requests
import json

NY_LAT = 40.712
NY_LONG = -74.006
SF_LAT = 37.775
SF_LONG = -122.419
CHI_LAT = 41.878
CHI_LONG = -87.630

class EmotoAPI():

    SIGNUP_URL = "{}/api/v1/users/new"
    STATUS_URL = "{}/api/v1/users/{}/status"
    MESSAGES_URL = "{}/api/v1/users/{}/messages"
    NEW_MESSAGE_URL = "{}/api/v1/users/{}/messages/new"
    SET_LOCATION_URL = "{}/api/v1/users/{}/location"
    PAIR_URL = "{}/api/v1/users/{}/pair/{}"
    UNPAIR_URL = "{}/api/v1/users/{}/unpair"
    EMOTOS_URL = "{}/api/v1/emotos"
    NEW_EMOTO_URL = "{}/api/v1/emotos/new"
    PRESENT_URL = "{}/api/v1/users/{}/present"
    ABSENT_URL = "{}/api/v1/users/{}/absent"
    SET_CURRENT_EMOTO_URL = "{}/api/v1/users/{}/emoto"

    def __init__(self, base_url, verbose=True):
        self.base_url = base_url
        self.verbose = verbose

    def signup(self, username, latitude, longitude, raw=False):
        url = self.SIGNUP_URL.format(self.base_url)
        if self.verbose: 
            print("POST {}".format(url))
        response = requests.post(url, data=json.dumps({"username": username, "latitude": latitude, "longitude": longitude}))
        if raw:
            return response
        else:
            return response.json()

    def signup_ny(self, username, raw=False):
        response = self.signup(username, NY_LAT, NY_LONG)
        if raw:
            return response
        else:
            return response.json()

    def signup_sf(self, username):
        response =  self.signup(username, SF_LAT, SF_LONG)
        if raw:
            return response
        else:
            return response.json()

    def status(self, username, raw=False):
        url = self.STATUS_URL.format(self.base_url, username)
        if self.verbose: 
            print("GET {}".format(url))
        response = requests.get(url)
        if raw:
            return response
        else:
            return response.json()

    def messages(self, username, raw=False):
        url = self.MESSAGES_URL.format(self.base_url, username)
        if self.verbose: 
            print("GET {}".format(url))
        response = requests.get(url)
        if raw:
            return response
        else:
            return response.json()

    def new_message(self, username, message, raw=False):
        url = self.NEW_MESSAGE_URL.format(self.base_url, username)
        if self.verbose: 
            print("POST {}".format(url))
        response = requests.post(url, data=json.dumps(message))
        return response
        if raw:
            return response
        else:
            return response.json()

    def new_message_hello(self, username, raw=False):
        response =  self.new_message(username, {"text": "Hello!"})
        if raw:
            return response
        else:
            return response.json()

    def set_location(self, username, location, raw=False):
        "Location should be of the format {'latitude': 47.3, 'longitude': -73.21}"
        url = self.SET_LOCATION_URL.format(self.base_url, username)
        if self.verbose: 
            print("POST {}".format(url))
        response = requests.post(url, data=json.dumps(location))
        if raw:
            return response
        else:
            return response.json()

    def pair(self, username, code, raw=False):
        url = self.PAIR_URL.format(self.base_url, username, code)
        if self.verbose: 
            print("POST {}".format(url))
        response = requests.post(url)
        if raw:
            return response
        else:
            return response.json()

    def unpair(self, username, raw=False):
        url = self.UNPAIR_URL.format(self.base_url, username)
        if self.verbose: 
            print("POST {}".format(url))
        response = requests.post(url)
        if raw:
            return response
        else:
            return response.json()

    def emotos(self, raw=False):
        url = self.EMOTOS_URL.format(self.base_url)
        response = requests.get(url)
        if raw:
            return response
        else:
            return response.json()

    def new_emoto(self, name, filepath, raw=False):
        url = self.NEW_EMOTO_URL.format(self.base_url)
        with open(filepath, 'rb') as imagefile:
            response = requests.post(
                url, 
                data={"name": name},
                files={"image": imagefile}
            )
        if raw:
            return response
        else:
            return response.json()

    def present(self, username, raw=False):
        url = self.PRESENT_URL.format(self.base_url, username)
        response = requests.post(url)
        if raw:
            return response
        else:
            return response.json()

    def absent(self, username, raw=False):
        url = self.ABSENT_URL.format(self.base_url, username)
        response = requests.post(url)
        if raw:
            return response
        else:
            return response.json()
        
    def set_current_emoto(self, username, emoto_name, raw=False):
        url = self.SET_CURRENT_EMOTO_URL.format(self.base_url, username)
        response = requests.post(url, data=json.dumps({"name": emoto_name}))
        if raw:
            return response
        else:
            return response.json()
        
        

