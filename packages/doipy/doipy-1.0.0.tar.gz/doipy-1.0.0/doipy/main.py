import json
from pathlib import Path
from typing import Annotated

import requests
import typer
from jsonschema.exceptions import ValidationError

from doipy import (
    add_bitsq,
    add_metadata,
    create,
    create_fdo,
    delete,
    delete_bitsq,
    delete_fdo,
    delete_metadata,
    get_design,
    get_doip_connection,
    get_http_connection,
    get_init_data,
    hello,
    list_operations,
    move_fdo,
    retrieve,
    search,
    update_all_metadata,
    update_bitsq,
    update_metadata,
)
from doipy.constants import ResponseStatus
from doipy.exceptions import (
    AuthenticationException,
    HandleNotFoundException,
    HandleValueNotFoundException,
    InputValidationError,
    InvalidOperationError,
    InvalidRequestException,
    OperationNotSupportedException,
    ProfileNotSupportedException,
    UnauthorizedException,
    UnexpectedError,
)
from doipy.request_and_response import print_json_response

app = typer.Typer()


@app.command(name='hello')
def hello_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying a data service')],
                  ip: Annotated[str, typer.Argument(help='the IP address identifying the data service')],
                  port: Annotated[int, typer.Argument(help='the DOIP port of the data service')]):
    """
    Implements 0.DOIP/Op.Hello: An operation to allow a client to get information about the DOIP service.
    """
    response = hello(target_id, ip, port)
    print_json_response(response)


@app.command(name='list_operations')
def list_operations_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying a data service')],
                            ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
                            port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
                            username: Annotated[
                                str, typer.Option(help='the username of the user at the data service')] = None,
                            client_id: Annotated[
                                str, typer.Option(help='the clientId of the user at the data service')] = None,
                            password: Annotated[
                                str, typer.Option(help='the password of the user at the data service')] = None,
                            token: Annotated[str, typer.Option(help='a token at the data service')] = None,
                            key: Annotated[str, typer.Option(help='a key at the data service')] = None):
    """
    Implements 0.DOIP/Op.ListOperations: An operation to request the list of operations that can be invoked on the
    target DO.
    """
    try:
        response = list_operations(target_id, ip, port, username, client_id, password, token, key)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit() from error

    print_json_response(response)


@app.command(name='create')
def create_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying a data service')],
                   ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
                   port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
                   do_type: Annotated[
                       str, typer.Option(help='name of the DO to be generated at the data service')],
                   do_name: Annotated[
                       str, typer.Option(help='name of the DO to be generated at data service')] = None,
                   do_identifier: Annotated[
                       str, typer.Option(help='PID of the DO to be generated at data service')] = None,
                   bitsq: Annotated[
                       Path, typer.Option(
                           help='Path to a file which comprises the data bit-sequence of the DO to be generated')]
                   = None,
                   metadata: Annotated[
                       Path, typer.Option(
                           help='Path to a JSON file which comprises the data bit-sequence of the DO to be generated')]
                   = None,
                   username: Annotated[
                       str, typer.Option(help='the username of the user at the data service')] = None,
                   client_id: Annotated[
                       str, typer.Option(help='the clientId of the user at the data service')] = None,
                   password: Annotated[
                       str, typer.Option(help='the password of the user at the data service')] = None,
                   token: Annotated[str, typer.Option(help='a token at the data service')] = None,
                   key: Annotated[str, typer.Option(help='a key at the data service')] = None):
    """
    Implements 0.DOIP/Op.Create: An operation to create a digital object (containing at most one data bit-sequence)
    within the DOIP service. The target of a creation operation is the DOIP service itself.
    """
    # get the metadata and write them into a dictionary
    metadata_dict = None
    if metadata:
        try:
            with open(metadata) as f:
                metadata_dict = json.load(f)
        except json.JSONDecodeError as error:
            print("Invalid JSON syntax:", error)
            raise typer.Exit() from error
        except Exception as error:
            print(error)
            raise typer.Exit() from error

    try:
        response = create(target_id, ip, port, do_type, do_name, do_identifier, bitsq, metadata_dict, username,
                          client_id, password, token, key)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit() from error

    print_json_response(response)


