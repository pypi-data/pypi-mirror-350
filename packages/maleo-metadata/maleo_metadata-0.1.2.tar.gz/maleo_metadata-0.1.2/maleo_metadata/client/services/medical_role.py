from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer
from maleo_foundation.enums import BaseEnums
from maleo_foundation.managers.cache.base import BaseCacheConfigurations
from maleo_foundation.managers.client.maleo import MaleoClientService
from maleo_foundation.utils.client import BaseClientUtils
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.client.controllers import MaleoMetadataMedicalRoleHTTPControllers
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.models.transfers.parameters.general.medical_role \
    import MaleoMetadataMedicalRoleGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.medical_role \
    import MaleoMetadataMedicalRoleClientParametersTransfers
from maleo_metadata.models.transfers.results.client.medical_role \
    import MaleoMetadataMedicalRoleClientResultsTransfers
from maleo_metadata.types.results.client.medical_role \
    import MaleoMetadataMedicalRoleClientResultsTypes

class MaleoMetadataMedicalRoleClientService(MaleoClientService):
    def __init__(
        self,
        key,
        logger,
        service_manager,
        controllers:MaleoMetadataMedicalRoleHTTPControllers
    ):
        super().__init__(key, logger, service_manager)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoMetadataMedicalRoleHTTPControllers:
        raise self._controllers

    async def get_medical_roles(
        self,
        parameters:MaleoMetadataMedicalRoleClientParametersTransfers.GetMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataMedicalRoleClientResultsTypes.GetMultiple:
        """Retrieve medical roles from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving medical roles",
            logger=self._logger,
            fail_result_class=MaleoMetadataMedicalRoleClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoMetadataMedicalRoleClientResultsTransfers.Fail,
            data_found_class=MaleoMetadataMedicalRoleClientResultsTransfers.MultipleData,
            no_data_class=MaleoMetadataMedicalRoleClientResultsTransfers.NoData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_1WK),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "medical_role",
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
            parameters:MaleoMetadataMedicalRoleClientParametersTransfers.GetMultiple,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataMedicalRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve medical roles using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_medical_roles(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataMedicalRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataMedicalRoleClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                if controller_result.content["data"] is None:
                    return (
                        MaleoMetadataMedicalRoleClientResultsTransfers
                        .NoData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
                else:
                    return (
                        MaleoMetadataMedicalRoleClientResultsTransfers
                        .MultipleData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_medical_role_specializations(
        self,
        parameters:MaleoMetadataMedicalRoleClientParametersTransfers.GetMultipleRootSpecializations,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataMedicalRoleClientResultsTypes.GetMultiple:
        """Retrieve medical role specializations from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving medical role specializations",
            logger=self._logger,
            fail_result_class=MaleoMetadataMedicalRoleClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoMetadataMedicalRoleClientResultsTransfers.Fail,
            data_found_class=MaleoMetadataMedicalRoleClientResultsTransfers.MultipleData,
            no_data_class=MaleoMetadataMedicalRoleClientResultsTransfers.NoData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_1WK),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "medical_role",
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
            parameters:MaleoMetadataMedicalRoleClientParametersTransfers.GetMultipleRootSpecializations,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataMedicalRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve medical role specializations using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_medical_roles_specializations(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataMedicalRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataMedicalRoleClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                if controller_result.content["data"] is None:
                    return (
                        MaleoMetadataMedicalRoleClientResultsTransfers
                        .NoData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
                else:
                    return (
                        MaleoMetadataMedicalRoleClientResultsTransfers
                        .MultipleData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_structured_medical_roles(
        self,
        parameters:MaleoMetadataMedicalRoleClientParametersTransfers.GetStructuredMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataMedicalRoleClientResultsTypes.GetStructuredMultiple:
        """Retrieve structured medical roles from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving structured medical roles",
            logger=self._logger,
            fail_result_class=MaleoMetadataMedicalRoleClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoMetadataMedicalRoleClientResultsTransfers.Fail,
            data_found_class=MaleoMetadataMedicalRoleClientResultsTransfers.MultipleStructured,
            no_data_class=MaleoMetadataMedicalRoleClientResultsTransfers.NoData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_1WK),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "medical_role",
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
            parameters:MaleoMetadataMedicalRoleClientParametersTransfers.GetStructuredMultiple,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataMedicalRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve structured medical roles using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_structured_medical_roles(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataMedicalRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataMedicalRoleClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                if controller_result.content["data"] is None:
                    return (
                        MaleoMetadataMedicalRoleClientResultsTransfers
                        .NoData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
                else:
                    return (
                        MaleoMetadataMedicalRoleClientResultsTransfers
                        .MultipleStructured
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_medical_role(
        self,
        parameters:MaleoMetadataMedicalRoleGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataMedicalRoleClientResultsTypes.GetSingle:
        """Retrieve medical role from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving medical role",
            logger=self._logger,
            fail_result_class=MaleoMetadataMedicalRoleClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoMetadataMedicalRoleClientResultsTransfers.Fail,
            data_found_class=MaleoMetadataMedicalRoleClientResultsTransfers.SingleData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_1WK),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "medical_role",
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
            parameters:MaleoMetadataMedicalRoleGeneralParametersTransfers.GetSingle,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataMedicalRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve medical role using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_medical_role(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataMedicalRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataMedicalRoleClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                return (
                    MaleoMetadataMedicalRoleClientResultsTransfers
                    .SingleData
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_medical_role_specializations(
        self,
        parameters:MaleoMetadataMedicalRoleClientParametersTransfers.GetMultipleSpecializations,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataMedicalRoleClientResultsTypes.GetMultiple:
        """Retrieve medical role's specializations from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving medical role's specializations",
            logger=self._logger,
            fail_result_class=MaleoMetadataMedicalRoleClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoMetadataMedicalRoleClientResultsTransfers.Fail,
            data_found_class=MaleoMetadataMedicalRoleClientResultsTransfers.MultipleData,
            no_data_class=MaleoMetadataMedicalRoleClientResultsTransfers.NoData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_1WK),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "medical_role",
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
            parameters:MaleoMetadataMedicalRoleClientParametersTransfers.GetMultipleSpecializations,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataMedicalRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve medical role's specializations using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_medical_role_specializations(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataMedicalRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataMedicalRoleClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                if controller_result.content["data"] is None:
                    return (
                        MaleoMetadataMedicalRoleClientResultsTransfers
                        .NoData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
                else:
                    return (
                        MaleoMetadataMedicalRoleClientResultsTransfers
                        .MultipleData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_structured_medical_role(
        self,
        parameters:MaleoMetadataMedicalRoleGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataMedicalRoleClientResultsTypes.GetSingleStructured:
        """Retrieve structured medical role from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving structured medical role",
            logger=self._logger,
            fail_result_class=MaleoMetadataMedicalRoleClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoMetadataMedicalRoleClientResultsTransfers.Fail,
            data_found_class=MaleoMetadataMedicalRoleClientResultsTransfers.SingleStructured
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_1WK),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "medical_role",
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
            parameters:MaleoMetadataMedicalRoleGeneralParametersTransfers.GetSingle,
            controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoMetadataGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataMedicalRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve structured medical role using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_structured_medical_role(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataMedicalRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoMetadataMedicalRoleClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                return (
                    MaleoMetadataMedicalRoleClientResultsTransfers
                    .SingleStructured
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )