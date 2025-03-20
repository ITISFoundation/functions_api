# FunctionJobCollection

Model for a collection of function jobs

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**description** | **str** |  | 
**job_ids** | **List[int]** |  | 
**status** | **str** |  | 

## Example

```python
from openapi_client.models.function_job_collection import FunctionJobCollection

# TODO update the JSON string below
json = "{}"
# create an instance of FunctionJobCollection from a JSON string
function_job_collection_instance = FunctionJobCollection.from_json(json)
# print the JSON string representation of the object
print(FunctionJobCollection.to_json())

# convert the object into a dict
function_job_collection_dict = function_job_collection_instance.to_dict()
# create an instance of FunctionJobCollection from a dict
function_job_collection_from_dict = FunctionJobCollection.from_dict(function_job_collection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


