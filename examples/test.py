import pprint
import time

import openapi_client
import openapi_client.api.function_api
import openapi_client.api.function_job_api

configuration = openapi_client.Configuration()
configuration.host = "http://127.0.0.1:8000"

api_client = openapi_client.ApiClient(configuration=configuration)

funcapi = openapi_client.api.function_api.FunctionApi(api_client)
funcjobapi = openapi_client.api.function_job_api.FunctionJobApi(api_client)
funcjobcolapi = (
    openapi_client.api.function_job_collection_api.FunctionJobCollectionApi(
        api_client
    )
)

funcapi.delete_all_functions()

functions = {}
created_functions = {}

functions["test_function1"] = openapi_client.models.Function(
    name="test_function1",
    type="local.python",
    description="Test function 1",
    url="/home/vangeit/src/functions_api/examples/test_script/test_function1.py:test_function1",
)
functions["test_function1_slow"] = openapi_client.models.Function(
    name="test_function1_slow",
    type="local.python",
    description="Test function 1 (slow)",
    input_schema={
        "type": "object",
        "properties": {"x": {"type": "number"}, "y": {"type": "number"}},
        "required": ["x", "y"],
    },
    output_schema={
        "type": "object",
        "properties": {"result": {"type": "number"}},
        "required": ["result"],
    },
    tags=["cacheable"],
    url="/home/vangeit/src/functions_api/examples/test_script/test_function1_slow.py:test_function1",
)
functions["test_study1"] = openapi_client.models.Function(
    name="test_study1",
    type="remote.http",
    description="Test study",
    url="https://api.osparc.io/studies/2332423423",
)

for function_name, function in functions.items():
    print(f"Adding function: {function_name}")

    created_functions[function_name] = funcapi.create_function(function)

    print(
        f"Search for function {function.name}, found {len(funcapi.search_functions_by_name(function.name))}"
    )

print(f"\nList of functions:\n {pprint.pformat(funcapi.list_functions())}\n")
print(
    f"\nCacheable functions:\n {pprint.pformat(funcapi.search_functions_by_tags(tags=['cacheable']))}\n"
)

function_job = funcapi.run_function(
    function_id=created_functions["test_function1_slow"].id,
    inputs='{"z": 1, "y": 2}',
)

print(f"Running function, created job: {function_job}")

print("\nRun batch of 3 inputs of test_function1_slow:")
response = funcapi.batch_run_function(
    function_id=created_functions["test_function1_slow"].id,
    collection_name="Batch of test_function1_slow",
    request_body=['{"x": 1, "y": 2}', '{"x": 1, "y": 3}', '{"x": 1, "y": 4}'],
    max_workers=2,
)

while (
    "COMPLETED" not in funcjobcolapi.get_collection_status(response.id).status
):
    time.sleep(1)
    response = funcjobcolapi.get_collection_status(response.id)
    print(response)

print("\nJobs done, results:")
for job_id in response.job_ids:
    function_job = funcjobapi.get_function_job(function_job_id=job_id)
    print(function_job)


# pprint.pprint(
#     funcjobapi.list_function_jobs(
#         function_id=created_functions["test_function1_slow"].id
#     )
# )

# running_function_job = funcjobapi.get_function_job(
#       function_job_id=function_job.id
# )
#
# print(f"Status function job: {running_function_job.status}")
# print(f"Output of the function job: {running_function_job.outputs}")
#
# map_jobs_list = funcapi.map_function(
#     function_id=created_functions["test_function1_slow"].id,
#     max_workers=2,
#     request_body=['{"x": 1, "y": 2}', '{"x": 1, "y": 3}', '{"x": 1, "y": 4}'],
# )
#
# print(
#     f"Running function map, created {len(map_jobs_list)} jobs: {map_jobs_list}"
# )
#
# map_jobs_ids = [map_job.id for map_job in map_jobs_list]
#
# while "PENDING" in str(funcjobapi.get_jobs_status(map_jobs_ids)):
#     import time
#
#     time.sleep(1)
#     jobs_statuses = funcjobapi.get_jobs_status(map_jobs_ids)
#     print(
#         f"{len([job_status for job_status in jobs_statuses if 'COMPLETED' in job_status.status])} jobs completed, "
#         f"{len([job_status for job_status in jobs_statuses if 'PENDING' in job_status.status])} jobs pending"
#     )
#
# print(f"JOBS ARE DONE:\n {funcjobapi.get_jobs_status(map_jobs_ids)}")
