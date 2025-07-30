import json

from doip_sdk import Response


def decode_json_response(response: Response) -> list:
    result = []
    for item in response.content:
        decoded_json = json.loads(item)
        result.append(decoded_json)
    return result


def print_json_response(response: list):
    for item in response:
        print(json.dumps(item, indent=2))
        print('#')
    print('#')
