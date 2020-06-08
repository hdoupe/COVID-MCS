# Write or import your Compute Studio functions here.
import inspect
import os
import json
import traceback
import paramtools
from COVID_MCS.COVID_MCS import COVID_MCS_TEST, COVID_MCS_PARAMETERS


def get_version():
    version = COVID_MCS.__version__
    return f"COVID_MCS v{version}"


def get_inputs(meta_param_dict):


    model_params = COVID_MCS_PARAMETERS()
    model_params = model_params.dump()

    retrun({"meta_parameters" : {}, "model_parameters" : model_params})


def validate_inputs(meta_param_dict, adjustment, errors_warnings):
    params = COVID_MCS_PARAMETERS()
    params.adjust(adjustment, raise_errors = False)

    errors_warnings["errors"].update(params.errors)

    return {"errors_warnings": errors_warnings}


def run_model(meta_param_dict, adjustment):

    params = COVID_MCS_PARAMETERS()
    params.adjust(adjustment)

    c = COVID_MCS_TEST(adjustment = params)
    model_output = c.MCS_Test()

    to_print = "<table>" + model_output + "</table>"

    out = {
        "renderable": [{
            "media_type": "table",
            "title": "My Table",
            "data": "<table>...</table>"
            }],
        "downloadable": []
    }

    return(out)

run_model({}, {})
