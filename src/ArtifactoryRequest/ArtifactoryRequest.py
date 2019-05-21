try:
    from aql import match, and_item, get_artifact_build
    from aql import aql
    from ArtifactorySend import ArtifactorySend
except:
    from ArtifactoryRequest.aql import match, and_item, get_artifact_build
    from ArtifactoryRequest.aql import aql
    from ArtifactoryRequest.ArtifactorySend import ArtifactorySend

import json
from requests.utils import requote_uri as encodeurl
from collections import OrderedDict
import requests

class ArtifactoryRequest(object):
    '''
    Artifactory Request library
    Generate REST API commands and AQL payloads programatically
    '''

    def validate_build_object(self):
        '''
        Retrieve build info and handle failure case
        '''
        valid = False
        self.get_build_info()
        if self.build_info['name'] == self.build_name:
            valid =  True
        return valid
    
    def get_latest_build(self, num):
        """Get last submitted build for build"""
        if num == "latest" or num == '':
            query = "{}/api/build/{}".format(self.server_url,
                                             encodeurl(self.build_name))
            request = ArtifactorySend(query, self)
            request.get()
            json_dict = json.loads(request.response.text)
            if "buildsNumbers" in json_dict:
                return json_dict["buildsNumbers"][0]['uri'].replace("/", "")
        else:
            return num

    def check_build_status(self, status="latest"):
        '''
        Check if statuses field exists return dictionary 
        containing latest status and timestampDate unless
        specific status specified
        '''
        if self.build_info:
            if status == "latest":
                return self.get_latest_status()
            else:
                return self.get_specific_status(status)
        else:
            return {}

    def get_latest_status(self):
        '''
        Iterate over statuses entry to find newest status
        '''
        latest_status = {"status": '', "timestamp": 0}
        if "statuses" in self.build_info:
            for status in self.build_info['statuses']:
                if status["timestampDate"] > latest_status["timestamp"]:
                    latest_status["timestamp"] = status["timestampDate"]
                    latest_status["status"] = status["status"]
                    latest_status["repo"] = status["repository"]
        return latest_status
    
    def get_specific_status(self, cstatus):
        if "statuses" in self.build_info:
            for status in self.build_info['statuses']:
                if status['status'] == cstatus:
                    return {"status": cstatus, "timestamp":status['timestampDate'],
                            "repo":status['repository']}
        return {}

    def send_aql_query(self, domain, query):
        aql_query = aql("items", query, self)
        json_dict = json.loads(aql_query.response.text)['results']
        self.artifacts = json_dict

    def get_artifacts(self, artifacts='*'):
        ''' 
        By default retrieve all artifacts, if artifacts is defined
        fetch items specified in artifacts field
        Ex: *.rpm will fetch all rpms, name.* will fetch all name.*
        '''
        fetch = True

        query = OrderedDict()
        query = {"name":match(artifacts)}
        query.update(and_item(get_artifact_build(self.build_name, 
                                                str(self.build_num))))
        self.send_aql_query("items", query)

        return fetch

    def get_artifact_paths(self, artifacts=None):
        '''
        Return array of artifact paths
        Input: Array defining artifacts wanted
        '''
        paths = []
        if artifacts is None:
            artifacts = []
        for arti in artifacts:
            for item in self.artifacts:
                if item['name'] == arti:
                    paths.append("{server_url}"
                                 "/{repo}/"
                                 "{path}/"
                                 "{name}".format(server_url=self.server_url,
                                                 repo=item['repo'],
                                                 path=item['path'],
                                                 name=item['name']))
        return paths


    def get_build_info(self):
        ''' 
        Retrieve JSON build info
        '''
        query = ("{}/api/build/{}/{}".format(self.server_url,
                                             encodeurl(self.build_name),
                                             self.build_num))
        request = ArtifactorySend(query, self)
        request.get()
        json_dict = json.loads(request.response.text)
        return json_dict['buildInfo']

    def promote_build(self, status, comment, target, dry_run=True):
        cstatus = self.get_latest_status()
        payload = { "status": status,
                    "comment" : comment,
                    "dryRun": dry_run,
                    "sourceRepo": cstatus["repo"],
                    "targetRepo" : target,
                    "copy": True,
                    "dependencies" : True,
                    "failFast": True}
        url = ("{}/api/build/promote/{}/{}".format(self.server_url,
                                                   encodeurl(self.build_name),
                                                   self.build_num))
        ArtifactorySend(url, self, payload=payload).post()

    def __init__(self, server_url, build_name, build_num='',
                 token=None, user=None, api_key=None):
        '''
        server_url : your Artifactory server URL
        build_name : build to be inspected
        build_num: optional, todo: fetch latest if undefined
        token : access token for API (not API key)
        user: user for API key
        api_key: ...api key
        '''
        self.server_url = server_url
        self.build_name = build_name
        self.token = token
        self.user = user
        self.api_key = api_key
        self.artifacts = {}
        self.build_num = str(self.get_latest_build(build_num))
        self.build_info = self.get_build_info()
        self.validate_build_object()
        

