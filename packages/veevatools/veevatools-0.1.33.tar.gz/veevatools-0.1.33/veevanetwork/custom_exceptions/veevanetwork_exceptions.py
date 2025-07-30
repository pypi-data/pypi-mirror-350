class NetworkAPIHeaderValueNotFound(Exception):
    """Exception raised when the required values are not provided to the
    Vn.api_call() method.

    Expecting to find a api['request']['header'][key]['value'] attribute in the json/dict provided, 
    where 'key' represents Authorization or Content Type header.
    """

    def __init__(self, message="The defined API does not contain a value parameter in its header.\
Expecting to find a api['request']['header'][key]['value'] attribute in the json/dict provided, \
where 'key' represents Authorization or Content Type header."):
        self.message = message
        super().__init__(self.message)

class NetworkAPIRequestMethodNotFound(Exception):
    """Exception raised when the required values are not provided to the
    Vn.api_call() method.

    Required Values:
        Expecting to find a api['request']['method'] attribute in the json/dict provided.
    """

    def __init__(self, message="The defined API does not contain a method parameter in its request method.\
Expecting to find a api['request']['method'] attribute in the json/dict provided."):
        self.message = message
        super().__init__(self.message)

class NetworkAPIRequestURLNotFound(Exception):
    """Exception raised when the required values are not provided to the
    Vn.api_call() method.

    Required Values:
        Expecting to find a api['request']['url']['raw'] attribute in the json/dict provided.
    """

    def __init__(self, message="The defined API does not contain a method parameter in its request method.\
Expecting to find a api['request']['url']['raw'] attribute in the json/dict provided."):
        self.message = message
        super().__init__(self.message)

class NetworkAPIRequestBodyNotFound(Exception):
    """Exception raised when the required values are not provided to the
    Vn.api_call() method.

    Required Values:
        The parameter body: dict is required in this API call, please refer to the Network API documentation for the syntax of the body parameter or set the if_example parameter to True for an example.
    """

    def __init__(self, message="The parameter body: dict is is required in this API call, please refer to the Network API documentation for the syntax of the body parameter or set the if_example parameter to True for an example."):
        self.message = message
        super().__init__(self.message)

class NetworkAPIRequestVariableNotFound(Exception):
    """Exception raised when the required values are not provided to the
    Vn.api_call() method.

    Required Values:
        The parameter variables: dict is required in this API call, please refer to the Network API documentation for the syntax of the body parameter or set the if_example parameter to True for an example.
    """

    def __init__(self, message="The parameter variables: dict is required in this API call, please refer to the Network API documentation for the syntax of the body parameter or set the if_example parameter to True for an example."):
        self.message = message
        super().__init__(self.message)

class NetworkAPIRequestQueryNotFound(Exception):
    """Exception raised when the required values are not provided to the
    Vn.api_call() method.

    Required Values:
        The parameter queries: dict is required in this API call, please refer to the Network API documentation for the syntax of the body parameter or set the if_example parameter to True for an example.
    """

    def __init__(self, message="The parameter queries: dict is required in this API call, please refer to the Network API documentation for the syntax of the body parameter or set the if_example parameter to True for an example."):
        self.message = message
        super().__init__(self.message)


