def ultra_max_pro_deep_copy(obj):
    """
    This is a utility method to handle deep copy for any type of object
    Currnetly supports only lists or dictionaries, as that is what is used so far in the overall code
    """
    # recursive deep copy: currently only supports dictionaries or lists
    if isinstance(obj, list):
        copy_obj = [ultra_max_pro_deep_copy(x) for x in obj] # recursively deep copy everything
        return copy_obj
    elif isinstance(obj, dict):
        copy_obj = {}
        for key in obj:
            copy_key = ultra_max_pro_deep_copy(key)
            copy_value = ultra_max_pro_deep_copy(obj[key])
            copy_obj[copy_key] = copy_value
        return copy_obj
    
    # more types to add if other object types are used in futuere

    return obj

