import json
import uuid
from pathlib import Path

from doip_sdk import send_request

from doipy.constants import DOIPOperation, DOTypeIdentifier, ResponseStatus
from doipy.exceptions import UnauthorizedException
from doipy.models import Authentication
from doipy.request_and_response import decode_json_response


def hello(target_id: str, ip: str, port: int):
    """
    Implements 0.DOIP/Op.Hello: An operation to allow a client to get information about the DOIP service.
    """
    # create request message
    message = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.HELLO.value
    }
    # send request and return response
    response = send_request(ip, port, [message])
    response_decoded = decode_json_response(response)
    return response_decoded


def list_operations(target_id: str, ip: str, port: int, username: str = None, client_id: str = None,
                    password: str = None, token: str = None, key: str = None):
    """
    Implements 0.DOIP/Op.ListOperations: An operation to request the list of operations that can be invoked on the
    target DO.
    """
    # create request message
    message = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.LIST_OPERATION.value
    }
    # validate authentication credentials and build message with authentication credentials, if authentication
    # credentials are provided
    if username or client_id or password or token or key:
        authentication = Authentication.create_instance(username, client_id, password, token, key)
        authentication_message = authentication.build_authentication_message()
        # concatenate messages
        message = message | authentication_message
    # send request and read response
    response = send_request(ip, port, [message])
    response_decoded = decode_json_response(response)
    return response_decoded


def create(target_id: str,
           ip: str,
           port: int,
           do_type: str,
           do_name: str = None,
           do_identifier: str = None,
           bitsq: Path = None,
           metadata: dict = None,
           username: str = None,
           client_id: str = None,
           password: str = None,
           token: str = None,
           key: str = None):
    """
    Implements 0.DOIP/Op.Create: An operation to create a digital object (containing at most one data bit-sequence)
    within the DOIP service. The target of a creation operation is the DOIP service itself.
    """
    # store messages in data
    data = []

    # create first message
    message_1 = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.CREATE.value
    }
    # validate authentication credentials and build message with authentication credentials
    authentication = Authentication.create_instance(username, client_id, password, token, key)
    authentication_message = authentication.build_authentication_message()

    # concatenate messages
    message_1 = message_1 | authentication_message
    data.append(message_1)

    # create second message: DO of type document in Cordra for the file which is added
    message_2 = {
        'type': do_type,
        'attributes': {
            'content': {
                'id': ''
            }
        }
    }

    # add identifier to the DO
    if do_identifier:
        message_2['id'] = do_identifier

    # add name to the DO
    if do_name:
        message_2['attributes']['content'] = message_2['attributes']['content'] | {'name': do_name}

    # add metadata to DO
    if metadata:
        message_2['attributes']['content'] = message_2['attributes']['content'] | metadata

    if bitsq:
        # add information on files to DO
        filename = bitsq.name
        my_uuid = str(uuid.uuid4())
        message_2['elements'] = [
            {
                'id': my_uuid,
                'type': 'text/plain',
                'attributes': {
                    'filename': filename
                }
            }
        ]
        data.append(message_2)

        # third message
        message_3 = {
            'id': my_uuid
        }
        data.append(message_3)

        # send content of files
        data.append(bitsq)

    else:
        data.append(message_2)

    # send request and read response
    response = send_request(ip, port, data)
    response_decoded = decode_json_response(response)
    return response_decoded


def retrieve(target_id: str, ip: str, port: int, file: str = None, username: str = None, client_id: str = None,
             password: str = None, token: str = None, key: str = None):
    """
    Implements 0.DOIP/Op.Retrieve: An operation to allow a client to get information about an (F)DO at a service.
    """
    # create message
    message = {
        'targetId': target_id,
        'operationId': DOIPOperation.RETRIEVE.value
    }
    if file:
        message['attributes'] = {
            'element': file
        }
    if username or client_id or password or token or key:
        # validate authentication credentials and build message with authentication credentials
        authentication = Authentication.create_instance(username, client_id, password, token, key)
        authentication_message = authentication.build_authentication_message()
        # concatenate messages
        message = message | authentication_message

    # send request and return response
    response = send_request(ip, port, [message])

    # decode first segment
    first_segment_json = json.loads(response.content[0])

    # if response is success and a file is returned
    if first_segment_json['status'] == ResponseStatus.SUCCESS.value and file:

        # if a filename is given, use this file name
        filename = first_segment_json.get('attributes').get('filename')
        splits = filename.split('/')
        filename = splits[len(splits) - 1]
        f = filename if filename else 'data'
        with open(f, "wb") as binary_file:
            # Write bytes to file
            binary_file.write(response.content[1])
        return [first_segment_json]

    # if response is not success or no file is returned
    else:
        response_decoded = decode_json_response(response)
        return response_decoded


