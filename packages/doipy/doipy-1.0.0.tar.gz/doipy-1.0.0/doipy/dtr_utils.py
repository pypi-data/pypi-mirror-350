import json

import requests

from doipy.constants import DomainName
from doipy.exceptions import HandleValueNotFoundException
from doipy.get_objects_from_apis import get_handle_value, resolve_handle

cached_configs = {}


def get_connection(service: str, protocol: str) -> (str, int):
    """
    Get the serviceId, IP and port from the handle correponding to the service that should be connected to.
    """

    # cache the service_id, ip and port of the requested service
    if service not in cached_configs:
        # resolve the service handle
        service_pid_record = resolve_handle(service)
        # find all service configs in the service handle
        service_configs = get_handle_value(service_pid_record, '21.T11966/e236fff11511968d8696')
        service_configs = json.loads(service_configs)
        # iterate over service configs to check whether there is an entry for the required protocol
        protocol_config_found = False
        protocol_config = {}
        for entry in service_configs:
            if entry['protocol'] == protocol:
                protocol_config_found = True
                protocol_config = entry
                break
        if not protocol_config_found:
            raise HandleValueNotFoundException(f'Could not find {protocol} configurations in the ServiceConfigs')
        else:
            cached_configs[service] = {
                'service': service,
                'ip': protocol_config['ip'],
                'port': protocol_config['port']
            }
    return cached_configs[service]['ip'], int(cached_configs[service]['port'])


def get_doip_connection(service: str) -> (str, int):
    return get_connection(service, 'DOIP on TCP')


def get_http_connection(service: str) -> (str, int):
    return get_connection(service, 'HTTP')


def get_service_id(fdo_service_ref: str) -> str:
    # get the service information from the dtr
    url = f'{DomainName.TYPE_REGISTRY_OBJECTS.value}/{fdo_service_ref}'
    service = requests.get(url).json()

    # get the service ID
    service_id = service['serviceId']
    return service_id
