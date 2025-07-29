from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer
from maleo_foundation.enums import BaseEnums
from maleo_foundation.managers.cache.base import BaseCacheConfigurations
from maleo_foundation.managers.client.maleo import MaleoClientService
from maleo_foundation.utils.client import BaseClientUtils
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.client.controllers import MaleoMetadataServiceControllers
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.models.transfers.parameters.general.service \
    import MaleoMetadataServiceGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.service \
    import MaleoMetadataServiceClientParametersTransfers
from maleo_metadata.models.transfers.results.client.service \
    import MaleoMetadataServiceClientResultsTransfers
from maleo_metadata.types.results.client.service \
    import MaleoMetadataServiceClientResultsTypes

class MaleoMetadataServiceClientService(MaleoClientService):
    def __init__(
        self,
        key,
        logger,
        service_manager,
        controllers:MaleoMetadataServiceControllers
    ):
        super().__init__(key, logger, service_manager)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoMetadataServiceControllers:
        raise self._controllers

    async def get_services(
        self,
        parameters:MaleoMetadataServiceClientParametersTransfers.GetMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataServiceClientResultsTypes.GetMultiple:
        """Retrieve services from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving services",
            logger=self._logger,
            fail_result_class=MaleoMetadataServiceClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoMetadataServiceClientResultsTransfers.Fail,
            data_found_class=MaleoMetadataServiceClientResultsTransfers.MultipleData,
            no_data_class=MaleoMetadataServiceClientResultsTransfers.NoData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_1WK),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "service",
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
            parameters:MaleoMetadataServiceClientParametersTransfers.GetMultiple,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataServiceClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve services using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_services(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataServiceClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataServiceClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                if controller_result.content["data"] is None:
                    return (
                        MaleoMetadataServiceClientResultsTransfers
                        .NoData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
                else:
                    return (
                        MaleoMetadataServiceClientResultsTransfers
                        .MultipleData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_service(
        self,
        parameters:MaleoMetadataServiceGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataServiceClientResultsTypes.GetSingle:
        """Retrieve service from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving service",
            logger=self._logger,
            fail_result_class=MaleoMetadataServiceClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoMetadataServiceClientResultsTransfers.Fail,
            data_found_class=MaleoMetadataServiceClientResultsTransfers.SingleData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_1WK),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "service",
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
            parameters:MaleoMetadataServiceGeneralParametersTransfers.GetSingle,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataServiceClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve service using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_service(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataServiceClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataServiceClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                return (
                    MaleoMetadataServiceClientResultsTransfers
                    .SingleData
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )