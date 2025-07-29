from maleo_foundation.managers.client.base import BearerAuth
from maleo_foundation.managers.client.maleo import MaleoClientHTTPController
from maleo_foundation.models.transfers.results.client.controllers.http \
    import BaseClientHTTPControllerResults
from maleo_metadata.models.transfers.parameters.general.medical_role \
    import MaleoMetadataMedicalRoleGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.medical_role \
    import MaleoMetadataMedicalRoleClientParametersTransfers

class MaleoMetadataMedicalRoleHTTPController(MaleoClientHTTPController):
    async def get_medical_roles(
        self,
        parameters:MaleoMetadataMedicalRoleClientParametersTransfers.GetMultiple
    ) -> BaseClientHTTPControllerResults:
        """Fetch medical roles from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/medical-roles/"

            #* Parse parameters to query params
            params = (
                MaleoMetadataMedicalRoleClientParametersTransfers
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

    async def get_medical_roles_specializations(
        self,
        parameters:MaleoMetadataMedicalRoleClientParametersTransfers.GetMultipleRootSpecializations
    ) -> BaseClientHTTPControllerResults:
        """Fetch medical roles specializations from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/medical-roles/specializations"

            #* Parse parameters to query params
            params = (
                MaleoMetadataMedicalRoleClientParametersTransfers
                .GetMultipleSpecializationsQuery
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

    async def get_structured_medical_roles(
        self,
        parameters:MaleoMetadataMedicalRoleClientParametersTransfers.GetStructuredMultiple
    ) -> BaseClientHTTPControllerResults:
        """Fetch structured medical roles from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/medical-roles/structured"

            #* Parse parameters to query params
            params = (
                MaleoMetadataMedicalRoleClientParametersTransfers
                .GetStructuredMultipleQuery
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

    async def get_medical_role(
        self,
        parameters:MaleoMetadataMedicalRoleGeneralParametersTransfers.GetSingle
    ) -> BaseClientHTTPControllerResults:
        """Fetch medical role from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/medical-roles/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = (
                MaleoMetadataMedicalRoleGeneralParametersTransfers
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

    async def get_medical_role_specializations(
        self,
        parameters:MaleoMetadataMedicalRoleClientParametersTransfers.GetMultipleSpecializations
    ) -> BaseClientHTTPControllerResults:
        """Fetch medical role's specializations from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/medical-roles/{parameters.medical_role_id}/specializations"

            #* Parse parameters to query params
            params = (
                MaleoMetadataMedicalRoleClientParametersTransfers
                .GetMultipleSpecializationsQuery
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

    async def get_structured_medical_role(
        self,
        parameters:MaleoMetadataMedicalRoleGeneralParametersTransfers.GetSingle
    ) -> BaseClientHTTPControllerResults:
        """Fetch structured medical role from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/medical-roles/{parameters.identifier}/{parameters.value}/structured"

            #* Parse parameters to query params
            params = (
                MaleoMetadataMedicalRoleGeneralParametersTransfers
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