def delete(target_id: str, ip: str, port: int, username: str = None, client_id: str = None, password: str = None,
           token: str = None, key: str = None):
    """
    Implements 0.DOIP/Op.Delete: An operation to allow a client to delete an DO at a service. This operation just
    deletes the referenced DO but not any other DOs which are referenced by the given DO.
    """
    # create message
    message = {
        'targetId': target_id,
        'operationId': DOIPOperation.DELETE.value
    }
    # validate authentication credentials and build message with authentication credentials
    authentication = Authentication.create_instance(username, client_id, password, token, key)
    authentication_message = authentication.build_authentication_message()
    # concatenate messages
    message = message | authentication_message

    # send request and return response
    response = send_request(ip, port, [message])
    response_decoded = decode_json_response(response)
    return response_decoded


def search(target_id: str, ip: str, port: int, query: str, username: str = None, client_id: str = None,
           password: str = None, token: str = None, key: str = None):
    """Implements 0.DOIP/Op.Search"""
    # create message
    message = {
        'targetId': target_id,
        'operationId': DOIPOperation.SEARCH.value,
        'attributes': {
            'query': query
        }
    }
    if username or client_id or password or token or key:
        # validate authentication credentials and build message with authentication credentials
        authentication = Authentication.create_instance(username, client_id, password, token, key)
        authentication_message = authentication.build_authentication_message()
        # concatenate messages
        message = message | authentication_message

    # send request and return response
    response = send_request(ip, port, [message])
    response_decoded = decode_json_response(response)
    return response_decoded


def add_metadata(target_id: str, ip: str, port: int, metadata: dict = None, update_if_exists: bool = False,
                 username: str = None, client_id: str = None, password: str = None,
                 token: str = None, key: str = None):
    """
    Implements 0.DOIP/Op.Update: Add new attributes in the PID record of the digital object with the PID 'target_id'.
    Values that are not updated stay unchanged in the record.
    """

    # raise an exception if the client tries to update DO_status
    # todo this must be part of the adapter
    if DOTypeIdentifier.DO_STATUS.value in metadata:
        raise UnauthorizedException(
            f"You are not authorized to add or update '{DOTypeIdentifier.DO_STATUS.value}' in the handle record.")
    if DOTypeIdentifier.STATUS_URL.value in metadata:
        raise UnauthorizedException(
            f"You are not authorized to add or update '{DOTypeIdentifier.STATUS_URL.value}' in the handle record.")

    # get the current digital object and its values
    current_do = retrieve(target_id=target_id, ip=ip, port=port, username=username, client_id=client_id,
                          password=password, token=token, key=key)
    current_values = current_do[0]['output']['attributes']['content']

    # store messages in data
    data = []

    # create first message
    message_1 = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.UPDATE.value
    }
    # validate authentication credentials and build message with authentication credentials
    authentication = Authentication.create_instance(username, client_id, password, token, key)
    authentication_message = authentication.build_authentication_message()

    # concatenate messages
    message_1 = message_1 | authentication_message
    data.append(message_1)

    # Check that the values which should be added do not exist yet.
    if not update_if_exists:
        for item in metadata:
            if item in current_values:
                raise KeyError(
                    f"'{item}' cannot be added. The key '{item}' already exists in the current list of PID values. To "
                    f"update '{item}', set update_if_exists = True or use the 'update_values' function.")

    # add values to the PID record by concatenating them with old values that should stay the same
    for item in current_values:
        if item not in metadata:
            metadata[item] = current_values[item]

    message_2 = {
        'attributes': {
            'content': metadata
        }
    }
    data.append(message_2)

    # send request and read response
    response = send_request(ip, port, data)
    response_decoded = decode_json_response(response)
    return response_decoded


