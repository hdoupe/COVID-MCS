# Write or import your Compute Studio functions here.
import COVID_MCS

def get_version():
    version = COVID_MCS.__version__
    return f"COVID_MCS v{version}"


def get_inputs(meta_param_dict):
    pass


def validate_inputs(meta_param_dict, adjustment, errors_warnings):
    pass


def run_model(meta_param_dict, adjustment):
    pass
