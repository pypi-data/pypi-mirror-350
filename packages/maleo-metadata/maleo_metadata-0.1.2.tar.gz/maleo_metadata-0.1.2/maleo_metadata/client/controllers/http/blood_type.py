from maleo_foundation.managers.client.base import BearerAuth
from maleo_foundation.managers.client.maleo import MaleoClientHTTPController
from maleo_foundation.models.transfers.results.client.controllers.http \
    import BaseClientHTTPControllerResults
from maleo_metadata.models.transfers.parameters.general.blood_type \
    import MaleoMetadataBloodTypeGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.blood_type \
    import MaleoMetadataBloodTypeClientParametersTransfers

class MaleoMetadataBloodTypeHTTPController(MaleoClientHTTPController):
    async def get_blood_types(
        self,
        parameters:MaleoMetadataBloodTypeClientParametersTransfers.GetMultiple
    ) -> BaseClientHTTPControllerResults:
        """Fetch blood types from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/blood-types/"

            #* Parse parameters to query params
            params = (
                MaleoMetadataBloodTypeClientParametersTransfers
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

    async def get_blood_type(
        self,
        parameters:MaleoMetadataBloodTypeGeneralParametersTransfers.GetSingle
    ) -> BaseClientHTTPControllerResults:
        """Fetch blood type from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/blood-types/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = (
                MaleoMetadataBloodTypeGeneralParametersTransfers
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