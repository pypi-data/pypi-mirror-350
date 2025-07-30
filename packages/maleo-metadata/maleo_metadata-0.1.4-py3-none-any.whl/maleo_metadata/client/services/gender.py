from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer
from maleo_foundation.enums import BaseEnums
from maleo_foundation.managers.cache.base import BaseCacheConfigurations
from maleo_foundation.managers.client.maleo import MaleoClientService
from maleo_foundation.utils.client import BaseClientUtils
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.client.controllers import MaleoMetadataGenderControllers
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.models.transfers.parameters.general.gender \
    import MaleoMetadataGenderGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.gender \
    import MaleoMetadataGenderClientParametersTransfers
from maleo_metadata.models.transfers.results.client.gender \
    import MaleoMetadataGenderClientResultsTransfers
from maleo_metadata.types.results.client.gender \
    import MaleoMetadataGenderClientResultsTypes

class MaleoMetadataGenderClientService(MaleoClientService):
    def __init__(
        self,
        key,
        logger,
        service_manager,
        controllers:MaleoMetadataGenderControllers
    ):
        super().__init__(key, logger, service_manager)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoMetadataGenderControllers:
        raise self._controllers

    async def get_genders(
        self,
        parameters:MaleoMetadataGenderClientParametersTransfers.GetMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataGenderClientResultsTypes.GetMultiple:
        """Retrieve genders from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving genders",
            logger=self._logger,
            fail_result_class=MaleoMetadataGenderClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoMetadataGenderClientResultsTransfers.Fail,
            data_found_class=MaleoMetadataGenderClientResultsTransfers.MultipleData,
            no_data_class=MaleoMetadataGenderClientResultsTransfers.NoData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_1WK),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "gender",
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
            parameters:MaleoMetadataGenderClientParametersTransfers.GetMultiple,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataGenderClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve genders using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_genders(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataGenderClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataGenderClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                if controller_result.content["data"] is None:
                    return (
                        MaleoMetadataGenderClientResultsTransfers
                        .NoData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
                else:
                    return (
                        MaleoMetadataGenderClientResultsTransfers
                        .MultipleData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_gender(
        self,
        parameters:MaleoMetadataGenderGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataGenderClientResultsTypes.GetSingle:
        """Retrieve gender from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving gender",
            logger=self._logger,
            fail_result_class=MaleoMetadataGenderClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoMetadataGenderClientResultsTransfers.Fail,
            data_found_class=MaleoMetadataGenderClientResultsTransfers.SingleData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_1WK),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "gender",
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
            parameters:MaleoMetadataGenderGeneralParametersTransfers.GetSingle,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataGenderClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve gender using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_gender(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataGenderClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataGenderClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                return (
                    MaleoMetadataGenderClientResultsTransfers
                    .SingleData
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )