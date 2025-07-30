import ast
import json


def validate_json(test_json):
    """
    Returns True if `test_json` is valid JSON (either double-escaped or normal),
    and the parsed result is a dict or list.
    Otherwise returns False.
    """
    # 1. Attempt parsing as double-escaped JSON first.
    #    We try to interpret the string as a Python string literal, then parse it as JSON.
    try:
        unescaped_json = ast.literal_eval(test_json)
        parsed = json.loads(unescaped_json)
        return isinstance(parsed, (dict, list)), unescaped_json
    except (ValueError, SyntaxError, json.JSONDecodeError, TypeError):
        pass  # Means it wasn’t valid double-escaped JSON

    # 2. If the above fails, attempt parsing as normal JSON.
    try:
        parsed = json.loads(test_json)
        return isinstance(parsed, (dict, list)), test_json
    except json.JSONDecodeError:
        return False, None