@app.command(name='retrieve')
def retrieve_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying an (F)do')],
                     ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
                     port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
                     file: Annotated[str, typer.Option(help='If the bit-sequence should be returned, this is the id of '
                                                            'the file in the DOIP service')] = None,
                     username: Annotated[
                         str, typer.Option(help='the username of the user at the data service')] = None,
                     client_id: Annotated[
                         str, typer.Option(help='the clientId of the user at the data service')] = None,
                     password: Annotated[
                         str, typer.Option(help='the password of the user at the data service')] = None,
                     token: Annotated[str, typer.Option(help='a token at the data service')] = None,
                     key: Annotated[str, typer.Option(help='a key at the data service')] = None):
    """
    Implements 0.DOIP/Op.Retrieve: An operation to allow a client to get information about an (F)DO at a service.
    """
    try:
        response = retrieve(target_id, ip, port, file, username, client_id, password, token, key)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit() from error

    print_json_response(response)


@app.command(name='delete')
def delete_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying an (F)do')],
                   ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
                   port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
                   username: Annotated[
                       str, typer.Option(help='the username of the user at the data service')] = None,
                   client_id: Annotated[
                       str, typer.Option(help='the clientId of the user at the data service')] = None,
                   password: Annotated[
                       str, typer.Option(help='the password of the user at the data service')] = None,
                   token: Annotated[str, typer.Option(help='a token at the data service')] = None,
                   key: Annotated[str, typer.Option(help='a key at the data service')] = None):
    """
    Implements 0.DOIP/Op.Delete: An operation to allow a client to delete an (F)DO at a service. This operation just
    deletes the referenced (F)DO but not any other (F)DOs which are referenced by the given (F)DO.
    """
    try:
        response = delete(target_id, ip, port, username, client_id, password, token, key)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit() from error

    print_json_response(response)


@app.command(name='search')
def search_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying an (F)do')],
                   ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
                   port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
                   query: Annotated[
                       str, typer.Argument(help='The search query to be performed, in a textual representation')],
                   username: Annotated[
                       str, typer.Option(help='the username of the user at the data service')] = None,
                   client_id: Annotated[
                       str, typer.Option(help='the clientId of the user at the data service')] = None,
                   password: Annotated[
                       str, typer.Option(help='the password of the user at the data service')] = None,
                   token: Annotated[str, typer.Option(help='a token at the data service')] = None,
                   key: Annotated[str, typer.Option(help='a key at the data service')] = None):
    """Implements 0.DOIP/Op.Search"""
    try:
        response = search(target_id, ip, port, query, username, client_id, password, token, key)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit() from error

    print_json_response(response)


@app.command(name='add_metadata')
def add_metadata_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying a data service')],
                         ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
                         port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
                         metadata: Annotated[
                             Path, typer.Argument(
                                 help='Path to a JSON file which comprises the metadata to be added to the DO')],
                         update_if_exists: Annotated[
                             bool, typer.Option(
                                 help='How to handle values that should be added but already exist in the PID record. '
                                      'If True, then the value is updated with the new value. If False, an exception '
                                      'is raised')] = False,
                         username: Annotated[
                             str, typer.Option(help='the username of the user at the data service')] = None,
                         client_id: Annotated[
                             str, typer.Option(help='the clientId of the user at the data service')] = None,
                         password: Annotated[
                             str, typer.Option(help='the password of the user at the data service')] = None,
                         token: Annotated[str, typer.Option(help='a token at the data service')] = None,
                         key: Annotated[str, typer.Option(help='a key at the data service')] = None):
    """
    Implements 0.DOIP/Op.Update: In particular, values are added to the PID record of a DO.
    """

    # get the metadata that should be added and write them into a dictionary
    metadata_dict = None
    if metadata:
        try:
            with open(metadata) as f:
                metadata_dict = json.load(f)
        except json.JSONDecodeError as error:
            print('Invalid JSON syntax:', error)
            raise typer.Exit() from error
        except Exception as error:
            print(error)
            raise typer.Exit() from error

    try:
        response = add_metadata(target_id, ip, port, metadata_dict, update_if_exists, username, client_id, password,
                                token, key)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit() from error
    except KeyError as error:
        print(str(error))
        raise typer.Exit() from error
    except UnauthorizedException as error:
        print(str(error))
        raise typer.Exit() from error

    print_json_response(response)


