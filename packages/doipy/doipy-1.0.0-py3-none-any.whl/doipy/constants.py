from enum import Enum


class CordraOperation(Enum):
    GET_DESIGN = '20.DOIP/Op.GetDesign'
    GET_INIT_DATA = '20.DOIP/Op.GetInitData'


class DOIPOperation(Enum):
    HELLO = '0.DOIP/Op.Hello'
    CREATE = '0.DOIP/Op.Create'
    RETRIEVE = '0.DOIP/Op.Retrieve'
    UPDATE = '0.DOIP/Op.Update'
    DELETE = '0.DOIP/Op.Delete'
    SEARCH = '0.DOIP/Op.Search'
    LIST_OPERATION = '0.DOIP/Op.ListOperations'


class ResponseStatus(Enum):
    SUCCESS = '0.DOIP/Status.001'
    INVALID = '0.DOIP/Status.101'
    UNAUTHENTICATED = '0.DOIP/Status.102'
    UNAUTHORIZED = '0.DOIP/Status.103'
    UNKNOWN_DO = '0.DOIP/Status.104'
    DUPLICATED_PID = '0.DOIP/Status.105'
    UNKNOWN_OPERATION = '0.DOIP/Status.200'
    UNKNOWN_ERROR = '0.DOIP/Status.500'


class FDOTypeIdentifier(Enum):
    FDO_PROFILE_REF = 'FDO_Profile_Ref'
    FDO_TYPE_REF = 'FDO_Type_Ref'
    FDO_STATUS = 'FDO_Status'
    FDO_RIGHTS_REF = 'FDO_Rights_Ref'
    FDO_GENRE_REF = 'FDO_Genre_Ref'
    FDO_DATA_REFS = 'FDO_Data_Refs'
    FDO_MD_REFS = 'FDO_MD_Refs'


class DOTypeIdentifier(Enum):
    DO_STATUS = 'DO_Status'
    STATUS_URL = 'Status_URL'


class ValidationSchemas(Enum):
    DATA_AND_METADATA = '21.T11969/27d8ca0c2585c0dafa39'


class DOType(Enum):
    DO = 'Document'
    FDO = 'FDO'


class DomainName(Enum):
    TYPE_API_SCHEMAS = 'https://typeapi.lab.pidconsortium.net/v1/types/schema'
    TYPE_REGISTRY_OBJECTS = 'https://typeregistry.lab.pidconsortium.net/objects'
    RESOLVE_PID = 'https://hdl.handle.net/api/handles'


class Profile(Enum):
    CONFIG_TYPE_14 = '21.T11969/141bf451b18a79d0fe66'
