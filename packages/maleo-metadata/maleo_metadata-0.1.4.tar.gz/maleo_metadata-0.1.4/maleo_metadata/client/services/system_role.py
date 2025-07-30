from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer
from maleo_foundation.enums import BaseEnums
from maleo_foundation.managers.cache.base import BaseCacheConfigurations
from maleo_foundation.managers.client.maleo import MaleoClientService
from maleo_foundation.utils.client import BaseClientUtils
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.client.controllers import MaleoMetadataSystemRoleControllers
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.models.transfers.parameters.general.system_role \
    import MaleoMetadataSystemRoleGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.system_role \
    import MaleoMetadataSystemRoleClientParametersTransfers
from maleo_metadata.models.transfers.results.client.system_role \
    import MaleoMetadataSystemRoleClientResultsTransfers
from maleo_metadata.types.results.client.system_role \
    import MaleoMetadataSystemRoleClientResultsTypes

class MaleoMetadataSystemRoleClientService(MaleoClientService):
    def __init__(
        self,
        key,
        logger,
        service_manager,
        controllers:MaleoMetadataSystemRoleControllers
    ):
        super().__init__(key, logger, service_manager)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoMetadataSystemRoleControllers:
        raise self._controllers

    async def get_system_roles(
        self,
        parameters:MaleoMetadataSystemRoleClientParametersTransfers.GetMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataSystemRoleClientResultsTypes.GetMultiple:
        """Retrieve system roles from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving system roles",
            logger=self._logger,
            fail_result_class=MaleoMetadataSystemRoleClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoMetadataSystemRoleClientResultsTransfers.Fail,
            data_found_class=MaleoMetadataSystemRoleClientResultsTransfers.MultipleData,
            no_data_class=MaleoMetadataSystemRoleClientResultsTransfers.NoData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_1WK),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "system_role",
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
            parameters:MaleoMetadataSystemRoleClientParametersTransfers.GetMultiple,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataSystemRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve system roles using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_system_roles(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataSystemRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataSystemRoleClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                if controller_result.content["data"] is None:
                    return (
                        MaleoMetadataSystemRoleClientResultsTransfers
                        .NoData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
                else:
                    return (
                        MaleoMetadataSystemRoleClientResultsTransfers
                        .MultipleData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_system_role(
        self,
        parameters:MaleoMetadataSystemRoleGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataSystemRoleClientResultsTypes.GetSingle:
        """Retrieve system role from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving system role",
            logger=self._logger,
            fail_result_class=MaleoMetadataSystemRoleClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoMetadataSystemRoleClientResultsTransfers.Fail,
            data_found_class=MaleoMetadataSystemRoleClientResultsTransfers.SingleData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_1WK),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "system_role",
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
            parameters:MaleoMetadataSystemRoleGeneralParametersTransfers.GetSingle,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataSystemRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve system role using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_system_role(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataSystemRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataSystemRoleClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                return (
                    MaleoMetadataSystemRoleClientResultsTransfers
                    .SingleData
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )