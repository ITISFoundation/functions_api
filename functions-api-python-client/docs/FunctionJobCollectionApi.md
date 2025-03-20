# openapi_client.FunctionJobCollectionApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_function_job_collection**](FunctionJobCollectionApi.md#create_function_job_collection) | **POST** /functionJobCollection | Create Function Job Collection
[**get_collection_status**](FunctionJobCollectionApi.md#get_collection_status) | **GET** /functionJobCollection/{collection_id}/status | Get Collection Status
[**list_function_job_collections**](FunctionJobCollectionApi.md#list_function_job_collections) | **GET** /functionJobCollection/list | List Function Job Collections


# **create_function_job_collection**
> FunctionJobCollection create_function_job_collection(function_job_collection)

Create Function Job Collection

Create a new function job collection.

Parameters:
    collection: Collection details including name and optional description

Returns:
    Created function job collection

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
    api_instance = openapi_client.FunctionJobCollectionApi(api_client)
    function_job_collection = openapi_client.FunctionJobCollection() # FunctionJobCollection | 

    try:
        # Create Function Job Collection
        api_response = api_instance.create_function_job_collection(function_job_collection)
        print("The response of FunctionJobCollectionApi->create_function_job_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionJobCollectionApi->create_function_job_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_job_collection** | [**FunctionJobCollection**](FunctionJobCollection.md)|  | 

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

# **get_collection_status**
> FunctionJobCollection get_collection_status(collection_id)

Get Collection Status

Get status of a function job collection.

Parameters:
    collection_id: ID of the collection to check

Returns:
    Collection details including current status of all jobs

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
    api_instance = openapi_client.FunctionJobCollectionApi(api_client)
    collection_id = 56 # int | 

    try:
        # Get Collection Status
        api_response = api_instance.get_collection_status(collection_id)
        print("The response of FunctionJobCollectionApi->get_collection_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionJobCollectionApi->get_collection_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **int**|  | 

### Return type

[**FunctionJobCollection**](FunctionJobCollection.md)

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

# **list_function_job_collections**
> List[FunctionJobCollection] list_function_job_collections()

List Function Job Collections

List all function job collections.

Returns:
    List of all function job collections

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
    api_instance = openapi_client.FunctionJobCollectionApi(api_client)

    try:
        # List Function Job Collections
        api_response = api_instance.list_function_job_collections()
        print("The response of FunctionJobCollectionApi->list_function_job_collections:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionJobCollectionApi->list_function_job_collections: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[FunctionJobCollection]**](FunctionJobCollection.md)

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

