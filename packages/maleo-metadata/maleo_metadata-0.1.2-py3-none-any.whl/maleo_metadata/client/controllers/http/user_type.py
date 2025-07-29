from maleo_foundation.managers.client.base import BearerAuth
from maleo_foundation.managers.client.maleo import MaleoClientHTTPController
from maleo_foundation.models.transfers.results.client.controllers.http \
    import BaseClientHTTPControllerResults
from maleo_metadata.models.transfers.parameters.general.user_type \
    import MaleoMetadataUserTypeGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.user_type \
    import MaleoMetadataUserTypeClientParametersTransfers

class MaleoMetadataUserTypeHTTPController(MaleoClientHTTPController):
    async def get_user_types(
        self,
        parameters:MaleoMetadataUserTypeClientParametersTransfers.GetMultiple
    ) -> BaseClientHTTPControllerResults:
        """Fetch user types from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/user-types/"

            #* Parse parameters to query params
            params = (
                MaleoMetadataUserTypeClientParametersTransfers
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

    async def get_user_type(
        self,
        parameters:MaleoMetadataUserTypeGeneralParametersTransfers.GetSingle
    ) -> BaseClientHTTPControllerResults:
        """Fetch user type from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/user-types/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = (
                MaleoMetadataUserTypeGeneralParametersTransfers
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