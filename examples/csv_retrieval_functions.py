"""
These functions aim to be a first, very simple step.
They will take previous results (contained in a csv file) and, if the results are there,
they will return them. Otherwise, an error will be generated.

Steps to be implemented are:
- Create the function (and make sure it runs offline).
- Register it in the database
- Serve the database, be able to query this function from React FrontEnd.
                    (or ITIS-Dakota backend, if generating an LHS).
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

## TODO could include label converter here (as part of the function)
## maybe even give option to user to do so in the GUI
# (e.g. user can provide "display" label for variable, which is optional)
# save (& load) all of those in a JSON file, which stays with the app

def retrieve_csv_result(
    csv_file_path: str, **inputs: Dict[str, float]
) -> Dict[str, float]:
    """
    Retrieve the result from a csv file.
    """

    df = pd.read_csv(csv_file_path)

    for col in inputs.keys():
        if col not in df.columns:
            raise ValueError(
                f"Input {col} not in the csv file. Columns are: {df.columns.values}"
            )
    result = df.loc[np.all(df[inputs.keys()] == inputs.values(), axis=1)]  #type: ignore
    # Check if the result is empty or has multiple rows
    assert len(result) != 0, f"No result found for inputs {inputs}."
    assert len(result) == 1, f"Multiple results found for inputs {inputs}."

    result = result.drop(columns=inputs.keys())
    result = result.iloc[0].to_dict()
    print(f"Result found for inputs {inputs}: \n\n {result}")
    return result

# class FunctionReturn(TypedDict):
#     # "EM_Shunting_Total_Current",
#     # "EM_Shunting_Current_Nerve",
#     # "EM_Shunting_Current_Outside",
#     # "EM_Shunting_Shunted_Current",
#     # "Dosimetry_Saline_PeakE",
#     # "Dosimetry_Saline_Iso99E",
#     # "Dosimetry_Saline_Iso98E",
#     # "Dosimetry_Saline_icnirp_peaks",
#     # "Dosimetry_Nerve_PeakE",
#     # "Dosimetry_Nerve_Iso99E",
#     # "Dosimetry_Nerve_Iso98E",
#     # "Dosimetry_Nerve_icnirp_peaks",
#     # "Dosimetry_Fascicles_PeakE",
#     # "Dosimetry_Fascicles_Iso99E",
#     # "Dosimetry_Fascicles_Iso98E",
#     # "Dosimetry_Fascicles_icnirp_peaks",
#     Thermal_Peak_Overall: float
#     Thermal_Peak_Nerve: float
#     Thermal_Peak_Saline: float


def nih_in_silico(
    SigmaMuscle: float,
    SigmaEpineurium: float,
    SigmaPerineurium: float,
    SigmaAlongFascicles: float,
    SigmaTransverseFascicles: float,
    ThermalConductivity_Fascicles: float,
    HeatTransferRate_Fascicles: float,
    ThermalConductivity_Saline: float,
    HeatTransferRate_Saline: float,
    ThermalConductivity_Connective_Tissue: float,
    HeatTransferRate_Connective_Tissue: float,
) -> Dict[str, float]:
    """
    This function emulates the NIH in silico pipeline.
    Instead of running the actual pipeline, it will retrieve the results from a csv file
    (or return an error if the results are not there).
    """

    csv_file_path: str = (
        "/home/ordonez/mmux/mmux_react/flaskapi/mmux_python/data/results_Final_50LHS_TitrationProcessed.csv"
    )

    inputs = {
        "SigmaMuscle": SigmaMuscle,
        "SigmaEpineurium": SigmaEpineurium,
        "SigmaPerineurium": SigmaPerineurium,
        "SigmaAlongFascicles": SigmaAlongFascicles,
        "SigmaTransverseFascicles": SigmaTransverseFascicles,
        "ThermalConductivity_Fascicles": ThermalConductivity_Fascicles,
        "HeatTransferRate_Fascicles": HeatTransferRate_Fascicles,
        "ThermalConductivity_Saline": ThermalConductivity_Saline,
        "HeatTransferRate_Saline": HeatTransferRate_Saline,
        "ThermalConductivity_Connective_Tissue": ThermalConductivity_Connective_Tissue,
        "HeatTransferRate_Connective_Tissue": HeatTransferRate_Connective_Tissue,
    }
    outputs = [
        # "EM_Shunting_Total_Current",
        # "EM_Shunting_Current_Nerve",
        # "EM_Shunting_Current_Outside",
        # "EM_Shunting_Shunted_Current",
        # "Dosimetry_Saline_PeakE",
        # "Dosimetry_Saline_Iso99E",
        # "Dosimetry_Saline_Iso98E",
        # "Dosimetry_Saline_icnirp_peaks",
        # "Dosimetry_Nerve_PeakE",
        # "Dosimetry_Nerve_Iso99E",
        # "Dosimetry_Nerve_Iso98E",
        # "Dosimetry_Nerve_icnirp_peaks",
        # "Dosimetry_Fascicles_PeakE",
        # "Dosimetry_Fascicles_Iso99E",
        # "Dosimetry_Fascicles_Iso98E",
        # "Dosimetry_Fascicles_icnirp_peaks",
        "Thermal_Peak_Overall",
        "Thermal_Peak_Nerve",
        "Thermal_Peak_Saline",
    ]

    return retrieve_csv_result(
        csv_file_path=csv_file_path, inputs=inputs, outputs=outputs
    )


if __name__ == "__main__":
    example_csv_file_path = "/home/ordonez/mmux/mmux_react/flaskapi/mmux_python/data/results_Final_50LHS_TitrationProcessed.csv"
    example_inputs = {
        "SigmaMuscle": 0.8105296106421488,
        "SigmaEpineurium": 0.1354717001508955,
        "SigmaPerineurium": 0.00496445857521,
        "SigmaAlongFascicles": 1.669324662304592,
        "SigmaTransverseFascicles": 0.1021138777716998,
        "ThermalConductivity_Fascicles": 0.3009090670855689,
        "HeatTransferRate_Fascicles": 34615.014043851304,
        "ThermalConductivity_Saline": 0.2324731525719103,
        "HeatTransferRate_Saline": 1230.5476269345313,
        "ThermalConductivity_Connective_Tissue": 0.1457043777250806,
        "HeatTransferRate_Connective_Tissue": 1683.5556671060272,
    }

    print(nih_in_silico(**example_inputs))
    print("Done!")

    from openapi_client import Configuration, ApiClient
    from openapi_client.api.function_api import FunctionApi

    # from openapi_client.api.function_job_api import FunctionJobApi
    # from openapi_client.api.function_job_collection_api import FunctionJobCollectionApi
    from openapi_client.models.function import Function

    configuration = Configuration()
    configuration.host = "http://localhost:8087"

    api_client = ApiClient(configuration=configuration)
    funcapi = FunctionApi(api_client)
    # funcjobapi = FunctionJobApi(api_client)
    # funcjobcolapi = FunctionJobCollectionApi(api_client)

    funcapi.delete_all_functions()
    functions: Dict[str, Function] = {}
    created_functions: Dict[str, Function] = {}

    def dict_to_text_inputs(inputs: Dict[str, Any]) -> str:
        # it actually matters '{"x" instead of "{'x' ...
        return str(inputs).translate(str.maketrans({'"': "'", "'": '"'}))

    functions["nih_in_silico"] = Function(
        name="nih_in_silico",
        type="local.python",
        description="Retrieve the NIH results (Final) from a csv file.",
        input_schema={
            "type": "object",
            "properties": {
                "SigmaMuscle": {"type": "number"},
                "SigmaEpineurium": {"type": "number"},
                "SigmaPerineurium": {"type": "number"},
                "SigmaAlongFascicles": {"type": "number"},
                "SigmaTransverseFascicles": {"type": "number"},
                "ThermalConductivity_Fascicles": {"type": "number"},
                "HeatTransferRate_Fascicles": {"type": "number"},
                "ThermalConductivity_Saline": {"type": "number"},
                "HeatTransferRate_Saline": {"type": "number"},
                "ThermalConductivity_Connective_Tissue": {"type": "number"},
                "HeatTransferRate_Connective_Tissue": {"type": "number"},
            },
        },
        tags=["cacheable"],
        url="./examples/csv_retrieval_functions.py:nih_in_silico",
    )

    for function_name, function in functions.items():
        print(f"Adding function: {function_name}")

        created_functions[function_name] = funcapi.create_function(function)

        print(
            f"Search for function {function.name}, found {len(funcapi.search_functions_by_name(function.name))}"
        )

    import pprint

    print(f"\nList of functions:\n {pprint.pformat(funcapi.list_functions())}\n")

    function_job = funcapi.run_function(
        function_id=created_functions["nih_in_silico"].id,
        inputs=dict_to_text_inputs(example_inputs),
    )
    print(function_job)

    print("Running function...")
    print(f"Created job: {function_job}")
    print("Done!")
