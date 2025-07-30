import json

def update_dict_with_cast(curr_conf: dict, new_conf: dict):
    for key in curr_conf.keys():
        if key in new_conf:
            key_type = type(curr_conf[key])
            cast_func = key_type if key_type in (str, int) else json.loads
            curr_conf[key] = cast_func(new_conf[key])