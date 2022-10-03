from yaml import safe_load


def read_params(config_path="sensor/config/params.yaml"):

    method_name = read_params.__name__

    try:
        with open(config_path) as f:
            config = safe_load(f)

        return config

    except Exception as e:
        raise Exception(
            f"Exception occurred in {__file__}, Method : {method_name}, Error : {str(e)}"
        )