def update_metadata(target_id: str, ip: str, port: int, metadata: dict = None, add_if_not_exists: bool = False,
                    username: str = None, client_id: str = None, password: str = None,
                    token: str = None, key: str = None):
    """
    Implements 0.DOIP/Op.Update: Update a digital object identified by the PID 'target_id' with new values for the PID
    record of the DO. Values that are not updated stay unchanged in the record.
    """

    # raise an exception if the client tries to update DO_status
    if DOTypeIdentifier.DO_STATUS.value in metadata:
        raise UnauthorizedException(
            f"You are not authorized to add or update '{DOTypeIdentifier.DO_STATUS.value}' in the handle record.")
    if DOTypeIdentifier.STATUS_URL.value in metadata:
        raise UnauthorizedException(
            f"You are not authorized to add or update '{DOTypeIdentifier.STATUS_URL.value}' in the handle record.")

    # get the current digital object and its values
    current_do = retrieve(target_id=target_id, ip=ip, port=port, username=username, client_id=client_id,
                          password=password, token=token, key=key)
    current_values = current_do[0]['output']['attributes']['content']

    # store messages in data
    data = []

    # create first message
    message_1 = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.UPDATE.value
    }
    # validate authentication credentials and build message with authentication credentials
    authentication = Authentication.create_instance(username, client_id, password, token, key)
    authentication_message = authentication.build_authentication_message()

    # concatenate messages
    message_1 = message_1 | authentication_message
    data.append(message_1)

    # Check that the values which should be updated exist already.
    if not add_if_not_exists:
        for item in metadata:
            if item not in current_values:
                raise KeyError(
                    f"'{item}' cannot be updated. The key '{item}' does not exist in the current list of PID values. To"
                    f" add '{item}', set add_if_not_exists = True or use the 'add_values' function.")

    # update values in the PID record by concatenating them with old values that should stay the same
    for item in current_values:
        if item not in metadata:
            metadata[item] = current_values[item]

    message_2 = {
        'attributes': {
            'content': metadata
        }
    }
    data.append(message_2)

    # send request and read response
    response = send_request(ip, port, data)
    response_decoded = decode_json_response(response)
    return response_decoded


def delete_metadata(target_id: str, ip: str, port: int, metadata: list = None, ignore_if_not_exists: bool = False,
                    username: str = None, client_id: str = None, password: str = None,
                    token: str = None, key: str = None):
    """
    Implements 0.DOIP/Op.Update: Delete some metadata from the PID record of a digital object identified by the PID
    'target_id'. Values that should be deleted but do not exist in the record are ignored if ignore_if_not_exists is set
     to True.
    """

    # raise an exception if the client tries to update DO_status
    if DOTypeIdentifier.DO_STATUS.value in metadata:
        raise UnauthorizedException(
            f"You are not authorized to delete '{DOTypeIdentifier.DO_STATUS.value}' from the handle record.")
    if DOTypeIdentifier.STATUS_URL.value in metadata:
        raise UnauthorizedException(
            f"You are not authorized to delete '{DOTypeIdentifier.STATUS_URL.value}' from the handle record.")

    # get the current digital object and its values
    current_do = retrieve(target_id=target_id, ip=ip, port=port, username=username, client_id=client_id,
                          password=password, token=token, key=key)
    current_values = current_do[0]['output']['attributes']['content']

    # store messages in data
    data = []

    # create first message
    message_1 = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.UPDATE.value
    }
    # validate authentication credentials and build message with authentication credentials
    authentication = Authentication.create_instance(username, client_id, password, token, key)
    authentication_message = authentication.build_authentication_message()

    # concatenate messages
    message_1 = message_1 | authentication_message
    data.append(message_1)

    # Check that the values which should be deleted exist already.
    if not ignore_if_not_exists:
        for item in metadata:
            if item not in current_values:
                raise KeyError(
                    f"'{item}' cannot be deleted. The key '{item}' does not exist in the current list of PID values.")

    # delete values from the PID record by just keeping the old values that should stay
    keep_metadata = {}
    for item in current_values:
        if item not in metadata:
            keep_metadata[item] = current_values[item]

    message_2 = {
        'attributes': {
            'content': keep_metadata
        }
    }
    data.append(message_2)

    # send request and read response
    response = send_request(ip, port, data)
    response_decoded = decode_json_response(response)
    return response_decoded


