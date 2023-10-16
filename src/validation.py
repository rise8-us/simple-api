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

ALPHANUMERIC = Regex(r'^[a-zA-Z0-9]+$')
INTEGER = Regex(r'^[0-9]+$')

def trim_none(coll):
    return (x for x in coll if x is not None)

def optional(schema):
    return {k: Optional(v) for k, v in schema.items()}

def verify_schema_item(schema_key, schema_type, item):
    if type(schema_type) == Optional:
        if schema_key not in item:
            return None
        schema_type = schema_type.schema_type
    if schema_key not in item:
        return {"error": f"key '{schema_key}' not found in item"}
    if type(schema_type) == Regex:
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
