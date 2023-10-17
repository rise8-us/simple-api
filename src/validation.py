import re

class Optional():
    def __init__(self, schema_type):
        self.schema_type = schema_type
    def __call__(self, item):
        if item == None:
            return None
        return self.schema_type(item)

class Regex():
    def __init__(self, regex):
        self.regex = regex
    def __call__(self, item):
        if re.match(self.regex, item):
            return None
        return f"item '{item}' does not match regex '{self.regex}'"
    
class CustomMessage():
    def __init__(self, schema, message):
        self.message = message
        self.schema = schema

ALPHANUMERIC = Regex(r'^[a-zA-Z0-9]+$')
INTEGER = Regex(r'^[0-9]+$')

TYPE_REGEX = {
    str: str,
    int: INTEGER,
}

def trim_none(coll):
    return (x for x in coll if x is not None)

def optional(schema):
    return {k: Optional(v) for k, v in schema.items()}

def to_search_schema(schema):
    return {k: Optional(TYPE_REGEX.get(v, v)) for k, v in schema.items()}

def verify_schema_item(schema_key, schema_type, item):
    if type(schema_type) == CustomMessage:
        if (schema_error := verify_schema_item(schema_key, schema_type.schema, item)):
            return {"error": schema_type.message}
        return None
    if type(schema_type) == Optional:
        if schema_key not in item:
            return None
        schema_type = schema_type.schema_type
    if schema_key not in item:
        return {"error": f"key '{schema_key}' not found in item"}
    if type(schema_type) == dict:
        if type(item[schema_key]) != dict:
            return {"error": f"key '{schema_key}' is not of type 'dict'"}
        if (errors := verify(item[schema_key], schema_type)):
            return {"error": errors}
        return None
    if type(schema_type) == list:
        if type(item[schema_key]) != list:
            return {"error": f"key '{schema_key}' is not of type 'list'"}
        if (errors := list(trim_none(verify_schema_item(schema_key, schema_type[0], x) for x in item[schema_key]))):
            return {"error": errors}
        return None
    if type(schema_type) == Regex:
        if type(item[schema_key]) != str:
            return {"error": f"key '{schema_key}' is not of type 'str'"}
        if (schema_error := schema_type(item[schema_key])):
            return {"error": schema_error}
        schema_type = str
    if type(schema_type) == type(lambda: None) and (schema_error := schema_type(item[schema_key])):
        return {"error": schema_error}
    if type(item[schema_key]) != schema_type:
        return {"error": f"key '{schema_key}' is not of type '{schema_type}'"}
    return None

def verify(item, schema: dict, exclusive=False):
    if exclusive:
        if (errors := [f"Error: key '{k}' not recognized" for k in item if not k in schema]):
            return errors
    return list(trim_none(verify_schema_item(k, v, item) for k, v in schema.items()))
