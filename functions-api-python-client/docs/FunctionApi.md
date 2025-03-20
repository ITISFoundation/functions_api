# openapi_client.FunctionApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**batch_run_function**](FunctionApi.md#batch_run_function) | **POST** /function/{function_id}/batch | Batch Run Function
[**create_function**](FunctionApi.md#create_function) | **POST** /function | Create Function
[**delete_all_functions**](FunctionApi.md#delete_all_functions) | **DELETE** /function/all | Delete All Functions
[**list_functions**](FunctionApi.md#list_functions) | **GET** /function/list | List Functions
[**map_function**](FunctionApi.md#map_function) | **POST** /function/{function_id}/map | Map Function
[**run_function**](FunctionApi.md#run_function) | **POST** /function/{function_id}/run | Run Function
[**search_functions_by_name**](FunctionApi.md#search_functions_by_name) | **GET** /function/searchByName | Search Functions By Name
[**search_functions_by_tags**](FunctionApi.md#search_functions_by_tags) | **GET** /function/searchByTags | Search Functions By Tags
[**update_function_config_function_config_post**](FunctionApi.md#update_function_config_function_config_post) | **POST** /function/config | Update Function Config


# **batch_run_function**
> FunctionJobCollection batch_run_function(function_id, collection_name, request_body, max_workers=max_workers)

Batch Run Function

Run a function with multiple inputs and create a job collection.

Parameters:
    function_id: ID of the function to run
    collection_name: Name for the job collection
    request_body: List of JSON strings containing input parameters
    max_workers: Optional maximum number of parallel workers

Returns:
    Created function job collection containing all job IDs

### Example


```python
import openapi_client
from openapi_client.models.function_job_collection import FunctionJobCollection
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FunctionApi(api_client)
    function_id = 56 # int | 
    collection_name = 'collection_name_example' # str | 
    request_body = ['request_body_example'] # List[str] | 
    max_workers = 56 # int |  (optional)

    try:
        # Batch Run Function
        api_response = api_instance.batch_run_function(function_id, collection_name, request_body, max_workers=max_workers)
        print("The response of FunctionApi->batch_run_function:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionApi->batch_run_function: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_id** | **int**|  | 
 **collection_name** | **str**|  | 
 **request_body** | [**List[str]**](str.md)|  | 
 **max_workers** | **int**|  | [optional] 

### Return type

[**FunctionJobCollection**](FunctionJobCollection.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_function**
> Function create_function(function)

Create Function

Create a new function with optional JSON Schema definitions for input and output.
Validates that provided schemas are valid JSON Schema.
Supports tags for better organization and searchability.

### Example


```python
import openapi_client
from openapi_client.models.function import Function
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FunctionApi(api_client)
    function = openapi_client.Function() # Function | 

    try:
        # Create Function
        api_response = api_instance.create_function(function)
        print("The response of FunctionApi->create_function:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionApi->create_function: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function** | [**Function**](Function.md)|  | 

### Return type

[**Function**](Function.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_all_functions**
> object delete_all_functions()

Delete All Functions

Delete all functions from the store.

Returns:
    Message confirming deletion with count of deleted functions

### Example


```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FunctionApi(api_client)

    try:
        # Delete All Functions
        api_response = api_instance.delete_all_functions()
        print("The response of FunctionApi->delete_all_functions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionApi->delete_all_functions: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_functions**
> List[Function] list_functions()

List Functions

List all functions in the store.

Returns:
    List of all registered functions

### Example


```python
import openapi_client
from openapi_client.models.function import Function
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FunctionApi(api_client)

    try:
        # List Functions
        api_response = api_instance.list_functions()
        print("The response of FunctionApi->list_functions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionApi->list_functions: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Function]**](Function.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **map_function**
> List[FunctionJob] map_function(function_id, request_body, max_workers=max_workers)

Map Function

Start asynchronous processing of multiple inputs with schema validation.

### Example


```python
import openapi_client
from openapi_client.models.function_job import FunctionJob
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FunctionApi(api_client)
    function_id = 56 # int | 
    request_body = ['request_body_example'] # List[str] | 
    max_workers = 56 # int |  (optional)

    try:
        # Map Function
        api_response = api_instance.map_function(function_id, request_body, max_workers=max_workers)
        print("The response of FunctionApi->map_function:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionApi->map_function: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_id** | **int**|  | 
 **request_body** | [**List[str]**](str.md)|  | 
 **max_workers** | **int**|  | [optional] 

### Return type

[**List[FunctionJob]**](FunctionJob.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **run_function**
> FunctionJob run_function(function_id, inputs)

Run Function

Run a function with the given inputs.
Validates inputs and outputs against JSON Schema if defined.

### Example


```python
import openapi_client
from openapi_client.models.function_job import FunctionJob
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FunctionApi(api_client)
    function_id = 56 # int | 
    inputs = 'inputs_example' # str | 

    try:
        # Run Function
        api_response = api_instance.run_function(function_id, inputs)
        print("The response of FunctionApi->run_function:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionApi->run_function: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_id** | **int**|  | 
 **inputs** | **str**|  | 

### Return type

[**FunctionJob**](FunctionJob.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_functions_by_name**
> List[Function] search_functions_by_name(name)

Search Functions By Name

Search for functions by name.

Parameters:
    name: String to search for in function names (case-sensitive partial match)

Returns:
    List of functions whose names contain the search string

### Example


```python
import openapi_client
from openapi_client.models.function import Function
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FunctionApi(api_client)
    name = 'name_example' # str | 

    try:
        # Search Functions By Name
        api_response = api_instance.search_functions_by_name(name)
        print("The response of FunctionApi->search_functions_by_name:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionApi->search_functions_by_name: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 

### Return type

[**List[Function]**](Function.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_functions_by_tags**
> List[Function] search_functions_by_tags(tags, match_all=match_all)

Search Functions By Tags

Search for functions by tags.

Parameters:
    tags: List of tags to search for
    match_all: If True, functions must have all specified tags. If False, functions must have any of the specified tags.

Returns:
    List of functions that match the tag criteria

### Example


```python
import openapi_client
from openapi_client.models.function import Function
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FunctionApi(api_client)
    tags = ['tags_example'] # List[str] | Tags to search for
    match_all = False # bool | If True, functions must have all tags. If False, functions must have any of the tags. (optional) (default to False)

    try:
        # Search Functions By Tags
        api_response = api_instance.search_functions_by_tags(tags, match_all=match_all)
        print("The response of FunctionApi->search_functions_by_tags:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionApi->search_functions_by_tags: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tags** | [**List[str]**](str.md)| Tags to search for | 
 **match_all** | **bool**| If True, functions must have all tags. If False, functions must have any of the tags. | [optional] [default to False]

### Return type

[**List[Function]**](Function.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_function_config_function_config_post**
> object update_function_config_function_config_post(max_parallel_jobs=max_parallel_jobs)

Update Function Config

Update function execution configuration settings.

Parameters:
    max_parallel_jobs: Maximum number of parallel jobs allowed (default: 10)

Returns:
    Updated configuration settings

### Example


```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FunctionApi(api_client)
    max_parallel_jobs = 10 # int |  (optional) (default to 10)

    try:
        # Update Function Config
        api_response = api_instance.update_function_config_function_config_post(max_parallel_jobs=max_parallel_jobs)
        print("The response of FunctionApi->update_function_config_function_config_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionApi->update_function_config_function_config_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **max_parallel_jobs** | **int**|  | [optional] [default to 10]

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

