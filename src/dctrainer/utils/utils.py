def build_log_tag(*args, **kwargs):
    """
    Generate a string as a tag to parse the logs more easily
    
    If you call `build_log_tag("arg1", "arg2", key1="value1", key2="value2")`
    This function generate this string in return :
    [arg1][arg2][key1="value1"][key2="value2"]
    """
    generated_string = ""
    for v in args:
        generated_string += "[" + str(v) + "]"
    
    for k,v in kwargs.items():
        generated_string += "[" + str(k) + "=" + "\"" + str(v) + "\"]"
    
    return generated_string