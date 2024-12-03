class OptimizerAPIException(Exception):
    """
    Any error raised while talking to the Optimizer API.
    """
    def __init__(self, message=None):  
        self.message = message  


class OptimizerAPIClientException(OptimizerAPIException):
    """
    Any error raised while talking to the Optimizer API due to request issue.
    """
    pass


class OptimizerAPIServerException(OptimizerAPIException):
    """
    Any error raised while talking to the Optimizer API due to server side issue.
    """
    def __init__(self, message=None):  
        self.message = message  


class ClientServerException(Exception):
    """
    Any error raised while talking to the Client's server
    """
    pass


class OptimizerObjectDoesNotExistsException(Exception):
    """
    If the object does not exist.
    """
    def __init__(self, message=None):
        self.message = message