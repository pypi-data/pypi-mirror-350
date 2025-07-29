from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer
from maleo_foundation.enums import BaseEnums
from maleo_foundation.managers.cache.base import BaseCacheConfigurations
from maleo_foundation.managers.client.maleo import MaleoClientService
from maleo_foundation.utils.client import BaseClientUtils
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.client.controllers import MaleoMetadataOrganizationTypeControllers
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.models.transfers.parameters.general.organization_type \
    import MaleoMetadataOrganizationTypeGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.organization_type \
    import MaleoMetadataOrganizationTypeClientParametersTransfers
from maleo_metadata.models.transfers.results.client.organization_type \
    import MaleoMetadataOrganizationTypeClientResultsTransfers
from maleo_metadata.types.results.client.organization_type \
    import MaleoMetadataOrganizationTypeClientResultsTypes

class MaleoMetadataOrganizationTypeClientService(MaleoClientService):
    def __init__(
        self,
        key,
        logger,
        service_manager,
        controllers:MaleoMetadataOrganizationTypeControllers
    ):
        super().__init__(key, logger, service_manager)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoMetadataOrganizationTypeControllers:
        raise self._controllers

    async def get_organization_types(
        self,
        parameters:MaleoMetadataOrganizationTypeClientParametersTransfers.GetMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataOrganizationTypeClientResultsTypes.GetMultiple:
        """Retrieve organization types from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving organization types",
            logger=self._logger,
            fail_result_class=MaleoMetadataOrganizationTypeClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoMetadataOrganizationTypeClientResultsTransfers.Fail,
            data_found_class=MaleoMetadataOrganizationTypeClientResultsTransfers.MultipleData,
            no_data_class=MaleoMetadataOrganizationTypeClientResultsTransfers.NoData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_1WK),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "organization_type",
                type=BaseEnums.CacheType.CLIENT,
                base_override=self.key
            ),
            key_builder=BaseCacheConfigurations.key_builder,
            skip_cache_func=lambda x: (
                self.service_manager.settings.ENVIRONMENT == BaseEnums.EnvironmentType.LOCAL
                or x is None
                or (
                    isinstance(x, dict)
                    and (
                        x.get("success") in [False, None]
                        or (x.get("success") is True and x.get("data") is None)
                    )
                )
            ),
            cache=Cache.REDIS,
            serializer=JsonSerializer(),
            endpoint=self.service_manager.configs.cache.redis.host,
            port=self.service_manager.configs.cache.redis.port,
            password=self.service_manager.configs.cache.redis.password,
            db=self.service_manager.configs.cache.redis.db
        )
        async def _impl(
            parameters:MaleoMetadataOrganizationTypeClientParametersTransfers.GetMultiple,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataOrganizationTypeClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve organization types using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_organization_types(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataOrganizationTypeClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataOrganizationTypeClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                if controller_result.content["data"] is None:
                    return (
                        MaleoMetadataOrganizationTypeClientResultsTransfers
                        .NoData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
                else:
                    return (
                        MaleoMetadataOrganizationTypeClientResultsTransfers
                        .MultipleData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_organization_type(
        self,
        parameters:MaleoMetadataOrganizationTypeGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataOrganizationTypeClientResultsTypes.GetSingle:
        """Retrieve organization type from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving organization type",
            logger=self._logger,
            fail_result_class=MaleoMetadataOrganizationTypeClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoMetadataOrganizationTypeClientResultsTransfers.Fail,
            data_found_class=MaleoMetadataOrganizationTypeClientResultsTransfers.SingleData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_1WK),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "organization_type",
                type=BaseEnums.CacheType.CLIENT,
                base_override=self.key
            ),
            key_builder=BaseCacheConfigurations.key_builder,
            skip_cache_func=lambda x: (
                self.service_manager.settings.ENVIRONMENT == BaseEnums.EnvironmentType.LOCAL
                or x is None
                or (
                    isinstance(x, dict)
                    and (
                        x.get("success") in [False, None]
                        or (x.get("success") is True and x.get("data") is None)
                    )
                )
            ),
            cache=Cache.REDIS,
            serializer=JsonSerializer(),
            endpoint=self.service_manager.configs.cache.redis.host,
            port=self.service_manager.configs.cache.redis.port,
            password=self.service_manager.configs.cache.redis.password,
            db=self.service_manager.configs.cache.redis.db
        )
        async def _impl(
            parameters:MaleoMetadataOrganizationTypeGeneralParametersTransfers.GetSingle,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataOrganizationTypeClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve organization type using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_organization_type(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataOrganizationTypeClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataOrganizationTypeClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                return (
                    MaleoMetadataOrganizationTypeClientResultsTransfers
                    .SingleData
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )