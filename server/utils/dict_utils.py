def safe_dict_get(dictionary, keys, default_value):
    value = dictionary
    for key in keys:
        if not isinstance(value, dict):
            break
        value = value.get(key, default_value)

    return value
