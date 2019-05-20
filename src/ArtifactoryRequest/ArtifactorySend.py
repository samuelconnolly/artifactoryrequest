import requests
from requests.auth import HTTPBasicAuth
try:
    from ArtiAuth import ArtiAuth
except:
    from ArtifactoryRequest.ArtiAuth import ArtiAuth

class ArtifactorySend(object):
    def __init__(self, query, artireq, payload=None):
        self.query = query
        self.artireq = artireq
        self.status_code = None 
        self.response = None
        self.payload = payload
        self.auth = ArtiAuth(self.artireq).auth_obj
    
    def validate_response(self, status):
        try:
            if status != 200:
                if status == 401:
                    raise ArtiAuth.ArtifactoryUnauthorizedException
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
        if isinstance(self.auth, dict):
            self.response = requests.post(self.query,
                                          headers=self.auth,
                                          data=self.payload)
        elif isinstance(self.auth, HTTPBasicAuth):
            self.response = requests.post(self.query,
                                          auth=self.auth,
                                          data=self.payload)
        self.validate_response(self.response.status_code)



