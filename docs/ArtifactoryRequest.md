ArtifactoryRequest.py
=====================

[\#](#section-0)

    from aql import match, and_item, get_artifact_build
    from aql import aql
    import json
    from urllib import quote as encodeurl
    from collections import OrderedDict
    import requests

[\#](#section-1)

    class ArtifactoryRequest(object):
        '''
        Artifactory Request library
        Generate REST API commands and AQL payloads programatically
        '''

[\#](#section-2)

        def validate_build_object(self):
            '''
            Retrieve build info and handle failure case
            '''
            response = self.get_build_info()
            if response != 200:
                return False
            if self.build_info['name'] == self.build_name:
                return True

[\#](#section-3)

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

[\#](#section-4)

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
            return latest_status

[\#](#section-5)

        def get_specific_status(self, cstatus):
            if "statuses" in self.build_info:
                for status in self.build_info['statuses']:
                    if status['status'] == cstatus:
                        return {"status": cstatus, "timestamp":status['timestampDate']}
            return {}

[\#](#section-6)

        def get_artifacts(self, artifacts='*'):
            ''' 
            By default retrieve all artifacts, if artifacts is defined
            fetch items specified in artifacts field
            Ex: *.rpm will fetch all rpms, name.* will fetch all name.*
            '''
            query = OrderedDict()
            query = {"name":match(artifacts)}
            query.update(and_item(get_artifact_build(self.build_name, 
                                                     self.build_num)))
            aql_query = aql("items", query, self)
            json_dict = json.loads(aql_query.response.text)['results']
            print(json_dict)
            return json_dict

[\#](#section-7)

        def get_build_info(self):
            ''' 
            Retrieve JSON build info
            '''
            response = requests.get("{}/api/build/{}/{}".format(self.server_url,
                                                            encodeurl(self.build_name),
                                                            self.build_num))
            json_dict = json.loads(response.text)
            return json_dict['buildInfo']

[\#](#section-8)

        def __init__(self, server_url, build_name, apikey, user, build_num=''):
            '''
            Init object with server_url and build object to be addressed
            If build num undefined fetch latest build
            Validate that build object exists before we get too far
            '''
            self.server_url = server_url

[\#](#section-9)

assert self.is\_artifactory()

            self.build_name = build_name
            self.build_num = build_num
            self.validate_build_object()
            self.apikey = apikey
            self.user = user
            self.build_info = self.get_build_info()

