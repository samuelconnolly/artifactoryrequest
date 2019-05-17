aql.py
======

[\#](#section-0)

    from collections import OrderedDict
    import requests
    ''' AQL Generators '''

[\#](#section-1)

    def and_item(value):
        ''' 
        Return $AND item with values inserted 
        AND is the default behaviour for unmarked AQL statements.
        Ex: 
        items.find( name = example AND [<criteria>])
        value argument is typically an array but if comparing to one object
        can be inserted as single dict
        '''
        return {"$and":value}

[\#](#section-2)

    def or_item(value):
        ''' 
        Return $OR item with values inserted 
        Ex: 
        items.find( name = example OR [{$AND{<criteria>}}])
        value argument is typically an array but if comparing to one object
        can be inserted as single dict
        '''
        return {"$or":value}

[\#](#section-3)

    def equal(value):
        ''' 
        Conditional argument, check if equal to value
        '''
        return {"$eq":value}

[\#](#section-4)

    def notequal(value):
        ''' 
        Conditional argument, check if not equal to value
        '''
        return {"$neq":value}

[\#](#section-5)

    def gt(value):
        ''' 
        Conditional argument, check if greater than value
        '''
        return {"$gt":value}

[\#](#section-6)

    def lt(value):
        ''' 
        Conditional argument, check if less than value
        '''
        return {"$lt":value}

[\#](#section-7)

    def lte(value):
        ''' 
        Conditional argument, check if less than or equal to value
        '''
        return {"$lte":value}

[\#](#section-8)

    def match(value):
        '''
        Check for match of name, can be wildcard or partial wildcard
        '''
        return {"$match":value}

[\#](#section-9)

    def nmatch(value):
        return {"$nmatch":value}

[\#](#section-10)

    def get_artifact_build(name, num):
        '''
        Return array looking for specific artifact build name and number
        '''
        return [{"artifact.module.build.name": name}, {"artifact.module.build.number": num}]

[\#](#section-11)

    class aql(object):

[\#](#section-12)

        def __init__(self, domain, query, artireq):
            '''
            Init AQL object
            Domain - builds, items, entries
            query - JSON query to be submitted to server
            artireq - ArtifactoryRequest object used to grab URL and Access key
            response - response['results'] from send() function, JSON object.
            '''
            self.domain = domain
            self.query = self.form_query(query)
            self.artireq = artireq
            self.response = self.send()

[\#](#section-13)

        def form_query(self, query):
            ''' 
            Form query based around domain specified in AQL init
            Query object should be valid JSON, which is then wrapped into a payload
            '''
            if self.domain == "items":
                formatted = "{}{}{}".format("items.find(", query, ")").replace("'", "\"")
            else:
                pass
            return formatted

[\#](#section-14)

        def send(self):
            '''
            Send payload to AQL endpoint
            Requires Auth key to use Artifactory endpoint
            '''
            url = "{}/api/search/aql".format(self.artireq.server_url)
            return requests.post(url, 
                                 headers={'Authorization': 'Bearer {}'.format(self.artireq.apikey)},
                                 data=self.query)

