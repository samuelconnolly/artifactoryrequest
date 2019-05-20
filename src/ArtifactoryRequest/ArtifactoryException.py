class ArtifactoryException(BaseException):
    ''' 
    Assume requests object has been passed and
    handle incorrect statuses
    '''
    pass

class ArtifactoryUnauthorizedException(ArtifactoryException):
    pass