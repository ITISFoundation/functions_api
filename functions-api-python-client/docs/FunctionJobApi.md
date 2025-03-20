# openapi_client.FunctionJobApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_function_job**](FunctionJobApi.md#get_function_job) | **GET** /functionJob/{function_job_id} | Get Function Job
[**get_function_jobs**](FunctionJobApi.md#get_function_jobs) | **GET** /function/{function_id}/jobs | Get Function Jobs
[**get_jobs_status**](FunctionJobApi.md#get_jobs_status) | **GET** /function/job/status | Get Jobs Status
[**list_function_jobs**](FunctionJobApi.md#list_function_jobs) | **GET** /functionJobs | List all function jobs with optional filtering


# **get_function_job**
> FunctionJob get_function_job(function_job_id)

Get Function Job

Get the details of a specific function job.

Parameters:
    function_job_id: ID of the function job to retrieve

Returns:
    Function job details including status, inputs, and outputs

Raises:
    HTTPException: If job is not found (404)

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
    api_instance = openapi_client.FunctionJobApi(api_client)
    function_job_id = 56 # int | 

    try:
        # Get Function Job
        api_response = api_instance.get_function_job(function_job_id)
        print("The response of FunctionJobApi->get_function_job:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionJobApi->get_function_job: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_job_id** | **int**|  | 

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

# **get_function_jobs**
> List[FunctionJob] get_function_jobs(function_id, limit=limit, offset=offset, status=status, start_date=start_date, end_date=end_date)

Get Function Jobs

Get all jobs for a specific function with optional filtering and pagination.

### Example


```python
import openapi_client
from openapi_client.models.function_job import FunctionJob
from openapi_client.models.job_status import JobStatus
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
    api_instance = openapi_client.FunctionJobApi(api_client)
    function_id = 56 # int | ID of the function to get jobs for
    limit = 56 # int | Maximum number of jobs to return (optional)
    offset = 56 # int | Number of jobs to skip (optional)
    status = openapi_client.JobStatus() # JobStatus | Filter by job status (optional)
    start_date = '2013-10-20T19:20:30+01:00' # datetime | Filter jobs after this date (optional)
    end_date = '2013-10-20T19:20:30+01:00' # datetime | Filter jobs before this date (optional)

    try:
        # Get Function Jobs
        api_response = api_instance.get_function_jobs(function_id, limit=limit, offset=offset, status=status, start_date=start_date, end_date=end_date)
        print("The response of FunctionJobApi->get_function_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionJobApi->get_function_jobs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **function_id** | **int**| ID of the function to get jobs for | 
 **limit** | **int**| Maximum number of jobs to return | [optional] 
 **offset** | **int**| Number of jobs to skip | [optional] 
 **status** | [**JobStatus**](.md)| Filter by job status | [optional] 
 **start_date** | **datetime**| Filter jobs after this date | [optional] 
 **end_date** | **datetime**| Filter jobs before this date | [optional] 

### Return type

[**List[FunctionJob]**](FunctionJob.md)

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

# **get_jobs_status**
> List[FunctionJob] get_jobs_status(job_ids)

Get Jobs Status

Get status of multiple jobs.

Parameters:
    job_ids: List of job IDs to check

Returns:
    List of job statuses

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
    api_instance = openapi_client.FunctionJobApi(api_client)
    job_ids = [56] # List[Optional[int]] | 

    try:
        # Get Jobs Status
        api_response = api_instance.get_jobs_status(job_ids)
        print("The response of FunctionJobApi->get_jobs_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionJobApi->get_jobs_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_ids** | [**List[Optional[int]]**](int.md)|  | 

### Return type

[**List[FunctionJob]**](FunctionJob.md)

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

# **list_function_jobs**
> List[FunctionJob] list_function_jobs(limit=limit, offset=offset, status=status, function_id=function_id, start_date=start_date, end_date=end_date)

List all function jobs with optional filtering

List all function jobs with optional filtering and pagination.

Parameters:
    limit: Maximum number of jobs to return (default: all)
    offset: Number of jobs to skip for pagination (default: 0)
    status: Filter by job status (e.g., PENDING, RUNNING, COMPLETED, FAILED)
    function_id: Filter jobs for a specific function
    start_date: Include jobs created after this date
    end_date: Include jobs created before this date

Returns:
    List[FunctionJob]: A filtered list of function jobs

### Example


```python
import openapi_client
from openapi_client.models.function_job import FunctionJob
from openapi_client.models.job_status import JobStatus
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
    api_instance = openapi_client.FunctionJobApi(api_client)
    limit = 56 # int | Maximum number of jobs to return (optional)
    offset = 56 # int | Number of jobs to skip (optional)
    status = openapi_client.JobStatus() # JobStatus | Filter by job status (optional)
    function_id = 56 # int | Filter by function ID (optional)
    start_date = '2013-10-20T19:20:30+01:00' # datetime | Filter jobs after this date (optional)
    end_date = '2013-10-20T19:20:30+01:00' # datetime | Filter jobs before this date (optional)

    try:
        # List all function jobs with optional filtering
        api_response = api_instance.list_function_jobs(limit=limit, offset=offset, status=status, function_id=function_id, start_date=start_date, end_date=end_date)
        print("The response of FunctionJobApi->list_function_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FunctionJobApi->list_function_jobs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Maximum number of jobs to return | [optional] 
 **offset** | **int**| Number of jobs to skip | [optional] 
 **status** | [**JobStatus**](.md)| Filter by job status | [optional] 
 **function_id** | **int**| Filter by function ID | [optional] 
 **start_date** | **datetime**| Filter jobs after this date | [optional] 
 **end_date** | **datetime**| Filter jobs before this date | [optional] 

### Return type

[**List[FunctionJob]**](FunctionJob.md)

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

