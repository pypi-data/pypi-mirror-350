from maleo_foundation.managers.client.base import BearerAuth
from maleo_foundation.managers.client.maleo import MaleoClientHTTPController
from maleo_foundation.models.transfers.results.client.controllers.http \
    import BaseClientHTTPControllerResults
from maleo_metadata.models.transfers.parameters.general.system_role \
    import MaleoMetadataSystemRoleGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.system_role \
    import MaleoMetadataSystemRoleClientParametersTransfers

class MaleoMetadataSystemRoleHTTPController(MaleoClientHTTPController):
    async def get_system_roles(
        self,
        parameters:MaleoMetadataSystemRoleClientParametersTransfers.GetMultiple
    ) -> BaseClientHTTPControllerResults:
        """Fetch system roles from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/system-roles/"

            #* Parse parameters to query params
            params = (
                MaleoMetadataSystemRoleClientParametersTransfers
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

    async def get_system_role(
        self,
        parameters:MaleoMetadataSystemRoleGeneralParametersTransfers.GetSingle
    ) -> BaseClientHTTPControllerResults:
        """Fetch system role from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/system-roles/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = (
                MaleoMetadataSystemRoleGeneralParametersTransfers
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