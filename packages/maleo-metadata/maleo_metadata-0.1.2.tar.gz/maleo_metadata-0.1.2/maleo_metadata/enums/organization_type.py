from enum import StrEnum

class MaleoMetadataOrganizationTypeEnums:
    class IdentifierType(StrEnum):
        ID = "id"
        UUID = "uuid"
        KEY = "key"
        NAME = "name"

    class OrganizationType(StrEnum):
        REGULAR = "regular"
        INTERNAL = "internal"
        CLIENT = "client"
        PARTNER = "partner"
        VENDOR = "vendor"
        GOVERNMENT = "government"