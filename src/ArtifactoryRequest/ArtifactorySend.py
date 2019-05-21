import requests
from requests.auth import HTTPBasicAuth
import json
try:
    from ArtiAuth import ArtiAuth
except:
    from ArtifactoryRequest.ArtiAuth import ArtiAuth

class ArtifactorySend(object):
    def __init__(self, query, artireq, payload=None, json=True):
        self.query = query
        self.artireq = artireq
        self.status_code = None 
        self.response = None
        self.payload = payload
        self.json = json
        self.auth = ArtiAuth(self.artireq).auth_obj
        if self.json:
            self.headers = {'Content-type': 'application/json'}
        else:
            self.headers = {}

    
    def validate_response(self, status):
        try:
            if status != 200:
                print(status)
                if status == 401:
                    raise ArtiAuth.ArtifactoryUnauthorizedException
                if status == 415:
                    print("Unsupported Media Type")
        except ArtiAuth.ArtifactoryUnauthorizedException:
            print("AUTH ERROR: Invalid credentials")
            exit(-1)

    def get(self):
        if isinstance(self.auth, dict):
            self.response = requests.get(self.query, headers=self.auth)
        elif isinstance(self.auth, HTTPBasicAuth):
            self.response = requests.get(self.query, auth=self.auth)
        self.validate_response(self.response.status_code)

    def post(self):
        if self.json:
            self.payload = json.dumps(self.payload)
        if isinstance(self.auth, dict):
            self.headers.update(self.auth)
            self.response = requests.post(self.query,
                                          headers=self.headers,
                                          data=self.payload)
        elif isinstance(self.auth, HTTPBasicAuth):
            if self.headers != {}:
                self.response = requests.post(self.query,
                                headers=self.headers,
                                auth=self.auth,
                                data=self.payload)
            else:
                self.response = requests.post(self.query,
                                              auth=self.auth,
                                              data=self.payload)
            print(self.response.text)
        self.validate_response(self.response.status_code)



