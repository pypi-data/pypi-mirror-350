from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer
from maleo_foundation.enums import BaseEnums
from maleo_foundation.managers.cache.base import BaseCacheConfigurations
from maleo_foundation.managers.client.maleo import MaleoClientService
from maleo_foundation.utils.client import BaseClientUtils
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_identity.client.controllers import MaleoIdentityUserControllers
from maleo_identity.enums.general import MaleoIdentityGeneralEnums
from maleo_identity.models.transfers.parameters.general.user \
    import MaleoIdentityUserGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.general.user_organization \
    import MaleoIdentityUserOrganizationGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.general.user_system_role \
    import MaleoIdentityUserSystemRoleGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.general.user_organization_role \
    import MaleoIdentityUserOrganizationRoleGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.client.user \
    import MaleoIdentityUserClientParametersTransfers
from maleo_identity.models.transfers.parameters.client.user_organization \
    import MaleoIdentityUserOrganizationClientParametersTransfers
from maleo_identity.models.transfers.parameters.client.user_system_role \
    import MaleoIdentityUserSystemRoleClientParametersTransfers
from maleo_identity.models.transfers.parameters.client.user_organization_role \
    import MaleoIdentityUserOrganizationRoleClientParametersTransfers
from maleo_identity.models.transfers.results.client.user \
    import MaleoIdentityUserClientResultsTransfers
from maleo_identity.models.transfers.results.client.user_organization \
    import MaleoIdentityUserOrganizationClientResultsTransfers
from maleo_identity.models.transfers.results.client.user_system_role \
    import MaleoIdentityUserSystemRoleClientResultsTransfers
from maleo_identity.models.transfers.results.client.user_organization_role \
    import MaleoIdentityUserOrganizationRoleClientResultsTransfers
from maleo_identity.types.results.client.user \
    import MaleoIdentityUserClientResultsTypes
from maleo_identity.types.results.client.user_organization \
    import MaleoIdentityUserOrganizationClientResultsTypes
from maleo_identity.types.results.client.user_system_role \
    import MaleoIdentityUserSystemRoleClientResultsTypes
from maleo_identity.types.results.client.user_organization_role \
    import MaleoIdentityUserOrganizationRoleClientResultsTypes

