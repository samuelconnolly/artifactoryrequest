from requests.auth import HTTPBasicAuth
try:
    from ArtifactoryException import ArtifactoryException
except:
    from ArtifactoryRequest.ArtifactoryException import ArtifactoryException

class ArtiAuth(object):

    class ArtifactoryUnauthorizedException(ArtifactoryException):
        pass

    def __init__(self, artireq):
        try:
            self.auth_obj = None
            if artireq.token:
                self.auth_obj = self.get_token_headers(artireq.token)
            elif artireq.user and artireq.api_key:
                self.auth_obj = self.get_http_auth(artireq.user, 
                                                artireq.api_key)
            else:
                raise self.ArtifactoryUnauthorizedException
        except self.ArtifactoryUnauthorizedException:
            print("No credentials provided")
            exit(-1)

    def get_token_headers(self, token):
        return {'Authorization': 'Bearer {}'.format(token)}

    def get_http_auth(self, user, api_key):
        return HTTPBasicAuth(user, api_key)