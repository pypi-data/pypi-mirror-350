import json

from doipy.actions.fdo_config_type_14 import (
    create_fdo_config_type_14,
    delete_fdo_config_type_14,
    move_fdo_config_type_14,
)
from doipy.constants import FDOTypeIdentifier, Profile
from doipy.dtr_utils import get_doip_connection, get_service_id
from doipy.exceptions import HandleValueNotFoundException, InputValidationError, ProfileNotSupportedException
from doipy.get_objects_from_apis import get_handle_value, resolve_handle
from doipy.models import CreateFdoInput, DeleteFdoInput, MoveFdoInput
from doipy.validation_utils import get_schema, validate_schema


def create_fdo(user_input: dict):

    # read the necessary elements (service and profile) from the JSON as a starting point to find the corresponding
    # operation in the DTR
    fdo_service_ref = user_input.get('FDO_Service_Ref')
    if not fdo_service_ref:
        raise InputValidationError('FDO_Service_Ref does not exist in the input JSON.')
    fdo_profile_ref = user_input.get('FDO_Profile_Ref')
    if not fdo_profile_ref:
        raise InputValidationError('FDO_Profile_Ref does not exist in the input JSON.')

    # get the schema which belongs to the inputs of the create operation for the chosen profile
    schema = get_schema('Create_FDO', fdo_profile_ref, [fdo_service_ref])

    # validate the user input against the input schema for the specific profile
    validate_schema(user_input, schema)

    # create an instance of FdoInput class
    fdo_input = CreateFdoInput.parse(user_input)

    # choose the correct create_fdo operation
    if fdo_profile_ref == Profile.CONFIG_TYPE_14.value:
        response = create_fdo_config_type_14(fdo_input)
    # check here for other profiles/configuration types
    else:
        raise ProfileNotSupportedException('Create_FDO is not supported by DOIPY for the chosen Profile.')

    return response[0]['output']['id']


def delete_fdo(user_input: dict):

    # read the necessary elements (PID_FDO and service) from the JSON as a starting point to find the corresponding
    # operation in the DTR
    pid_fdo = user_input.get("PID_FDO")
    if not pid_fdo:
        raise InputValidationError('PID_FDO does not exist in the input JSON.')
    fdo_service_ref = user_input.get("FDO_Service_Ref")
    if not fdo_service_ref:
        raise InputValidationError('FDO_Service_Ref does not exist in the input JSON.')

    # resolve the PID_FDO to get the FDO record
    fdo_record = resolve_handle(pid_fdo)

    # read the profile from the fdo record
    profile = get_handle_value(fdo_record, FDOTypeIdentifier.FDO_PROFILE_REF.value)

    # get the schema which belongs to the inputs of the delete operation for the profile corresponding to PID_FDO
    schema = get_schema('Delete_FDO', profile, [fdo_service_ref])

    # validate the user input against the input schema for the given profile
    validate_schema(user_input, schema)

    # create an instance of DeleteFdoInput
    fdo_input = DeleteFdoInput.parse(user_input)

    # get service ID, IP and port
    service_id = get_service_id(fdo_service_ref)
    ip, port = get_doip_connection(service_id)

    # get data and metadata bitsequences
    try:
        data = json.loads(get_handle_value(fdo_record, FDOTypeIdentifier.FDO_DATA_REFS.value))
        fdo_input.data_bitsqs = data
    except HandleValueNotFoundException:
        pass

    if fdo_input.delete_MD:
        try:
            md = json.loads(get_handle_value(fdo_record, FDOTypeIdentifier.FDO_MD_REFS.value))
            fdo_input.md_bitsqs = md
        except HandleValueNotFoundException:
            pass

    # write all values into the fdo_input object
    fdo_input.ip = ip
    fdo_input.port = port

    # choose the correct delete_fdo operation
    if profile == Profile.CONFIG_TYPE_14.value:
        result = delete_fdo_config_type_14(fdo_input)
    # check here for other profiles/configuration types
    else:
        raise ProfileNotSupportedException('Delete_FDO is not supported by DOIPY for the chosen Profile.')

    return result


def move_fdo(user_input: dict):

    # read the necessary elements from the input JSON as a starting point to find the corresponding operation in the DTR
    for attr in ['PID_FDO', 'FDO_Service_Ref_Source', 'FDO_Service_Ref_Destination']:
        if attr not in user_input:
            raise InputValidationError(f'{attr} does not exist in the input JSON.')
    pid_fdo = user_input['PID_FDO']
    fdo_service_ref_source = user_input['FDO_Service_Ref_Source']
    fdo_service_ref_destination = user_input['FDO_Service_Ref_Destination']

    # resolve the PID_FDO to get the FDO record
    fdo_record = resolve_handle(pid_fdo)

    # read the profile from the fdo record, profile is no configuration type specific attribute
    profile = get_handle_value(fdo_record, FDOTypeIdentifier.FDO_PROFILE_REF.value)

    # get the schema which belongs to the inputs of the move operation for the profile corresponding to PID_FDO
    schema = get_schema('Move_FDO', profile, [fdo_service_ref_source,
                                              fdo_service_ref_destination])

    # validate the user input against the input schema for the given profile
    validate_schema(user_input, schema)

    # create an instance of MoveFdoInput class
    fdo_input = MoveFdoInput.parse(user_input)

    # get service ID, IP and port of source/destination DOIP service
    service_id_source = get_service_id(fdo_service_ref_source)
    ip_source, port_source = get_doip_connection(service_id_source)
    service_id_destination = get_service_id(fdo_service_ref_destination)
    ip_destination, port_destination = get_doip_connection(service_id_destination)

    # write all values into the fdo_input object
    fdo_input.ip_source = ip_source
    fdo_input.port_source = port_source
    fdo_input.ip_destination = ip_destination
    fdo_input.port_destination = port_destination
    fdo_input.profile = profile

    # choose the correct move_fdo operation
    if profile == Profile.CONFIG_TYPE_14.value:
        result = move_fdo_config_type_14(fdo_input, fdo_record)
    # check here for other profiles/configuration types
    else:
        raise ProfileNotSupportedException('Move_FDO is not supported by DOIPY for the chosen Profile.')
    return result
