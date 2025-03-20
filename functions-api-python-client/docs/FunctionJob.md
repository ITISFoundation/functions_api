# FunctionJob


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**function_id** | **int** |  | 
**status** | [**JobStatus**](JobStatus.md) |  | [optional] 
**inputs** | **object** |  | [optional] 
**outputs** | **object** |  | [optional] 
**job_info** | **object** |  | [optional] 
**created_at** | **datetime** |  | [optional] 

## Example

```python
from openapi_client.models.function_job import FunctionJob

# TODO update the JSON string below
json = "{}"
# create an instance of FunctionJob from a JSON string
function_job_instance = FunctionJob.from_json(json)
# print the JSON string representation of the object
print(FunctionJob.to_json())

# convert the object into a dict
function_job_dict = function_job_instance.to_dict()
# create an instance of FunctionJob from a dict
function_job_from_dict = FunctionJob.from_dict(function_job_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