@app.command(name='update_metadata')
def update_metadata_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying a data service')],
                            ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
                            port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
                            metadata: Annotated[
                                Path, typer.Argument(
                                    help='Path to a JSON file which comprises the metadata to be updated in the DO')],
                            add_if_not_exists: Annotated[
                                bool, typer.Option(
                                    help='How to handle values that should be updated but do not yet exist in the PID '
                                         'record. If True, then the value is added. If False, an exception is raised')]
                            = False,
                            username: Annotated[
                                str, typer.Option(help='the username of the user at the data service')] = None,
                            client_id: Annotated[
                                str, typer.Option(help='the clientId of the user at the data service')] = None,
                            password: Annotated[
                                str, typer.Option(help='the password of the user at the data service')] = None,
                            token: Annotated[str, typer.Option(help='a token at the data service')] = None,
                            key: Annotated[str, typer.Option(help='a key at the data service')] = None):
    """
    Implements 0.DOIP/Op.Update: In particular, values in the PID record of a DO are updated.
    """

    # get the metadata that should be added and write them into a dictionary
    metadata_dict = None
    if metadata:
        try:
            with open(metadata) as f:
                metadata_dict = json.load(f)
        except json.JSONDecodeError as error:
            print('Invalid JSON syntax:', error)
            raise typer.Exit() from error
        except Exception as error:
            print(error)
            raise typer.Exit() from error

    try:
        response = update_metadata(target_id, ip, port, metadata_dict, add_if_not_exists, username, client_id, password,
                                   token, key)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit() from error
    except KeyError as error:
        print(str(error))
        raise typer.Exit() from error
    except UnauthorizedException as error:
        print(str(error))
        raise typer.Exit() from error

    print_json_response(response)


@app.command(name='delete_metadata')
def delete_metadata_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying a data service')],
                            ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
                            port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
                            metadata: Annotated[
                                Path, typer.Argument(
                                    help='Path to a JSON file which comprises the metadata to be deleted from the DO')],
                            ignore_if_not_exists: Annotated[
                                bool, typer.Option(
                                    help='How to handle values that should be updated but do not yet exist in the PID '
                                         'record. If True, then the value is added. If False, an exception is raised')]
                            = False,
                            username: Annotated[
                                str, typer.Option(help='the username of the user at the data service')] = None,
                            client_id: Annotated[
                                str, typer.Option(help='the clientId of the user at the data service')] = None,
                            password: Annotated[
                                str, typer.Option(help='the password of the user at the data service')] = None,
                            token: Annotated[str, typer.Option(help='a token at the data service')] = None,
                            key: Annotated[str, typer.Option(help='a key at the data service')] = None):
    """
    Implements 0.DOIP/Op.Update: In particular, the given values are deleted from the PID record of a DO.
    """

    # get the metadata that should be added and write them into a dictionary
    metadata_dict = None
    if metadata:
        try:
            with open(metadata) as f:
                metadata_dict = json.load(f)
        except json.JSONDecodeError as error:
            print('Invalid JSON syntax:', error)
            raise typer.Exit() from error
        except Exception as error:
            print(error)
            raise typer.Exit() from error

    try:
        response = delete_metadata(target_id, ip, port, metadata_dict, ignore_if_not_exists, username, client_id,
                                   password, token, key)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit() from error
    except KeyError as error:
        print(str(error))
        raise typer.Exit() from error
    except UnauthorizedException as error:
        print(str(error))
        raise typer.Exit() from error

    print_json_response(response)


@app.command(name='update_all_metadata')
def update_all_metadata_command(
        target_id: Annotated[str, typer.Argument(help='the targetId identifying a data service')],
        ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
        port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
        metadata: Annotated[
            Path, typer.Argument(
                help='Path to a JSON file which comprises the metadata to be written into the PID record of the DO.')],
        username: Annotated[
            str, typer.Option(help='the username of the user at the data service')] = None,
        client_id: Annotated[
            str, typer.Option(help='the clientId of the user at the data service')] = None,
        password: Annotated[
            str, typer.Option(help='the password of the user at the data service')] = None,
        token: Annotated[str, typer.Option(help='a token at the data service')] = None,
        key: Annotated[str, typer.Option(help='a key at the data service')] = None):
    """
    Implements 0.DOIP/Op.Update: In particular, the given values overwrite the old values in the PID record of a DO.
    """

    # get the metadata that should be added and write them into a dictionary
    metadata_dict = None
    if metadata:
        try:
            with open(metadata) as f:
                metadata_dict = json.load(f)
        except json.JSONDecodeError as error:
            print('Invalid JSON syntax:', error)
            raise typer.Exit() from error
        except Exception as error:
            print(error)
            raise typer.Exit() from error

    try:
        response = update_all_metadata(target_id, ip, port, metadata_dict, username, client_id, password,
                                       token, key)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit() from error
    except UnauthorizedException as error:
        print(str(error))
        raise typer.Exit() from error

    print_json_response(response)


