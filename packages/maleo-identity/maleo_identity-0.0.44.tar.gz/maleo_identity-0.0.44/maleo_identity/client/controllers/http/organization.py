from maleo_foundation.managers.client.base import BearerAuth
from maleo_foundation.managers.client.maleo import MaleoClientHTTPController
from maleo_foundation.models.transfers.results.client.controllers.http \
    import BaseClientHTTPControllerResults
from maleo_identity.models.transfers.parameters.general.organization_role \
    import MaleoIdentityOrganizationRoleGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.general.organization \
    import MaleoIdentityOrganizationGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.general.user_organization \
    import MaleoIdentityUserOrganizationGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.general.user_organization_role \
    import MaleoIdentityUserOrganizationRoleGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.client.organization_role \
    import MaleoIdentityOrganizationRoleClientParametersTransfers
from maleo_identity.models.transfers.parameters.client.organization \
    import MaleoIdentityOrganizationClientParametersTransfers
from maleo_identity.models.transfers.parameters.client.user_organization \
    import MaleoIdentityUserOrganizationClientParametersTransfers
from maleo_identity.models.transfers.parameters.client.user_organization_role \
    import MaleoIdentityUserOrganizationRoleClientParametersTransfers

class MaleoIdentityOrganizationHTTPController(MaleoClientHTTPController):
    async def get_organizations(
        self,
        parameters:MaleoIdentityOrganizationClientParametersTransfers.GetMultiple
    ) -> BaseClientHTTPControllerResults:
        """Fetch organizations from MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/"

            #* Parse parameters to query params
            params = (
                MaleoIdentityOrganizationClientParametersTransfers
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

    async def get_structured_organizations(
        self,
        parameters:MaleoIdentityOrganizationClientParametersTransfers.GetMultipleStructured
    ) -> BaseClientHTTPControllerResults:
        """Fetch structured organizations from MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/structured"

            #* Parse parameters to query params
            params = (
                MaleoIdentityOrganizationClientParametersTransfers
                .GetMultipleStructuredQuery
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

    async def get_organization(
        self,
        parameters:MaleoIdentityOrganizationGeneralParametersTransfers.GetSingle
    ) -> BaseClientHTTPControllerResults:
        """Fetch organization from MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = (
                MaleoIdentityOrganizationGeneralParametersTransfers
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

    async def get_structured_organization(
        self,
        parameters:MaleoIdentityOrganizationGeneralParametersTransfers.GetSingle
    ) -> BaseClientHTTPControllerResults:
        """Fetch structured organization from MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/{parameters.identifier}/{parameters.value}/structured"

            #* Parse parameters to query params
            params = (
                MaleoIdentityOrganizationGeneralParametersTransfers
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

    async def get_organization_children(
        self,
        parameters:MaleoIdentityOrganizationClientParametersTransfers.GetMultipleChildren
    ) -> BaseClientHTTPControllerResults:
        """Fetch organization's children from MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/{parameters.organization_id}/children"

            #* Parse parameters to query params
            params = (
                MaleoIdentityOrganizationClientParametersTransfers
                .GetMultipleChildrenQuery
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

    async def create(
        self,
        parameters:MaleoIdentityOrganizationGeneralParametersTransfers.Create
    ) -> BaseClientHTTPControllerResults:
        """Create a new organization in MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/"

            #* Declare body
            json = (
                MaleoIdentityOrganizationGeneralParametersTransfers
                .CreateOrUpdateData
                .model_validate(
                    parameters.model_dump()
                )
                .model_dump()
            )

            #* Parse parameters to query params
            params = (
                MaleoIdentityOrganizationGeneralParametersTransfers
                .CreateOrUpdateQuery
                .model_validate(
                    parameters.model_dump()
                )
                .model_dump(exclude_none=True)
            )

            #* Create auth
            token = self._service_manager.token
            auth = BearerAuth(token=token) if token is not None else None

            #* Send request and wait for response
            response = await client.post(url=url, json=json, params=params, auth=auth)
            return BaseClientHTTPControllerResults(response=response)

    async def update(
        self,
        parameters:MaleoIdentityOrganizationGeneralParametersTransfers.Update
    ) -> BaseClientHTTPControllerResults:
        """Update organization's data in MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/{parameters.identifier}/{parameters.value}"

            #* Declare body
            json = (
                MaleoIdentityOrganizationGeneralParametersTransfers
                .CreateOrUpdateData
                .model_validate(
                    parameters.model_dump()
                )
                .model_dump()
            )

            #* Parse parameters to query params
            params = (
                MaleoIdentityOrganizationGeneralParametersTransfers
                .CreateOrUpdateQuery
                .model_validate(
                    parameters.model_dump()
                )
                .model_dump(exclude_none=True)
            )

            #* Create auth
            token = self._service_manager.token
            auth = BearerAuth(token=token) if token is not None else None

            #* Send request and wait for response
            response = await client.put(url=url, json=json, params=params, auth=auth)
            return BaseClientHTTPControllerResults(response=response)

    async def get_organization_roles(
        self,
        parameters:MaleoIdentityOrganizationRoleClientParametersTransfers.GetMultipleFromOrganization
    ) -> BaseClientHTTPControllerResults:
        """Get organization's roles from MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/{parameters.organization_id}/roles/"

            #* Parse parameters to query params
            params = (
                MaleoIdentityOrganizationRoleClientParametersTransfers
                .GetMultipleFromOrganizationQuery
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

    async def get_organization_role(
        self,
        parameters:MaleoIdentityOrganizationRoleGeneralParametersTransfers.GetSingle
    ) -> BaseClientHTTPControllerResults:
        """Get organization's role from MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/{parameters.organization_id}/roles/{parameters.key}"

            #* Parse parameters to query params
            params = (
                MaleoIdentityOrganizationRoleGeneralParametersTransfers
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

    async def get_organization_users(
        self,
        parameters:MaleoIdentityUserOrganizationClientParametersTransfers.GetMultipleFromOrganization
    ) -> BaseClientHTTPControllerResults:
        """Get organization's users from MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/{parameters.organization_id}/users/"

            #* Parse parameters to query params
            params = (
                MaleoIdentityUserOrganizationClientParametersTransfers
                .GetMultipleFromOrganizationQuery
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

    async def get_organization_user(
        self,
        parameters:MaleoIdentityUserOrganizationGeneralParametersTransfers.GetSingle
    ) -> BaseClientHTTPControllerResults:
        """Get organization's user from MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/{parameters.organization_id}/users/{parameters.user_id}"

            #* Parse parameters to query params
            params = (
                MaleoIdentityUserOrganizationGeneralParametersTransfers
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

    async def get_organization_user_roles(
        self,
        parameters:MaleoIdentityUserOrganizationRoleClientParametersTransfers.GetMultipleFromUserOrOrganization
    ) -> BaseClientHTTPControllerResults:
        """Get organization's user roles from MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/{parameters.organization_id}/users/{parameters.user_id}/roles/"

            #* Parse parameters to query params
            params = (
                MaleoIdentityUserOrganizationRoleClientParametersTransfers
                .GetMultipleFromUserOrOrganizationQuery
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

    async def get_organization_user_role(
        self,
        parameters:MaleoIdentityUserOrganizationRoleGeneralParametersTransfers.GetSingle
    ) -> BaseClientHTTPControllerResults:
        """Get organization's user role from MaleoIdentity"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/organizations/{parameters.organization_id}/users/{parameters.user_id}/roles/{parameters.key}"

            #* Parse parameters to query params
            params = (
                MaleoIdentityUserOrganizationRoleGeneralParametersTransfers
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