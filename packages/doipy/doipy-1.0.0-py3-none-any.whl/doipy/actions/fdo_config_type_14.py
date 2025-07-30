import contextlib
import json
import os
import shutil
import tempfile
import uuid

from benedict import benedict
from doip_sdk import send_request

from doipy.actions.doip import create, delete_bitsq, retrieve, update_all_metadata, update_metadata
from doipy.constants import DOIPOperation, DOType, FDOTypeIdentifier, ResponseStatus
from doipy.dtr_utils import get_doip_connection, get_service_id
from doipy.exceptions import HandleValueNotFoundException, InvalidRequestException
from doipy.get_objects_from_apis import get_handle_value
from doipy.models import Authentication, CreateFdoInput, DeleteFdoInput, MoveFdoInput
from doipy.request_and_response import decode_json_response


def create_fdo_config_type_14(fdo_input: CreateFdoInput):
    # get service ID, IP and port
    service_id = get_service_id(fdo_input.fdo_service_ref)
    ip, port = get_doip_connection(service_id)

    # create first message
    message_1 = {
        'targetId': f'{service_id}',
        'operationId': DOIPOperation.CREATE.value,
    }

    # provide correct set of authentication credentials
    authentication_message = fdo_input.authentication.build_authentication_message()
    message_1 = message_1 | authentication_message

    # create second message
    message_2 = {
        'type': DOType.FDO.value,
        'attributes': {
            'content': {
                'id': '',
                'name': 'FAIR Digital Object',
                # FDO_Profile_Ref: mandatory
                FDOTypeIdentifier.FDO_PROFILE_REF.value: fdo_input.fdo_profile_ref,
                # FDO_Type_Ref: mandatory
                FDOTypeIdentifier.FDO_TYPE_REF.value: fdo_input.fdo_type_ref,
                # FDO_Status: mandatory
                FDOTypeIdentifier.FDO_STATUS.value: 'created'
            }
        }
    }
    # FDO_Rights_Ref: optional
    if fdo_input.fdo_rights_ref:
        message_2['attributes']['content'][FDOTypeIdentifier.FDO_RIGHTS_REF.value] = fdo_input.fdo_rights_ref
    # FDO_Genre_Ref: optional
    if fdo_input.fdo_genre_ref:
        message_2['attributes']['content'][FDOTypeIdentifier.FDO_GENRE_REF.value] = fdo_input.fdo_genre_ref

    # create the data and metadata DOs
    if fdo_input.data_and_metadata:
        data_refs = []
        metadata_refs = []
        for item in fdo_input.data_and_metadata:
            # create the data do
            if item.data_bitsq or item.data_values:
                response_decoded = create(target_id=service_id, ip=ip, port=port, do_type=DOType.DO.value,
                                          do_name='Data-DO', bitsq=item.data_bitsq, metadata=item.data_values,
                                          username=fdo_input.authentication.username,
                                          client_id=fdo_input.authentication.client_id,
                                          password=fdo_input.authentication.password,
                                          token=fdo_input.authentication.token)
                if response_decoded[0]['status'] == ResponseStatus.SUCCESS.value:
                    data_ref = response_decoded[0]['output']['id']
                    data_refs.append(data_ref)
                else:
                    raise InvalidRequestException(response_decoded)
            # create the metadata do
            if item.metadata_bitsq or item.metadata_values:
                response_decoded = create(target_id=service_id, ip=ip, port=port, do_type=DOType.DO.value,
                                          do_name='Metadata-DO', bitsq=item.metadata_bitsq,
                                          metadata=item.metadata_values, username=fdo_input.authentication.username,
                                          client_id=fdo_input.authentication.client_id,
                                          password=fdo_input.authentication.password,
                                          token=fdo_input.authentication.token)
                if response_decoded[0]['status'] == ResponseStatus.SUCCESS.value:
                    metadata_ref = response_decoded[0]['output']['id']
                    metadata_refs.append(metadata_ref)
                else:
                    raise InvalidRequestException(response_decoded)

        if data_refs:
            message_2['attributes']['content'][FDOTypeIdentifier.FDO_DATA_REFS.value] = data_refs
        if metadata_refs:
            message_2['attributes']['content'][FDOTypeIdentifier.FDO_MD_REFS.value] = metadata_refs

    # send request and read response
    data = [message_1, message_2]
    response = send_request(ip, port, data)
    response_decoded = decode_json_response(response)

    # check status code
    if response_decoded[0]['status'] == ResponseStatus.SUCCESS.value:
        return response_decoded
    raise InvalidRequestException(response_decoded)


