import re

def extract_value_from_source(input_string, lookup_field):
    regex = fr"<iframe.*?{lookup_field}=['\"](.*?)['\"]"
    match = re.search(regex, input_string)
    if match:
        return match.group(1)
    else:
        return None
