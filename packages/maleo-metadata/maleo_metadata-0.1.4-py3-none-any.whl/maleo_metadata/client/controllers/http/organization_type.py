from maleo_foundation.managers.client.base import BearerAuth
from maleo_foundation.managers.client.maleo import MaleoClientHTTPController
from maleo_foundation.models.transfers.results.client.controllers.http \
    import BaseClientHTTPControllerResults
from maleo_metadata.models.transfers.parameters.general.organization_type \
    import MaleoMetadataOrganizationTypeGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.organization_type \
    import MaleoMetadataOrganizationTypeClientParametersTransfers

class MaleoMetadataOrganizationTypeHTTPController(MaleoClientHTTPController):
    async def get_organization_types(
        self,
        parameters:MaleoMetadataOrganizationTypeClientParametersTransfers.GetMultiple
    ) -> BaseClientHTTPControllerResults:
        """Fetch organization types from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organization-types/"

            #* Parse parameters to query params
            params = (
                MaleoMetadataOrganizationTypeClientParametersTransfers
                .GetMultipleQuery
                .model_validate(
                    parameters.model_dump()
                )
                .model_dump(
                    exclude={"sort_columns", "date_filters"},
                    exclude_none=True
                )
            )

            #* Create auth
            token = self._service_manager.token
            auth = BearerAuth(token=token) if token is not None else None

            #* Send request and wait for response
            response = await client.get(url=url, params=params, auth=auth)
            return BaseClientHTTPControllerResults(response=response)

    async def get_organization_type(self, parameters:MaleoMetadataOrganizationTypeGeneralParametersTransfers.GetSingle) -> BaseClientHTTPControllerResults:
        """Fetch organization type from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organization-types/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = (
                MaleoMetadataOrganizationTypeGeneralParametersTransfers
                .GetSingleQuery
                .model_validate(
                    parameters.model_dump()
                )
                .model_dump(exclude_none=True)
            )

            #* Create auth
            token = self._service_manager.token
            auth = BearerAuth(token=token) if token is not None else None

            #* Send request and wait for response
            response = await client.get(url=url, params=params, auth=auth)
            return BaseClientHTTPControllerResults(response=response)