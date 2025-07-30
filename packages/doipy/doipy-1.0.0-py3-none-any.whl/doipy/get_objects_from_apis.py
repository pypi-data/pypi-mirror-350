import requests

from doipy.constants import DomainName
from doipy.exceptions import HandleNotFoundException, HandleValueNotFoundException, UnexpectedError


def resolve_handle(pid: str):
    url = f'{DomainName.RESOLVE_PID.value}/{pid}'
    response = requests.get(url)

    # check status code and raise an HTTP error if status code is not valid
    response.raise_for_status()

    # if no error, turn response json into a dictionary
    pid_record = response.json()

    response_code = pid_record.get('responseCode')
    if response_code == 2:
        raise HandleNotFoundException(f'Something unexpected went wrong during handle resolution of {pid}.')
    elif response_code == 100:
        raise HandleNotFoundException(f'Handle {pid} Not Found.')
    elif response_code == 200:
        raise HandleNotFoundException(
            f'Values Not Found. The handle {pid} exists but has no values (or no values according to the types and '
            f'indices specified).')
    elif response_code == 1:
        return pid_record
    else:
        raise UnexpectedError('An unexpected server error occurred.')


def get_handle_value(handle_json: dict, key: str):
    """
    Get the handle value corresponding to a handle key from a PID record that is received via the handle API
    """
    found_value = None
    for item in handle_json['values']:
        if item['type'] == key:
            found_value = item['data']['value']
            break
    if not found_value:
        raise HandleValueNotFoundException(f"The PID record does not contain the handle key "
                                           f"'{key}'.")
    return found_value


def get_object_from_dtr(pid: str):
    url = f'{DomainName.TYPE_REGISTRY_OBJECTS.value}/{pid}'
    response = requests.get(url)

    # check status code and raise an HTTP error if status code is not valid
    response.raise_for_status()

    # if no error, turn response json into a dictionary and return it
    return response.json()


def get_schema_from_typeapi(pid: str):
    url = f'{DomainName.TYPE_API_SCHEMAS.value}/{pid}'
    response = requests.get(url)

    # check status code and raise an HTTP error if status code is not valid
    response.raise_for_status()

    # if no error, turn response json into a dictionary and return it
    return response.json()
