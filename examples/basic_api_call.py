if __name__ == "__main__":
    from openapi_client import Configuration, ApiClient
    from openapi_client.api.function_api import FunctionApi

    configuration = Configuration()
    configuration.host = "http://localhost:8087"

    api_client = ApiClient(configuration=configuration)
    funcapi = FunctionApi(api_client)
    print(funcapi.list_functions())
    """Result (after running "make test"; otherwise probably empty list):
    [Function(id=1, name='test_function1', type='local.python', url='./examples/test_script/test_function1.py:test_function1', description='Test function 1', input_schema=None, output_schema=None, tags=None), Function(id=2, name='test_function1_slow', type='local.python', url='./examples/test_script/test_function1_slow.py:test_function1', description='Test function 1 (slow)', input_schema={'type': 'object', 'properties': {'x': {'type': 'number'}, 'y': {'type': 'number'}}, 'required': ['x', 'y']}, output_schema={'type': 'object', 'properties': {'result': {'type': 'number'}}, 'required': ['result']}, tags=['cacheable']), Function(id=3, name='test_study1', type='remote.http', url='https://api.osparc.io/studies/2332423423', description='Test study', input_schema=None, output_schema=None, tags=None)]
    """
