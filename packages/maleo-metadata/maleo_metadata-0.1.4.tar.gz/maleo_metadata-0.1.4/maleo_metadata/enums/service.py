from enum import StrEnum

class MaleoMetadataServiceEnums:
    class IdentifierType(StrEnum):
        ID = "id"
        UUID = "uuid"
        KEY = "key"
        NAME = "name"

    class Service(StrEnum):
        MALEO_STUDIO = "maleo-studio"
        MALEO_METADATA = "maleo-metadata"
        MALEO_IDENTITY = "maleo-identity"