def delete_fdo_config_type_14(fdo_input: DeleteFdoInput):
    # assumption for move_fdo: all data PIDs are moved to the same repository as a bundle.
    if fdo_input.data_bitsqs:
        for data_pid in fdo_input.data_bitsqs:
            # delete the data bit-sequence and update the data-record with DO_Status and Status_URL
            with contextlib.suppress(KeyError):
                delete_bitsq(target_id=data_pid, ip=fdo_input.ip, port=fdo_input.port,
                             username=fdo_input.authentication.username, password=fdo_input.authentication.password,
                             client_id=fdo_input.authentication.client_id, token=fdo_input.authentication.token)
            # In case that the DO does not have any bit-sequence, a KeyError occurs. The KeyError is caught and the
            # program continues as no bit-sequence needs to be deleted.

    # update the Metadata-record with DO_Status and Status_URL
    if fdo_input.md_bitsqs:
        for md_pid in fdo_input.md_bitsqs:
            # delete the metadata bit-sequence and update the metadata-record with DO_Status and Status_URL
            with contextlib.suppress(KeyError):
                delete_bitsq(target_id=md_pid, ip=fdo_input.ip, port=fdo_input.port,
                             username=fdo_input.authentication.username, password=fdo_input.authentication.password,
                             client_id=fdo_input.authentication.client_id, token=fdo_input.authentication.token)

    # update the FDO-record with FDO_Status
    update_md = {FDOTypeIdentifier.FDO_STATUS.value: "deleted"}
    update_metadata(target_id=fdo_input.pid_fdo, ip=fdo_input.ip, port=fdo_input.port,
                    metadata=update_md, add_if_not_exists=True, username=fdo_input.authentication.username,
                    password=fdo_input.authentication.password, client_id=fdo_input.authentication.client_id,
                    token=fdo_input.authentication.token)

    # return a status code
    return 1


