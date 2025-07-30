import json
from pathlib import Path

import requests
from pydantic import BaseModel

from doipy.constants import DomainName, ValidationSchemas
from doipy.exceptions import AuthenticationException
from doipy.validation_utils import validate_schema


class Authentication(BaseModel):
    # optional
    username: str = None
    client_id: str = None
    password: str = None
    token: str = None
    key: str = None

    @classmethod
    def create_instance(cls, username: str = None, client_id: str = None, password: str = None,
                        token: str = None, key: str = None) -> 'Authentication':
        # TODO: can the validation process be formulated as part of the DTR? -> ask Hans
        if not username and not client_id and not token and not key:
            raise AuthenticationException('Provide token, key, username or client_id')

        # build the Authentication object
        authentication = cls()
        if token:
            authentication.token = token
        elif key:
            authentication.key = key
        elif client_id:
            if password:
                authentication.client_id = client_id
                authentication.password = password
            else:
                raise AuthenticationException('Provide password')
        else:
            if password:
                authentication.username = username
                authentication.password = password
            else:
                raise AuthenticationException('Provide password')
        return authentication

    def build_authentication_message(self) -> dict:
        # create the message
        authentication_message = {}
        if self.token:
            authentication_message['authentication'] = {
                'token': self.token
            }
        elif self.key:
            authentication_message['authentication'] = {
                'key': self.key
            }
        elif self.client_id:
            authentication_message['clientId'] = self.client_id
            authentication_message['authentication'] = {
                'password': self.password
            }
        else:
            authentication_message['authentication'] = {
                'username': self.username,
                'password': self.password
            }
        return authentication_message


class DataAndMetadata(BaseModel):
    # optional
    data_bitsq: Path = None
    data_values: dict = None
    metadata_bitsq: Path = None
    metadata_values: dict = None

    @classmethod
    def parse(cls, user_input: dict) -> 'DataAndMetadata':
        # validate the input against the JSON input schema
        url = f'{DomainName.TYPE_API_SCHEMAS.value}/{ValidationSchemas.DATA_AND_METADATA.value}'
        input_schema = requests.get(url).json()

        validate_schema(user_input, input_schema)

        do_input = cls()

        if 'data_bitsq' in user_input:
            data_bitsq = Path(user_input['data_bitsq'])
            do_input.data_bitsq = data_bitsq

        if 'metadata_bitsq' in user_input:
            metadata_bitsq = Path(user_input['metadata_bitsq'])
            do_input.metadata_bitsq = metadata_bitsq

        if 'data_values' in user_input:
            with open(user_input['data_values']) as f:
                data_values = json.load(f)
                do_input.data_values = data_values

        if 'metadata_values' in user_input:
            with open(user_input['metadata_values']) as f:
                metadata_values = json.load(f)
                do_input.metadata_values = metadata_values

        return do_input


class CreateFdoInput(BaseModel):
    # mandatory
    fdo_service_ref: str
    fdo_profile_ref: str
    authentication: Authentication
    fdo_type_ref: str
    # optional
    fdo_rights_ref: str = None
    fdo_genre_ref: str = None
    data_and_metadata: list[DataAndMetadata] = None

    @classmethod
    def parse(cls, user_input: dict) -> 'CreateFdoInput':

        # construct the authentication object
        auth = Authentication.create_instance(user_input['FDO_Authentication'].get('username'),
                                              user_input['FDO_Authentication'].get('client_id'),
                                              user_input['FDO_Authentication'].get('password'),
                                              user_input['FDO_Authentication'].get('token'),
                                              user_input['FDO_Authentication'].get('key'))

        # construct the fdo_input object with the mandatory references
        fdo_input = cls(fdo_service_ref=user_input['FDO_Service_Ref'], fdo_profile_ref=user_input['FDO_Profile_Ref'],
                        fdo_type_ref=user_input['FDO_Type_Ref'], authentication=auth)

        # define the optional references
        if 'FDO_Rights_Ref' in user_input:
            fdo_input.fdo_rights_ref = user_input['FDO_Rights_Ref']
        if 'FDO_Genre_Ref' in user_input:
            fdo_input.fdo_genre_ref = user_input['FDO_Genre_Ref']

        # define the data and metadata arrays which will be used to create the DOs
        if 'FDO_Data_and_Metadata' in user_input:
            fdo_input.data_and_metadata = []
            for item in user_input['FDO_Data_and_Metadata']:
                if item:
                    # create the structure for the data DO and for the metadata DO
                    do = DataAndMetadata.parse(item)
                    fdo_input.data_and_metadata.append(do)

        return fdo_input


class DeleteFdoInput(BaseModel):
    # mandatory
    pid_fdo: str
    fdo_service_ref: str
    authentication: Authentication
    delete_MD: bool
    # optional (those are not required by the user, but they are added in the code after the PID_FDO was resolved)
    ip: str = None
    port: int = None
    data_bitsqs: list[str] = None
    md_bitsqs: list[str] = None

    @classmethod
    def parse(cls, user_input: dict) -> 'DeleteFdoInput':

        # construct the authentication object
        auth = Authentication.create_instance(user_input['FDO_Authentication'].get('username'),
                                              user_input['FDO_Authentication'].get('client_id'),
                                              user_input['FDO_Authentication'].get('password'),
                                              user_input['FDO_Authentication'].get('token'),
                                              user_input['FDO_Authentication'].get('key'))

        del_md = user_input.get('delete_MD', False)

        # construct the fdo_input object with the mandatory references
        fdo_input = cls(pid_fdo=user_input['PID_FDO'], fdo_service_ref=user_input['FDO_Service_Ref'],
                        authentication=auth, delete_MD=del_md)

        return fdo_input


class MoveFdoInput(BaseModel):
    # mandatory
    pid_fdo: str
    fdo_service_ref_source: str
    authentication_source: Authentication
    fdo_service_ref_destination: str
    authentication_destination: Authentication
    # optional (those are not required by the user, but they are added in the code after the PID_FDO was resolved)
    # note that those values are not necessary for all possible configuration types
    ip_source: str = None
    port_source: int = None
    ip_destination: str = None
    port_destination: int = None
    profile: str = None

    @classmethod
    def parse(cls, user_input: dict) -> 'MoveFdoInput':

        # construct the authentication object
        auth_source = Authentication.create_instance(user_input['FDO_Authentication_Source'].get('username'),
                                                     user_input['FDO_Authentication_Source'].get('client_id'),
                                                     user_input['FDO_Authentication_Source'].get('password'),
                                                     user_input['FDO_Authentication_Source'].get('token'),
                                                     user_input['FDO_Authentication_Source'].get('key'))

        auth_destination = Authentication.create_instance(user_input['FDO_Authentication_Destination'].get('username'),
                                                          user_input['FDO_Authentication_Destination'].get('client_id'),
                                                          user_input['FDO_Authentication_Destination'].get('password'),
                                                          user_input['FDO_Authentication_Destination'].get('token'),
                                                          user_input['FDO_Authentication_Destination'].get('key'))

        # construct the fdo_input object with the mandatory references
        fdo_input = cls(pid_fdo=user_input['PID_FDO'], fdo_service_ref_source=user_input['FDO_Service_Ref_Source'],
                        authentication_source=auth_source,
                        fdo_service_ref_destination=user_input['FDO_Service_Ref_Destination'],
                        authentication_destination=auth_destination)

        return fdo_input
