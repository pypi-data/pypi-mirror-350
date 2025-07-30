from jsonschema import validate

from doipy.exceptions import InvalidOperationError, OperationNotSupportedException, UnexpectedError
from doipy.get_objects_from_apis import get_object_from_dtr, get_schema_from_typeapi


def get_schema(operation_str: str, fdo_profile_ref: str = None, fdo_service_refs: list[str] = None):
    if operation_str == 'Create_FDO':

        # get the service information from the dtr
        service = get_object_from_dtr(fdo_service_refs[0])

        # get all operations that can be performed on the given service
        operation_pids = service.get('implementsOperations')
        if not operation_pids:
            raise OperationNotSupportedException('The service does not support any operations.')

        # find the correct create_FDO operation (which corresponds to the given profile)
        found_operation = None
        for operation_pid in operation_pids:
            if not found_operation:
                operation = get_object_from_dtr(operation_pid)   # get an operation that is supported by this profile
                if operation.get('operationCategory') != operation_str:   # check that the operation is create
                    continue   # go to next operation
                related_profiles = operation.get('relatedFdoProfiles')
                if related_profiles:
                    for related_profile in related_profiles:
                        # condition that the correct FDO operation was found
                        if related_profile == fdo_profile_ref:
                            found_operation = operation
                            break
            else:
                break

        if not found_operation:
            raise OperationNotSupportedException('The service does not support Create_FDO for this profile, or the '
                                                 'given profile does not exist.')

    elif operation_str in ['Delete_FDO', 'Move_FDO']:

        # get the profile object from the DTR
        profile_definition = get_object_from_dtr(fdo_profile_ref)

        # get all operations that can be performed on the given FDO, specified by a list in the profile
        operation_pids = profile_definition.get('References')
        if not operation_pids:
            raise OperationNotSupportedException('The profile does not support any operations.')

        # Search for a delete operation that can be generally performed on an FDO with the given profile.
        found_operation = None
        for operation_pid in operation_pids:
            operation = get_object_from_dtr(operation_pid)
            # condition that the correct FDO operation was found
            if operation.get('operationCategory') == operation_str:
                found_operation = operation
                break
        if not found_operation:
            raise OperationNotSupportedException('The FDO does not support any Delete_FDO operation.')

        # Check that all involved DOIP services implement the required operation.
        for fdo_service_ref in fdo_service_refs:
            service = get_object_from_dtr(fdo_service_ref)
            service_supports_operation = False
            implemented_operations = service.get('implementsOperations')
            if not implemented_operations:
                raise OperationNotSupportedException(f'The DOIP service identified by {fdo_service_ref} does not '
                                                     f'support any operations.')
            for s in implemented_operations:
                if s == found_operation['identifier']:
                    service_supports_operation = True
                    break
            if not service_supports_operation:
                raise OperationNotSupportedException(f'The DOIP service identified by {fdo_service_ref} does not '
                                                     f'support {operation_str} operation.')

    else:
        raise UnexpectedError('An unexpected server error occurred.')

    # return input schema from the DTR for the chosen create_FDO operation
    input_pid = found_operation.get('inputs')
    if not input_pid:
        raise InvalidOperationError('The operation does not have any input schema.')

    validation_schema = get_schema_from_typeapi(input_pid)
    return validation_schema


def validate_schema(user_input: dict, input_schema: dict):
    # validate the input against the JSON input schema
    validate(instance=user_input, schema=input_schema)
