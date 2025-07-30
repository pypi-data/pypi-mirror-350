from __future__ import annotations
from maleo_foundation.managers.client.maleo import MaleoClientManager
from maleo_foundation.managers.service import ServiceManager
from maleo_identity.client.controllers.http.organization \
    import MaleoIdentityOrganizationHTTPController
from maleo_identity.client.controllers.http.user \
    import MaleoIdentityUserHTTPController
from maleo_identity.client.controllers import (
    MaleoIdentityOrganizationControllers,
    MaleoIdentityUserControllers,
    MaleoIdentityControllers
)
from maleo_identity.client.services import (
    MaleoIdentityOrganizationClientService,
    MaleoIdentityUserClientService,
    MaleoIdentityServices
)

class MaleoIdentityClientManager(MaleoClientManager):
    def __init__(self, service_manager:ServiceManager):
        key = service_manager.configs.client.maleo.identity.key
        name = service_manager.configs.client.maleo.identity.name
        url = service_manager.configs.client.maleo.identity.url
        super().__init__(key, name, url, service_manager)
        self._initialize_controllers()
        self._initialize_services()
        self._logger.info("Client manager initialized successfully")

    def _initialize_controllers(self):
        super()._initialize_controllers()
        #* Organization controllers
        organization_http_controller = MaleoIdentityOrganizationHTTPController(
            service_manager=self.service_manager,
            manager=self._controller_managers.http
        )
        organization_controllers = MaleoIdentityOrganizationControllers(
            http=organization_http_controller
        )
        #* User controllers
        user_http_controller = MaleoIdentityUserHTTPController(
            service_manager=self.service_manager,
            manager=self._controller_managers.http
        )
        user_controllers = MaleoIdentityUserControllers(
            http=user_http_controller
        )
        #* All controllers
        self._controllers = MaleoIdentityControllers(
            organization=organization_controllers,
            user=user_controllers
        )

    @property
    def controllers(self) -> MaleoIdentityControllers:
        return self._controllers

    def _initialize_services(self):
        super()._initialize_services()
        organization_service = MaleoIdentityOrganizationClientService(
            key=self._key,
            logger=self._logger,
            service_manager=self.service_manager,
            controllers=self._controllers.organization
        )
        user_service = MaleoIdentityUserClientService(
            key=self._key,
            logger=self._logger,
            service_manager=self.service_manager,
            controllers=self._controllers.user)
        self._services = MaleoIdentityServices(
            organization=organization_service,
            user=user_service
        )

    @property
    def services(self) -> MaleoIdentityServices:
        return self._services