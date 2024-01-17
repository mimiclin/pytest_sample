import jsonschema
from jsonschema import validate


def validate_json(instance, schema):
    """REF: https://json-schema.org/ """
    try:
        validate(instance=instance, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "Given JSON data is InValid"
        return False

    message = "Given JSON data is Valid"
    return True