def update_all_metadata(target_id: str, ip: str, port: int, metadata: dict = None, username: str = None,
                        client_id: str = None, password: str = None, token: str = None, key: str = None):
    """
    Implements 0.DOIP/Op.Update: Overwrite the whole list of metadata of a digital object identified by the PID
    'target_id' with new values for the PID record of the DO.
    """

    # raise an exception if the client tries to update DO_status
    if DOTypeIdentifier.DO_STATUS.value in metadata:
        raise UnauthorizedException(
            f"You are not authorized to add or update '{DOTypeIdentifier.DO_STATUS.value}' in the handle record.")
    if DOTypeIdentifier.STATUS_URL.value in metadata:
        raise UnauthorizedException(
            f"You are not authorized to add or update '{DOTypeIdentifier.STATUS_URL.value}' in the handle record.")

    # store messages in data
    data = []

    # create first message
    message_1 = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.UPDATE.value
    }
    # validate authentication credentials and build message with authentication credentials
    authentication = Authentication.create_instance(username, client_id, password, token, key)
    authentication_message = authentication.build_authentication_message()

    # concatenate messages
    message_1 = message_1 | authentication_message
    data.append(message_1)

    message_2 = {
        'attributes': {
            'content': metadata
        }
    }
    data.append(message_2)

    # send request and read response
    response = send_request(ip, port, data)
    response_decoded = decode_json_response(response)
    return response_decoded


def update_bitsq(target_id: str, ip: str, port: int, bitsq: Path, username: str = None, client_id: str = None,
                 password: str = None, token: str = None, key: str = None):
    """
    Implements 0.DOIP/Op.Update: Overwrite the bit-sequence of a digital object identified by the PID 'target_id' with
    a new bit-sequence.
    """

    # get the current digital object, its metadata and its file_id
    current_do = retrieve(target_id=target_id, ip=ip, port=port, username=username, client_id=client_id,
                          password=password, token=token, key=key)
    current_values = current_do[0]['output']['attributes']['content']
    elements = current_do[0]['output'].get('elements')
    if not elements:
        raise KeyError('The digital object does not have any bit-sequences. No bit-sequence to be updated.')
    file_id = elements[0]['id']

    # store messages in data
    data = []

    # create first message
    message_1 = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.UPDATE.value
    }
    # validate authentication credentials and build message with authentication credentials
    authentication = Authentication.create_instance(username, client_id, password, token, key)
    authentication_message = authentication.build_authentication_message()

    # concatenate messages
    message_1 = message_1 | authentication_message
    data.append(message_1)

    # second message: send attributes and elements
    message_2 = {
        # change of type not enabled in Cordra. Hence, giving the type is not required.
        'attributes': {
            # Send the old attributes in content variable to keep them.
            'content': current_values
        },
        'elements': [
            # required: id
            # not required: type (if no type is given then type=application/octet-stream), attributes, filename (empty
            # if no value is given)
            {
                'id': file_id,
                'type': 'text/plain',
                'attributes': {
                    'filename': bitsq.name
                }
            }
        ]
    }
    data.append(message_2)

    # third message: send file ID of old bit-sequence
    message_3 = {
        'id': file_id
    }
    data.append(message_3)

    # fourth message: the bit-sequence that should replace the old bit-sequence
    data.append(bitsq)

    # send request and read response
    response = send_request(ip, port, data)
    response_decoded = decode_json_response(response)
    return response_decoded