@app.command(name='update_bitsq')
def update_bitsq_command(
        target_id: Annotated[str, typer.Argument(help='the targetId identifying a data service')],
        ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
        port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
        bitsq: Annotated[
            Path, typer.Argument(help='Path to a file which comprises the data bit-sequence of the DO to be updated')],
        username: Annotated[
            str, typer.Option(help='the username of the user at the data service')] = None,
        client_id: Annotated[
            str, typer.Option(help='the clientId of the user at the data service')] = None,
        password: Annotated[
            str, typer.Option(help='the password of the user at the data service')] = None,
        token: Annotated[str, typer.Option(help='a token at the data service')] = None,
        key: Annotated[str, typer.Option(help='a key at the data service')] = None):
    """
    Implements 0.DOIP/Op.Update: In particular, the payload of the DO is overwritten by a new bit-sequence.
    """

    try:
        response = update_bitsq(target_id, ip, port, bitsq, username, client_id, password, token, key)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit() from error
    except KeyError as error:
        print(str(error))
        raise typer.Exit() from error

    print_json_response(response)


@app.command(name='delete_bitsq')
def delete_bitsq_command(
        target_id: Annotated[str, typer.Argument(help='the targetId identifying a digital object')],
        ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
        port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
        username: Annotated[
            str, typer.Option(help='the username of the user at the data service')] = None,
        client_id: Annotated[
            str, typer.Option(help='the clientId of the user at the data service')] = None,
        password: Annotated[
            str, typer.Option(help='the password of the user at the data service')] = None,
        token: Annotated[str, typer.Option(help='a token at the data service')] = None,
        key: Annotated[str, typer.Option(help='a key at the data service')] = None):
    """
    Implements 0.DOIP/Op.Update: In particular, the payload of the DO is deleted.
    """

    try:
        response = delete_bitsq(target_id, ip, port, username, client_id, password, token, key)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit() from error
    except KeyError as error:
        print(str(error))
        raise typer.Exit() from error

    print_json_response(response)


@app.command(name='add_bitsq')
def add_bitsq_command(
        target_id: Annotated[str, typer.Argument(help='the targetId identifying a digital object')],
        ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
        port: Annotated[int, typer.Argument(help='the DOIP port of the data service')],
        bitsq: Annotated[
            Path, typer.Argument(help='Path to a file which contains the data bit-sequence to be added to the DO')],
        username: Annotated[
            str, typer.Option(help='the username of the user at the data service')] = None,
        client_id: Annotated[
            str, typer.Option(help='the clientId of the user at the data service')] = None,
        password: Annotated[
            str, typer.Option(help='the password of the user at the data service')] = None,
        token: Annotated[str, typer.Option(help='a token at the data service')] = None,
        key: Annotated[str, typer.Option(help='a key at the data service')] = None):
    """
    Implements 0.DOIP/Op.Update: In particular, add a bit-sequence to a DO which does not have a bit-sequence yet.
    """

    try:
        response = add_bitsq(target_id, ip, port, bitsq, username, client_id, password, token, key)
    except AuthenticationException as error:
        print(str(error))
        raise typer.Exit() from error
    except KeyError as error:
        print(str(error))
        raise typer.Exit() from error

    print_json_response(response)


@app.command(name='create_fdo')
def create_fdo_command(
        input_file: Annotated[Path, typer.Argument(help='A file containing a JSON which follows a specific '
                                                        'JSON schema. The file contains data bit-sequences, '
                                                        'metadata bit-sequences and the metadata that should '
                                                        'be written into the corresponding PID records.')]):
    """
    Create a FAIR Digital Object (FDO).
    """
    # read the user input
    try:
        with open(input_file) as f:
            user_input = json.load(f)
    except json.JSONDecodeError as error:
        print("Invalid JSON syntax:", error)
        raise typer.Exit() from error
    except Exception as error:
        print(error)
        raise typer.Exit() from error

    # Create the FDO
    try:
        response = create_fdo(user_input)
    #  catch the following exceptions:
    # - a HTTP error occurs during API usage
    # - the input does not validate against the schema
    # - the chosen operation is not supported by the profile
    # - authentication fails
    # - the chosen profile is not supported
    except (requests.exceptions.RequestException, InputValidationError, ValidationError, OperationNotSupportedException,
            AuthenticationException, ProfileNotSupportedException, FileNotFoundError) as error:
        print(str(error))
        raise typer.Exit() from error
    # in case that the DOIP response is not success, raise an exception and terminate the program
    except InvalidRequestException as error:
        details = error.args[0][0]
        print(f'{details["status"]} {ResponseStatus(details["status"]).name}')
        print(details['output']['message'])
        raise typer.Exit() from error

    print(response)


@app.command(name='delete_fdo')
def delete_fdo_command(
        input_file: Annotated[Path, typer.Argument(help='A file containing a JSON which follows a specific '
                                                        'JSON schema. The file contains all arguments necessary to '
                                                        'delete an FDO.')]):
    """
    Delete a FAIR Digital Object (FDO).
    """
    # read the user input
    try:
        with open(input_file) as f:
            user_input = json.load(f)
    except json.JSONDecodeError as error:
        print("Invalid JSON syntax:", error)
        raise typer.Exit() from error
    except Exception as error:
        print(error)
        raise typer.Exit() from error

    try:
        result = delete_fdo(user_input)
    except (requests.exceptions.RequestException, InputValidationError, HandleValueNotFoundException,
            HandleNotFoundException, UnexpectedError, OperationNotSupportedException, ProfileNotSupportedException,
            InvalidOperationError) as error:
        print(error)
        raise typer.Exit() from error

    print(result)


@app.command(name='get_doip_connection')
def get_doip_connection_command(service: Annotated[str, typer.Argument(help='the PID identifying a data service')]):
    """
    Implements 0.DOIP/Op.Hello: An operation to allow a client to get information about the DOIP service.
    """
    try:
        ip, port = get_doip_connection(service)
        print(f'IP: {ip}')
        print(f'Port: {port}')
    except Exception as error:
        print(f'Error: {error}')
        raise typer.Exit() from error


@app.command(name='get_http_connection')
def get_http_connection_command(service: Annotated[str, typer.Argument(help='the PID identifying a data service')]):
    """
    Implements 0.DOIP/Op.Hello: An operation to allow a client to get information about the DOIP service.
    """
    try:
        ip, port = get_http_connection(service)
        print(f'IP: {ip}')
        print(f'Port: {port}')
    except Exception as error:
        print(f'Error: {error}')
        raise typer.Exit() from error


@app.command(name='get_design')
def get_design_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying a digital object')],
                       ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
                       port: Annotated[int, typer.Argument(help='the DOIP port of the data service')]):
    """Implements 20.DOIP/Op.GetDesign (see https://www.cordra.org)"""
    response = get_design(target_id, ip, port)
    print_json_response(response)


@app.command(name='get_init_data')
def get_init_data_command(target_id: Annotated[str, typer.Argument(help='the targetId identifying a digital object')],
                          ip: Annotated[str, typer.Argument(help='the IP address identifying a data service')],
                          port: Annotated[int, typer.Argument(help='the DOIP port of the data service')]):
    """Implements 20.DOIP/Op.GetInitData (see https://www.cordra.org)"""
    response = get_init_data(target_id, ip, port)
    print_json_response(response)


@app.command(name='move_fdo')
def move_fdo_command(
        input_file: Annotated[Path, typer.Argument(help='A file containing a JSON which follows a specific '
                                                        'JSON schema. The file contains all arguments necessary to '
                                                        'move an FDO to another repository.')]):
    """
    Delete a FAIR Digital Object (FDO).
    """
    # read the user input
    try:
        with open(input_file) as f:
            user_input = json.load(f)
    except json.JSONDecodeError as error:
        print("Invalid JSON syntax:", error)
        raise typer.Exit() from error

    try:
        result = move_fdo(user_input)
    except (requests.exceptions.RequestException, InputValidationError, HandleValueNotFoundException,
            HandleNotFoundException, UnexpectedError, OperationNotSupportedException, ProfileNotSupportedException,
            InvalidOperationError, KeyError) as error:
        print(error)
        raise typer.Exit() from error

    print(result)