def move_fdo_config_type_14(fdo_input: MoveFdoInput, fdo_record: dict):
    # get the pids identifying the data respectively metadata dos
    with contextlib.suppress(HandleValueNotFoundException):
        data_pids = json.loads(get_handle_value(fdo_record, FDOTypeIdentifier.FDO_DATA_REFS.value))

    with contextlib.suppress(HandleValueNotFoundException):
        md_pids = json.loads(get_handle_value(fdo_record, FDOTypeIdentifier.FDO_MD_REFS.value))

    # download the data bit-sequence(s) and the corresponding handle values from the DOs and store them locally
    data_dos_paths = []
    data_dos_folders = []
    if data_pids:
        for data_pid in data_pids:
            paths = {}

            # retrieve the do
            response_data_do = retrieve(target_id=data_pid, ip=fdo_input.ip_source, port=fdo_input.port_source,
                                        username=fdo_input.authentication_source.username,
                                        password=fdo_input.authentication_source.password,
                                        client_id=fdo_input.authentication_source.client_id,
                                        token=fdo_input.authentication_source.token)
            data_do = benedict(response_data_do[0])
            data_values = data_do.get_dict('output.attributes.content', default={})
            data_element = data_do.get_dict('output.elements[0]', default={})

            # get the values of the data DO and write it to a file, store the local path to the file
            if data_values:
                data_values.pop('id', None)
                my_uuid = str(uuid.uuid4())
                path = save_values(data_values, my_uuid)
                paths['data_values'] = path

            # download the bit-sequence of the data DO and store the local path to the file
            if data_element:
                file_id = data_element.get_str('id', default='')
                if file_id:
                    file_name = data_element.get_str('attributes.filename', default=file_id)
                    data_bitsq_path, data_bitsq_folder = save_bitsq(target_id=data_pid, ip=fdo_input.ip_source,
                                                                    port=fdo_input.port_source, file_id=file_id,
                                                                    file_name=file_name,
                                                                    username=fdo_input.authentication_source.username,
                                                                    password=fdo_input.authentication_source.password,
                                                                    client_id=fdo_input.authentication_source.client_id,
                                                                    token=fdo_input.authentication_source.token)
                    paths['data_bitsq'] = data_bitsq_path
                    data_dos_folders.append(data_bitsq_folder)
                else:
                    raise KeyError(f'The bit-sequence of the PID {data_pid} does not have an id.')

            # write the paths to the list
            data_dos_paths.append(paths)

    # download the metadata bit-sequence(s) and the corresponding handle values from the DOs and store them locally
    md_dos_paths = []
    md_dos_folders = []
    if md_pids:
        for md_pid in md_pids:
            paths = {}

            # retrieve the do
            response_md_do = retrieve(target_id=md_pid, ip=fdo_input.ip_source, port=fdo_input.port_source,
                                      username=fdo_input.authentication_source.username,
                                      password=fdo_input.authentication_source.password,
                                      client_id=fdo_input.authentication_source.client_id,
                                      token=fdo_input.authentication_source.token)
            md_do = benedict(response_md_do[0])
            md_values = md_do.get_dict('output.attributes.content', default={})
            md_element = md_do.get_dict('output.elements[0]', default={})

            # get the values of the data DO and write it to a file, store the local path to the file
            if md_values:
                md_values.pop('id', None)
                my_uuid = str(uuid.uuid4())
                path = save_values(md_values, my_uuid)
                paths['metadata_values'] = path

            # download the bit-sequence of the data DO and store the local path to the file
            if md_element:
                file_id = md_element.get_str('id', default='')
                if file_id:
                    file_name = md_element.get_str('attributes.filename', default=file_id)
                    md_bitsq_path, md_bitsq_folder = save_bitsq(target_id=md_pid, ip=fdo_input.ip_source,
                                                                port=fdo_input.port_source,
                                                                file_id=file_id, file_name=file_name,
                                                                username=fdo_input.authentication_source.username,
                                                                password=fdo_input.authentication_source.password,
                                                                client_id=fdo_input.authentication_source.client_id,
                                                                token=fdo_input.authentication_source.token)
                    paths['metadata_bitsq'] = md_bitsq_path
                    md_dos_folders.append(md_bitsq_folder)
                else:
                    raise KeyError(f'The bit-sequence of the PID {md_pid} does not have an id.')

            # write the paths to the list
            md_dos_paths.append(paths)

    # read the type from the fdo record (mandatory in fdo record)
    fdo_type_ref = get_handle_value(fdo_record, FDOTypeIdentifier.FDO_TYPE_REF.value)

    # generate the input dictionary for create_fdo
    input_create_fdo = {
        'FDO_Service_Ref': fdo_input.fdo_service_ref_destination,
        'FDO_Profile_Ref': fdo_input.profile,
        'FDO_Type_Ref': fdo_type_ref,
    }
    # read the rights and genre from the fdo record, those might be configuration type specific and are optional in the
    # fdo record
    try:
        fdo_rights_ref = get_handle_value(fdo_record, FDOTypeIdentifier.FDO_RIGHTS_REF.value)
        input_create_fdo['FDO_Rights_Ref'] = fdo_rights_ref
    except HandleValueNotFoundException:
        pass
    try:
        fdo_genre_ref = get_handle_value(fdo_record, FDOTypeIdentifier.FDO_GENRE_REF.value)
        input_create_fdo['FDO_Genre_Ref'] = fdo_genre_ref
    except HandleValueNotFoundException:
        pass

    # add authentication credentials
    auth = {}
    if fdo_input.authentication_destination.username:
        auth['username'] = fdo_input.authentication_destination.username
    if fdo_input.authentication_destination.password:
        auth['password'] = fdo_input.authentication_destination.password
    if fdo_input.authentication_destination.client_id:
        auth['clientId'] = fdo_input.authentication_destination.client_id
    if fdo_input.authentication_destination.token:
        auth['token'] = fdo_input.authentication_destination.token
    input_create_fdo['FDO_Authentication'] = auth

    # add files
    files = data_dos_paths + md_dos_paths
    input_create_fdo['FDO_Data_and_Metadata'] = files

    # create a new fdo in the destination DOIP service
    input_create_fdo_parsed = CreateFdoInput.parse(input_create_fdo)
    create_fdo_result = create_fdo_config_type_14(input_create_fdo_parsed)
    # check status code
    if create_fdo_result[0]['status'] != ResponseStatus.SUCCESS.value:
        raise InvalidRequestException(create_fdo_result)
    moved_fdo = create_fdo_result[0]['output']['id']

    # remove files
    for file in data_dos_paths:
        if file.get('data_bitsq'):
            os.remove(file['data_bitsq'])
        if file.get('data_values'):
            os.remove(file['data_values'])
    for file in md_dos_paths:
        if file.get('metadata_bitsq'):
            os.remove(file['metadata_bitsq'])
        if file.get('metadata_values'):
            os.remove(file['metadata_values'])

    # remove folders
    folders = data_dos_folders + md_dos_folders
    for folder in folders:
        os.rmdir(folder)

    # generate the input dictionary for delete_fdo
    input_delete_fdo = {
        'PID_FDO': fdo_input.pid_fdo,
        'FDO_Service_Ref': fdo_input.fdo_service_ref_source,
        'delete_MD': True,
    }
    # add authentication credentials
    auth = {}
    if fdo_input.authentication_source.username:
        auth['username'] = fdo_input.authentication_source.username
    if fdo_input.authentication_source.password:
        auth['password'] = fdo_input.authentication_source.password
    if fdo_input.authentication_source.client_id:
        auth['clientId'] = fdo_input.authentication_source.client_id
    if fdo_input.authentication_source.token:
        auth['token'] = fdo_input.authentication_source.token
    input_delete_fdo['FDO_Authentication'] = auth

    # parse input dictionary and add ip, port
    input_delete_fdo_parsed = DeleteFdoInput.parse(input_delete_fdo)
    input_delete_fdo_parsed.ip = fdo_input.ip_source
    input_delete_fdo_parsed.port = fdo_input.port_source
    if data_pids:
        input_delete_fdo_parsed.data_bitsqs = data_pids
    if md_pids:
        input_delete_fdo_parsed.md_bitsqs = md_pids

    # delete the FDO
    delete_fdo_result = delete_fdo_config_type_14(input_delete_fdo_parsed)
    # check status code
    if delete_fdo_result != 1:
        raise InvalidRequestException(delete_fdo_result)

    # set fdo status of the newly created FDO to 'moved' (?)
    fdo_status = {FDOTypeIdentifier.FDO_STATUS.value: 'moved'}
    update_md_result = update_metadata(target_id=moved_fdo, ip=fdo_input.ip_source, port=fdo_input.port_source,
                                       metadata=fdo_status, add_if_not_exists=True,
                                       username=fdo_input.authentication_source.username,
                                       client_id=fdo_input.authentication_source.client_id,
                                       password=fdo_input.authentication_source.password,
                                       token=fdo_input.authentication_source.token)
    # check status code
    if update_md_result[0]['status'] != ResponseStatus.SUCCESS.value:
        raise InvalidRequestException(update_md_result)

    # set HS_Alias in pid_fdo
    set_alias = {'HS_ALIAS': moved_fdo}
    update_md_result = update_all_metadata(target_id=fdo_input.pid_fdo, ip=fdo_input.ip_source,
                                           port=fdo_input.port_source, metadata=set_alias,
                                           username=fdo_input.authentication_source.username,
                                           client_id=fdo_input.authentication_source.client_id,
                                           password=fdo_input.authentication_source.password,
                                           token=fdo_input.authentication_source.token)
    # check status code
    if update_md_result[0]['status'] != ResponseStatus.SUCCESS.value:
        raise InvalidRequestException(update_md_result)

    return create_fdo_result[0]['output']['id']


