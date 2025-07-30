# DOIPY

DOIPY is a Python wrapper for communication using the Digital Object Interface Protocol (DOIP) in its current
[specification v2.0](https://www.dona.net/sites/default/files/2018-11/DOIPv2Spec_1.pdf).

It supports three main functionalities:

1. Receive the IP and port of a DOIP service by supplying the service ID (see `get_connection`).
2. All basic DOIP operations to handle digital objects (DOs): `hello`, `list_operations`, `create`, `update`, `delete`,
   `retrieve`, and `search`. Extended operations implemented by specific repository software are and will be included in
   the future.
3. Some FDO-Manager functionality to handle FAIR digital objects (FDOs): Create or delete an FDO (
   see `create_fdo`, `delete_fdo`) that complies
   with configuration type 14, which is expressed by a combination of DOIP basic operations, validation steps and
   communication with the data type registry (DTR).

## Install

Simply run

```shell
$ pip install doipy
```

## Usage (Python Code)

To use the `doipy` package in the Python code simply import it and call the exposed methods. The package has several
methods. Please use `doipy --help` to list all available methods.

### 1. Get the IP and Port of a DOIP Service

The service ID is a handle which identifies a DOIP service. For example, `21.T11967/service` is the service ID
identifying the Cordra instance in the FDO One Testbed. Starting with the service ID, one receives the IP and port of
the DOIP service by applying the `get_doip_connection` function.

```python
from doipy import get_doip_connection

# get the IP and port of a DOIP service
ip, port = get_doip_connection('21.T11967/service')
```

### 2. Basic DOIP Operations

#### hello, list_operations, create, and search

To communicate with a DOIP service, one has to supply a target ID as well as the IP and port of the desired service. For
the operations `hello`, `create`, and `search`, the target ID is equal to the service ID. For `retrieve`, `delete`,
and `update`, the target ID corresponds to the PID of a DO. For `list_operations`, the target ID might be either a
service ID or a DO PID. Below is demonstrated how to apply operations where the service ID is required.

```python
from doipy import get_doip_connection, hello, list_operations, create, search
from pathlib import Path

# get the IP and port of a DOIP service
service_id = '21.T11967/service'
ip, port = get_doip_connection(service=service_id)

# say hello to the data service
response_hello = hello(target_id=service_id, ip=ip, port=port)

# list all available operations at the data service
response_list_operations = list_operations(target_id=service_id, ip=ip, port=port)

# create a DO at the data service
metadata = {'key1': 'value1', 'key2': 'value2'}
username = ''
password = ''
# possibilities for authentication: provide either (username, password) or (client_id, password) or (token). The 
# authentication credentials are the credentials to authenticate the user at the DOIP service.
response_create = create(target_id=service_id, ip=ip, port=port, do_type='Document', do_name='my-FDO', 
                         bitsq=Path('file.txt'), metadata=metadata, username=username, password=password)

# call the search operation
response_search = search(target_id=service_id, ip=ip, port=port, query='type:Document', username=username,
                         password=password)
```

#### list_operations, retrieve, and delete

For the operations `list_operations`, `retrieve`, and `delete`, the target ID corresponds to a PID identifying a DO. As
an example, we take the PID `21.T11967/35463c4d5e1cf0449a31` which identifies a DO at the Cordra instance of the FDO One
Testbed. To run those operations in the Python code, one can follow the lines below.

```python
from doipy import get_doip_connection, list_operations, retrieve, delete

# get the IP and port of a DOIP service
ip, port = get_doip_connection('21.T11967/service')

do = '21.T11967/35463c4d5e1cf0449a31'
username = ''
password = ''

# list all available operations on the given DO
response_list_operations = list_operations(target_id=do, ip=ip, port=port, username=username, password=password)

# retrieve a DO
response_retrieve = retrieve(target_id=do, ip=ip, port=port, username=username, password=password)

# download a bit-sequence of a DO. The file must be the id of the bit-sequence to be downloaded.
response_download = retrieve(target_id=do, ip=ip, file='031c09fd-d45d-48b0-acab-57ec049bb6c8', port=port,
                             username=username, password=password)

# delete a DO
response_delete = delete(target_id=do, ip=ip, port=port, username=username, password=password)
```

#### add_metadata, update_metadata, delete_metadata, and update_all_metadata

There are several operations available to update the metadata key-value pairs in a PID record of a DO. The functions
are: `add_metadata` to add some metadata to a PID record, `delete_metadata` to delete some metadata from a PID record,
`update_metadata` to update some already existing metadata, and `update_all_metadata` which overrides the current
metadata
by a completely new list of metadata. The target ID corresponds to the PID of the DO that should be updated. One can
follow the code lines below.

```python
from doipy import get_doip_connection, add_metadata, update_metadata, delete_metadata, update_all_metadata

# get the IP and port of a DOIP service
ip, port = get_doip_connection('21.T11967/service')

# choose a DO located at the given service, which can be updated with my username and password
do = ''
metadata = {'key1': 'value1', 'key2': 'value2'}
metadata_keys = ['key1', 'key2']
username = ''
password = ''

# add values to the metadata of the DO
response_add_metadata = add_metadata(target_id=do, ip=ip, port=port, metadata=metadata, username=username,
                                     password=password)

# update existing metadata of the DO
response_update_metadata = update_metadata(target_id=do, ip=ip, port=port, metadata=metadata, username=username,
                                           password=password)

# delete values from the metadata of the DO
response_delete_metadata = delete_metadata(target_id=do, ip=ip, port=port, metadata=metadata_keys, username=username,
                                           password=password)

# override the metadata of the DO by a new list of metadata
response_update_all_metadata = update_all_metadata(target_id=do, ip=ip, port=port, metadata=metadata, username=username,
                                                   password=password)
```

#### add_bitsq, update_bitsq, and delete_bitsq

There are also several operations available to update the (unique) bit-sequence of a DO. The functions are: `add_bitsq`
to add a bit-sequence to a DO which does not have any bit-sequence yet, `delete_bitsq` to delete an existing
bit-sequence from a DO, and `update_bitsq` to update the (unique) bit-sequence of a DO by a new bit-sequence. The target
ID corresponds to the PID of the DO that should be updated. One can follow the code lines below.

```python
from doipy import get_doip_connection, add_bitsq, update_bitsq, delete_bitsq
from pathlib import Path

# get the IP and port of a DOIP service
ip, port = get_doip_connection('21.T11967/service')

# choose a DO located at the given service, which does not have any bit-sequence yet and which can be updated with my 
# username and password
do = ''
username = ''
password = ''

# add values to the metadata of the DO
response_add_bitsq = add_bitsq(target_id=do, ip=ip, port=port, bitsq=Path('file1.txt'), username=username,
                               password=password)

# update existing metadata of the DO
response_update_bitsq = update_bitsq(target_id=do, ip=ip, port=port, bitsq=Path('file2.txt'), username=username,
                                     password=password)

# delete values from the metadata of the DO
response_delete_bitsq = delete_bitsq(target_id=do, ip=ip, port=port, username=username, password=password)
```

### 3. FDO Manager

#### create_fdo

To create an FDO in the Python code, one needs to supply a Python dictionary which follows the structure of the schema
defined at https://typeapi.lab.pidconsortium.net/v1/types/schema/21.T11969/6e36f6c0de5fcab4a425 as input to
`create_fdo`.

The `create_fdo` function supports FDOs following configuration type 14, i.e., which consist of multiple data DOs and
multiple metadata DOs.

Each item in `FDO_Data_and_Metadata` is a data bit-sequence `data_bitsq` and its corresponding metadata bit-sequence
`metadata_bitsq`. One DO is generated for the data bit-sequence and one DO is generated for the metadata bit-sequence.
The content of `data_values` is written into the PID record of the data DO. The content of `metadata_values` is written
into the PID record of the metadata DO.

Use `create_fdo` to register an FDO with specified (meta)data bit-sequences. If `create_fdo` is successful, the PID of
the new FDO is returned. If it is not successful, an error is returned.

```python
from doipy import create_fdo

user_input = {
    "FDO_Service_Ref": "21.T11969/01370800d56a0d897dc1",
    "FDO_Profile_Ref": "21.T11969/141bf451b18a79d0fe66",
    "FDO_Authentication": {
        "username": "",
        "password": ""
    },
    "FDO_Type_Ref": "21.1/thisIsAnFdoType",
    "FDO_Rights_Ref": "21.1/thisIsAnFdoRightsSpecification",
    "FDO_Genre_Ref": "21.1/thisIsAnFdoGenre",
    "FDO_Data_and_Metadata": [
        {
            "data_bitsq": "data_bitsq_1.txt",
            "data_values": "data_values_1.json",
            "metadata_bitsq": "metadata_bitsq_1.json",
            "metadata_values": "metadata_values_1.json"
        },
        {
            "data_bitsq": "data_bitsq_2.txt",
            "data_values": "data_values_2.json",
            "metadata_bitsq": "metadata_bitsq_2.json",
            "metadata_values": "metadata_values_2.json"
        }
    ]
}

# create an FDO
result_create_fdo = create_fdo(user_input)
```

#### delete_fdo

To delete an FDO that follows configuration type 14 in the Python code, one needs to supply a Python dictionary
following the structure of the schema defined at
https://typeapi.lab.pidconsortium.net/v1/types/schema/21.T11969/78a7b599f1f707830402 as input to
`delete_fdo`.

Deleting the FDO means to delete all data bit-sequences that belong to the FDO. Additionally, one can specify whether
also the metadata bit-sequences should be deleted (parameter: `delete_md`). The FDO_Status in the FDO record is set to
`deleted`. The DO_Status and Status_URL in all DOs whose bit-sequences are deleted are updated to `deleted` respectively
reference a tombstone URL.

If `delete_fdo` is successful, 1 is returned. If it is not successful, an error is returned.

```python
from doipy import delete_fdo

user_input = {
    "PID_FDO": "21.T11967/72c5e9b5843c7c8c0658",
    "FDO_Service_Ref": "21.T11969/01370800d56a0d897dc1",
    "delete_MD": True,
    "FDO_Authentication": {
        "username": "",
        "password": ""
    }
}

# create an FDO
result_delete_fdo = delete_fdo(user_input)
```

#### move_fdo (currently supported: move from Cordra to Cordra)

Using `move_fdo`, an FDO that follows configuration type 14 can be moved from a source repository R1 to a destination
repository R2. The operation requires that all DOs that form the FDO and the FDO record are initially placed in the same
source repository R1. Moving this FDO from R1 to R2 means:

- All DOs (i.e., data DOs and metadata DOs) are moved to R2 and receive new PIDs in R2.
- The FDO Record is moved to R2 and receives a new PID in R2. It will contain the new DO PIDs in FDO_Data_Ref and
  FDO_Metadata_Ref. Its FDO_Status is `moved`.
- All bit-sequences of the initial FDO are deleted. The FDO record of the initial FDO gets a HS_ALIAS which references
  the moved FDO in R2. All other metadata are removed from the initial FDO record.

To move an FDO from R1 to R2, one needs to supply a Python dictionary following the structure of the schema defined at
https://typeapi.lab.pidconsortium.net/v1/types/schema/21.T11969/4677eeaea2eb2a2c2704 as input to`move_fdo`.
If `move_fdo` is successful, the PID of the moved FDO is returned. If it is not successful, an error is returned.

```python
from doipy import move_fdo

user_input = {
    "PID_FDO": "",
    "FDO_Service_Ref_Source": "21.T11969/01370800d56a0d897dc1",
    "FDO_Authentication_Source": {
        "username": "",
        "password": ""
    },
    "FDO_Service_Ref_Destination": "21.T11969/01370800d56a0d897dc1",
    "FDO_Authentication_Destination": {
        "username": "",
        "password": ""
    }
}
# create an FDO
result_move_fdo = move_fdo(user_input)
```

### Authentication

If authentication credentials need to be provided, then the user has several options to authenticate:

1. `username` and `password`
2. `client_id` and `password`
3. `token`

Authentication credentials must be provided for the DOIP functions: `create`, `delete`, and `update`. Depending on
the rights for read access, authentication credentials might be necessary for `list_operations` of a DO, `retrieve`, and
`search` as well. Authentication credentials must be provided for the FDO-Manager functions: `create_fdo`. Note that not
all data services accept all three options of authentication credentials.

## Usage (Command Line Interface)

### 1. Get the IP and port of a DOIP service

Starting with the service ID, receive the IP and port of the DOIP service by applying the `get_doip_connection` function.

```shell
# get the IP and port of a DOIP service
$ doipy get_doip_connection '21.T11967/service'
```

### 2. Basic DOIP Operations

#### hello, list_operations, create, and search

We demonstrate how to apply operations `hello`, `list_operations`, `create`, and `search` on the DOIP service which is
identified by the service ID.
Additional to the service ID, IP and port, the `create` operation has more parameters: The `do_type` refers to the type
of the DO at the data service, which is `Document` in Cordra. `bitsq` is a path to a file which contains the data of the
DO. `metadata` is a path to a JSON file containing the metadata. The key-value pairs from the JSON file are written into
the handle record of the DO at generation. `username` and `password`are the authentication credentials of a user at
the data service.

```shell
# get information from the DOIP service
$ doipy hello '21.T11967/service' '141.5.106.77' 9000

# list all available operations at the DOIP service
$ doipy list_operations '21.T11967/service' '141.5.106.77' 9000

# create a DO at the DOIP service
$ doipy create '21.T11967/service' '141.5.106.77' 9000 --do-type 'Document' --do-name 'my_DO' --bitsq 'data.txt' --metadata 'metadata.json' --username '' --password ''

# search in the DOIP service for a DO (todo)
$ doipy search '21.T11967/service' '141.5.106.77' 9000 'type:Document' --username '' --password ''
```

#### list_operations, retrieve, and delete

Apply the functions `list_operations` , `retrieve`, and `delete` on the DO which is identified by the PID
`"21.T11967/35463c4d5e1cf0449a31`.

```shell
# List all available operations of a DO
$ doipy list_operations '21.T11967/35463c4d5e1cf0449a31' '141.5.106.77' 9000 --username '' --password ''

# retrieve a DO 
$ doipy retrieve '21.T11967/35463c4d5e1cf0449a31' '141.5.106.77' 9000 --username '' --password ''

# download a bit-sequence of a DO. The file must be the id of the bit-sequence to be downloaded.
$ doipy retrieve '21.T11967/35463c4d5e1cf0449a31' '141.5.106.77' 9000 --file '031c09fd-d45d-48b0-acab-57ec049bb6c8' --username '' --password ''

# delete a DO
$ doipy delete '21.T11967/35463c4d5e1cf0449a31' '141.5.106.77' 9000 --username '' --password ''
```

#### add_metadata, update_metadata, delete_metadata and update_all_metadata

To update the metadata in the PID record of a DO, apply the
functions `add_metadata`, `update_metadata`, `delete_metadata` and `update_all_metadata`. The new list of metadata shall
be supplied as a JSON file `metadata.json`.

```shell
# add values to the metadata of the DO
$ doipy add_metadata '21.T11967/35463c4d5e1cf0449a31' '141.5.106.77' 9000 'metadata.json' --username '' --password ''

# update existing metadata of the DO
$ doipy update_metadata '21.T11967/35463c4d5e1cf0449a31' '141.5.106.77' 9000 'metadata.json' --username '' --password ''

# delete values from the metadata of the DO
$ doipy delete_metadata '21.T11967/35463c4d5e1cf0449a31' '141.5.106.77' 9000 'metadata.json' --username '' --password ''

# override the metadata of the DO by a new list of metadata
$ doipy update_all_metadata '21.T11967/35463c4d5e1cf0449a31' '141.5.106.77' 9000 'metadata.json' --username '' --password ''
```

#### add_bitsq, update_bitsq, and delete_bitsq

To update the bit-sequence of a DO, apply the functions `add_bitsq`, `update_bitsq`, and `delete_bitsq`. The new
bit-sequence of the DO shall be supplied as a file `file.txt`.

```shell
# add values to the metadata of the DO
$ doipy add_bitsq '21.T11967/35463c4d5e1cf0449a31' '141.5.106.77' 9000 'file.txt' --username '' --password ''

# update existing metadata of the DO
$ doipy update_bitsq '21.T11967/35463c4d5e1cf0449a31' '141.5.106.77' 9000 'file.txt' --username '' --password ''

# delete values from the metadata of the DO
$ doipy delete_bitsq '21.T11967/35463c4d5e1cf0449a31' '141.5.106.77' 9000 --username '' --password ''
```

### 3. FDO Manager

#### create_fdo

To create an FDO on the CLI, first create a JSON file (called input.json), whose content follows
the schema defined at https://typeapi.lab.pidconsortium.net/v1/types/schema/21.T11969/6e36f6c0de5fcab4a425

An example JSON file could look like this:

```json
{
  "FDO_Service_Ref": "21.T11969/01370800d56a0d897dc1",
  "FDO_Profile_Ref": "21.T11969/141bf451b18a79d0fe66",
  "FDO_Authentication": {
    "username": "",
    "password": ""
  },
  "FDO_Type_Ref": "21.1/thisIsAnFdoType",
  "FDO_Rights_Ref": "21.1/thisIsAnFdoRightsSpecification",
  "FDO_Genre_Ref": "21.1/thisIsAnFdoGenre",
  "FDO_Data_and_Metadata": [
    {
      "data_bitsq": "data_bitsq_1.txt",
      "data_values": "data_values_1.json",
      "metadata_bitsq": "metadata_bitsq_1.json",
      "metadata_values": "metadata_values_1.json"
    },
    {
      "data_bitsq": "data_bitsq_2.txt",
      "data_values": "data_values_2.json",
      "metadata_bitsq": "metadata_bitsq_2.json",
      "metadata_values": "metadata_values_2.json"
    }
  ]
}
```

Use `create_fdo` to register an FDO with specified (meta)data bit-sequences:

```shell
$ doipy create_fdo input.json
```

#### delete_fdo

To delete an FDO on the CLI, first create a JSON file (called input.json), whose content follows
the schema defined at https://typeapi.lab.pidconsortium.net/v1/types/schema/21.T11969/78a7b599f1f707830402

An example JSON file could look like this:

```json
{
  "PID_FDO": "21.T11967/72c5e9b5843c7c8c0658",
  "FDO_Service_Ref": "21.T11969/01370800d56a0d897dc1",
  "delete_MD": true,
  "FDO_Authentication": {
    "username": "",
    "password": ""
  }
}
```

Use `delete_fdo` to delete an FDO that follows configuration type 14:

```shell
$ doipy delete_fdo input.json
```

#### move_fdo (currently supported: move from Cordra to Cordra)

To move an FDO from R1 to R2 on the CLI, first create a JSON file (called input.json), whose content follows
the schema defined at https://typeapi.lab.pidconsortium.net/v1/types/schema/21.T11969/4677eeaea2eb2a2c2704

An example JSON file could look like this:

```json
{
  "PID_FDO": "",
  "FDO_Service_Ref_Source": "21.T11969/01370800d56a0d897dc1",
  "FDO_Authentication_Source": {
    "username": "",
    "password": ""
  },
  "FDO_Service_Ref_Destination": "21.T11969/01370800d56a0d897dc1",
  "FDO_Authentication_Destination": {
    "username": "",
    "password": ""
  }
}
```

Use `move_fdo` to move an FDO that follows configuration type 14:

```shell
$ doipy move_fdo input.json
```

## For developer

The project is managed by [Poetry](https://python-poetry.org/). Therefore, make sure that Poetry is installed in your
system. Then run

```shell
$ poetry install
```

to install all dependencies. With this command, Poetry also installs the package in editable mode.