def delete_bitsq(target_id: str, ip: str, port: int, username: str = None, client_id: str = None, password: str = None,
                 token: str = None, key: str = None):
    """
    Implements 0.DOIP/Op.Update: Delete the bit-sequence of a digital object identified by the PID 'target_id'.
    """

    # get the current digital object, its metadata and its file_id
    current_do = retrieve(target_id=target_id, ip=ip, port=port, username=username, client_id=client_id,
                          password=password, token=token, key=key)
    current_values = current_do[0]['output']['attributes']['content']
    elements = current_do[0]['output'].get('elements')
    if not elements:
        raise KeyError('The digital object does not have any bit-sequence. No bit-sequence to delete.')
    file_id = elements[0]['id']

    # store messages in data
    data = []

    # create first message
    message_1 = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.UPDATE.value,
        # list all payload IDs whose payloads should be deleted
        'attributes': {
            'elementsToDelete': [file_id]
        }
    }
    # validate authentication credentials and build message with authentication credentials
    authentication = Authentication.create_instance(username, client_id, password, token, key)
    authentication_message = authentication.build_authentication_message()

    # concatenate messages
    message_1 = message_1 | authentication_message
    data.append(message_1)

    # update the DO_Status and Status_URL of the DO
    current_values[DOTypeIdentifier.DO_STATUS.value] = "deleted"
    current_values[DOTypeIdentifier.STATUS_URL.value] = "some tombstone URL"  # todo

    # create second message
    message_2 = {
        'attributes': {
            'content': current_values
        }
    }
    data.append(message_2)

    # send request and read response
    response = send_request(ip, port, data)
    response_decoded = decode_json_response(response)
    return response_decoded


def add_bitsq(target_id: str, ip: str, port: int, bitsq: Path, username: str = None, client_id: str = None,
              password: str = None, token: str = None, key: str = None):
    """
    Implements 0.DOIP/Op.Update: Add a bit-sequence to a digital object identified by the PID 'target_id', which does
    not have a bit-sequence yet.
    """

    # get the current digital object and its metadata
    current_do = retrieve(target_id=target_id, ip=ip, port=port, username=username, client_id=client_id,
                          password=password, token=token, key=key)
    current_values = current_do[0]['output']['attributes']['content']
    elements = current_do[0]['output'].get('elements')
    if elements:
        raise KeyError("The digital object already has a bit-sequence. To update the bit-sequence, use the function "
                       "'update_bitsq'.")

    # store messages in data
    data = []

    # create first message
    message_1 = {
        'targetId': f'{target_id}',
        'operationId': DOIPOperation.UPDATE.value
    }
    # validate authentication credentials and build message with authentication credentials
    authentication = Authentication.create_instance(username, client_id, password, token, key)
    authentication_message = authentication.build_authentication_message()

    # concatenate messages
    message_1 = message_1 | authentication_message
    data.append(message_1)

    # if the DO_Status is 'deleted' or 'embargoed', update the status to 'created'
    if (current_values[DOTypeIdentifier.DO_STATUS.value] == 'deleted'
            or current_values[DOTypeIdentifier.DO_STATUS.value] == 'embargoed'):
        current_values[DOTypeIdentifier.DO_STATUS.value] = 'created'

    # if Status_URL is 'deleted' or 'embargoed', remove Status_URL
    if current_values[DOTypeIdentifier.STATUS_URL.value]:
        current_values.pop(DOTypeIdentifier.STATUS_URL.value, None)

    # second message: send attributes and elements
    message_2 = {
        'attributes': {
            'content': current_values
        }
    }

    # add information on file to DO
    filename = bitsq.name
    my_uuid = str(uuid.uuid4())
    message_2['elements'] = [
        {
            'id': my_uuid,
            'type': 'text/plain',
            'attributes': {
                'filename': filename
            }
        }
    ]
    data.append(message_2)

    # third message
    message_3 = {
        'id': my_uuid
    }
    data.append(message_3)

    # send content of files
    data.append(bitsq)

    # send request and read response
    response = send_request(ip, port, data)
    response_decoded = decode_json_response(response)
    return response_decoded