class MaleoIdentityUserClientService(MaleoClientService):
    def __init__(
        self,
        key,
        logger,
        service_manager,
        controllers:MaleoIdentityUserControllers
    ):
        super().__init__(key, logger, service_manager)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoIdentityUserControllers:
        raise self._controllers

    async def get_users(
        self,
        parameters:MaleoIdentityUserClientParametersTransfers.GetMultiple,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserClientResultsTypes.GetMultiple:
        """Retrieve users from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving users",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoIdentityUserClientResultsTransfers.Fail,
            data_found_class=MaleoIdentityUserClientResultsTransfers.MultipleData,
            no_data_class=MaleoIdentityUserClientResultsTransfers.NoData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_30MN),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "user",
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
            parameters:MaleoIdentityUserClientParametersTransfers.GetMultiple,
            controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoIdentityGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve users using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_users(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoIdentityUserClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                if controller_result.content["data"] is None:
                    return (
                        MaleoIdentityUserClientResultsTransfers
                        .NoData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
                else:
                    return (
                        MaleoIdentityUserClientResultsTransfers
                        .MultipleData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_user(
        self,
        parameters:MaleoIdentityUserGeneralParametersTransfers.GetSingle,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserClientResultsTypes.GetSingle:
        """Retrieve user from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoIdentityUserClientResultsTransfers.Fail,
            data_found_class=MaleoIdentityUserClientResultsTransfers.SingleData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_30MN),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "user",
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
            parameters:MaleoIdentityUserGeneralParametersTransfers.GetSingle,
            controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoIdentityGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve user using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_user(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoIdentityUserClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                return (
                    MaleoIdentityUserClientResultsTransfers
                    .SingleData
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def create(
        self,
        parameters:MaleoIdentityUserGeneralParametersTransfers.Create,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserClientResultsTypes.CreateOrUpdate:
        """Create a new user in MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="creating a new user",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserClientResultsTransfers.Fail
        )
        async def _impl(
            parameters:MaleoIdentityUserGeneralParametersTransfers.Create,
            controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoIdentityGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Create a new user using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .create(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoIdentityUserClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                )
            else:
                return (
                    MaleoIdentityUserClientResultsTransfers
                    .SingleData
                    .model_validate(controller_result.content)
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def update(
        self,
        parameters:MaleoIdentityUserGeneralParametersTransfers.Update,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserClientResultsTypes.CreateOrUpdate:
        """Update user's data in MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="updating user's data",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserClientResultsTransfers.Fail
        )
        async def _impl(
            parameters:MaleoIdentityUserGeneralParametersTransfers.Update,
            controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoIdentityGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Update user's data using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .update(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoIdentityUserClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                )
            else:
                return (
                    MaleoIdentityUserClientResultsTransfers
                    .SingleData
                    .model_validate(controller_result.content)
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_password(
        self,
        parameters:MaleoIdentityUserGeneralParametersTransfers.GetSinglePassword,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserClientResultsTypes.GetSinglePassword:
        """Retrieve user's password from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user's password",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoIdentityUserClientResultsTransfers.Fail,
            data_found_class=MaleoIdentityUserClientResultsTransfers.SinglePassword
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_30MN),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "user",
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
            parameters:MaleoIdentityUserGeneralParametersTransfers.GetSinglePassword,
            controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoIdentityGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve user's password using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_password(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoIdentityUserClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                return (
                    MaleoIdentityUserClientResultsTransfers
                    .SinglePassword
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_user_organizations(
        self,
        parameters:MaleoIdentityUserOrganizationClientParametersTransfers.GetMultipleFromUser,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserOrganizationClientResultsTypes.GetMultiple:
        """Retrieve user's organizations from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user's organizations",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserOrganizationClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoIdentityUserOrganizationClientResultsTransfers.Fail,
            data_found_class=MaleoIdentityUserOrganizationClientResultsTransfers.MultipleData,
            no_data_class=MaleoIdentityUserOrganizationClientResultsTransfers.NoData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_30MN),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "user_organization",
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
            parameters:MaleoIdentityUserOrganizationClientParametersTransfers.GetMultipleFromUser,
            controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoIdentityGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserOrganizationClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve user's organizations using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_user_organizations(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserOrganizationClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoIdentityUserOrganizationClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                if controller_result.content["data"] is None:
                    return (
                        MaleoIdentityUserOrganizationClientResultsTransfers
                        .NoData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
                else:
                    return (
                        MaleoIdentityUserOrganizationClientResultsTransfers
                        .MultipleData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_user_organization(
        self,
        parameters:MaleoIdentityUserOrganizationGeneralParametersTransfers.GetSingle,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserOrganizationClientResultsTypes.GetSingle:
        """Retrieve user's organization from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user's organization",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserOrganizationClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoIdentityUserOrganizationClientResultsTransfers.Fail,
            data_found_class=MaleoIdentityUserOrganizationClientResultsTransfers.SingleData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_30MN),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "user_organization",
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
            parameters:MaleoIdentityUserOrganizationGeneralParametersTransfers.GetSingle,
            controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoIdentityGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserOrganizationClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve user's organization using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_user_organization(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserOrganizationClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoIdentityUserOrganizationClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                return (
                    MaleoIdentityUserOrganizationClientResultsTransfers
                    .SingleData
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_user_system_roles(
        self,
        parameters:MaleoIdentityUserSystemRoleClientParametersTransfers.GetMultipleFromUser,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserSystemRoleClientResultsTypes.GetMultiple:
        """Retrieve user's system roles from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user's system roles",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserSystemRoleClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoIdentityUserSystemRoleClientResultsTransfers.Fail,
            data_found_class=MaleoIdentityUserSystemRoleClientResultsTransfers.MultipleData,
            no_data_class=MaleoIdentityUserSystemRoleClientResultsTransfers.NoData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_30MN),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "user_system_role",
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
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoIdentityGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserSystemRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve user's system roles using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_user_system_roles(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserSystemRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoIdentityUserSystemRoleClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                if controller_result.content["data"] is None:
                    return (
                        MaleoIdentityUserSystemRoleClientResultsTransfers
                        .NoData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
                else:
                    return (
                        MaleoIdentityUserSystemRoleClientResultsTransfers
                        .MultipleData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_user_system_role(
        self,
        parameters:MaleoIdentityUserSystemRoleGeneralParametersTransfers.GetSingle,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserSystemRoleClientResultsTypes.GetSingle:
        """Retrieve user's system role from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user's system role",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserSystemRoleClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoIdentityUserSystemRoleClientResultsTransfers.Fail,
            data_found_class=MaleoIdentityUserSystemRoleClientResultsTransfers.SingleData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_30MN),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "user_system_role",
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
            parameters:MaleoIdentityUserSystemRoleClientParametersTransfers.GetMultipleFromUser,
            controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserSystemRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve user's system role using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_user_system_role(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserSystemRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoIdentityUserSystemRoleClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                return (
                    MaleoIdentityUserSystemRoleClientResultsTransfers
                    .SingleData
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_user_organization_roles(
        self,
        parameters:MaleoIdentityUserOrganizationRoleClientParametersTransfers.GetMultipleFromUserOrOrganization,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserOrganizationRoleClientResultsTypes.GetMultiple:
        """Retrieve user's organization roles from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user's organization roles",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserOrganizationRoleClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoIdentityUserOrganizationRoleClientResultsTransfers.Fail,
            data_found_class=MaleoIdentityUserOrganizationRoleClientResultsTransfers.MultipleData,
            no_data_class=MaleoIdentityUserOrganizationRoleClientResultsTransfers.NoData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_30MN),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "user_organization_role",
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
            parameters:MaleoIdentityUserOrganizationRoleClientParametersTransfers.GetMultipleFromUserOrOrganization,
            controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoIdentityGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserOrganizationRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve user's organization roles using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_user_organization_roles(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserOrganizationRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoIdentityUserOrganizationRoleClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                if controller_result.content["data"] is None:
                    return (
                        MaleoIdentityUserOrganizationRoleClientResultsTransfers
                        .NoData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
                else:
                    return (
                        MaleoIdentityUserOrganizationRoleClientResultsTransfers
                        .MultipleData
                        .model_validate(controller_result.content)
                        .model_dump(mode="json")
                    )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )

    async def get_user_organization_role(
        self,
        parameters:MaleoIdentityUserOrganizationRoleGeneralParametersTransfers.GetSingle,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserOrganizationRoleClientResultsTypes.GetSingle:
        """Retrieve user's organization role from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user's organization role",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserOrganizationRoleClientResultsTransfers.Fail
        )
        @BaseClientUtils.result_processor(
            fail_class=MaleoIdentityUserOrganizationRoleClientResultsTransfers.Fail,
            data_found_class=MaleoIdentityUserOrganizationRoleClientResultsTransfers.SingleData
        )
        @cached(
            ttl=int(BaseEnums.CacheTTL.TTL_30MN),
            namespace=self.service_manager.configs.cache.redis.namespaces.create(
                "user_organization_role",
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
            parameters:MaleoIdentityUserOrganizationRoleGeneralParametersTransfers.GetSingle,
            controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
        ):
            #* Validate chosen controller type
            if not isinstance(
                controller_type,
                MaleoIdentityGeneralEnums.ClientControllerType
            ):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserOrganizationRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Retrieve user's organization role using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = (
                    await self._controllers.http
                    .get_user_organization_role(parameters=parameters)
                )
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserOrganizationRoleClientResultsTransfers.Fail(
                    message=message,
                    description=description
                )
            #* Return proper response
            if not controller_result.success:
                return (
                    MaleoIdentityUserOrganizationRoleClientResultsTransfers
                    .Fail
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
            else:
                return (
                    MaleoIdentityUserOrganizationRoleClientResultsTransfers
                    .SingleData
                    .model_validate(controller_result.content)
                    .model_dump(mode="json")
                )
        return await _impl(
            parameters=parameters,
            controller_type=controller_type
        )