def save_bitsq(target_id: str, ip: str, port: int, file_id: str = None, file_name: str = None, username: str = None,
               client_id: str = None, password: str = None, token: str = None):
    # create message
    message = {
        'targetId': target_id,
        'operationId': DOIPOperation.RETRIEVE.value,
        'attributes': {
            'element': file_id
        }
    }
    if username or client_id or password or token:
        # validate authentication credentials and build message with authentication credentials
        authentication = Authentication.create_instance(username, client_id, password, token)
        authentication_message = authentication.build_authentication_message()
        # concatenate messages
        message = message | authentication_message

    # send request and return response
    response = send_request(ip, port, [message])

    temp_folder = tempfile.gettempdir()
    path_folder = os.path.join(temp_folder, file_id)
    path_file = os.path.join(temp_folder, file_id, file_name)
    if os.path.exists(path_folder):
        shutil.rmtree(path_folder)

    # create temporary folder
    os.makedirs(path_folder)

    # create temporary file in the folder
    with open(path_file, "wb") as binary_file:
        # Write bytes to file
        binary_file.write(response.content[1])

    return path_file, path_folder


def save_values(md: dict, file_id: str):
    temp_folder = tempfile.gettempdir()
    path = os.path.join(temp_folder, file_id) + '-1'
    with open(path, 'w') as f:
        f.write(json.dumps(md))
    return path
