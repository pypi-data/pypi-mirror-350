import typing

from authorizenet import apicontractsv1, apicontrollers

from .base import AuthorizenetBase


class AuthorizenetAddressProfile(AuthorizenetBase):
    """An Authorizenet address profile."""

    def __init__(self, customerProfileId: int | str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if isinstance(customerProfileId, str) and not customerProfileId.isdigit():
            raise ValueError(
                f"'customerProfileId' can only contain digits, got '{customerProfileId}'."
            )
        self.customerProfileId = customerProfileId

    def _authorizenet_create_customer_shipping_address(
        self, address: apicontractsv1.customerAddressType, default: bool = False
    ) -> dict[str, typing.Any] | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.createCustomerShippingAddressRequest` using the Authorizenet API.

        `createCustomerShippingAddressRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-create-customer-shipping-address>`_

        :param address: A customer address object.
        :type address: :py:obj:`~authorizenet.apicontractsv1.customerAddressType`
        :param default: Whether or not to set the address profile as default.
        :type default: :py:obj:`bool`
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """

        request = apicontractsv1.createCustomerShippingAddressRequest()
        request.merchantAuthentication = self.merchantAuthentication
        request.customerProfileId = self.customerProfileId
        request.address = address
        request.defaultShippingAddress = str(default).lower()

        return self.execute_controller(
            apicontrollers.createCustomerShippingAddressController(request)
        )

    def _authorizenet_get_customer_shipping_address(
        self,
    ) -> dict[str, typing.Any] | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.getCustomerShippingAddressRequest` using the Authorizenet API.

        `getCustomerShippingAddressRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-get-customer-shipping-address>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """

        assert self.id, "Address profile id wasn't set."

        request = apicontractsv1.getCustomerShippingAddressRequest()
        request.merchantAuthentication = self.merchantAuthentication
        request.customerProfileId = self.customerProfileId
        request.customerAddressId = self.id

        return self.execute_controller(
            apicontrollers.getCustomerShippingAddressController(request)
        )

    def _authorizenet_update_customer_shipping_address(
        self, address: apicontractsv1.customerAddressType, default: bool = False
    ) -> dict[str, typing.Any] | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.updateCustomerShippingAddress` using the Authorizenet API.

        `updateCustomerShippingAddressRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-update-customer-shipping-address>`_

        :param address: A customer address object.
        :type address: :py:obj:`~authorizenet.apicontractsv1.customerAddressType`
        :param default: Whether or not to set the address profile as default.
        :type default: :py:obj:`bool`
        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        request = apicontractsv1.updateCustomerShippingAddressRequest()
        request.merchantAuthentication = self.merchantAuthentication
        request.customerProfileId = self.customerProfileId
        request.address = address
        request.address.customerAddressId = self.id
        request.defaultShippingAddress = str(default).lower()

        return self.execute_controller(
            apicontrollers.updateCustomerShippingAddressController(request)
        )

    def _authorizenet_delete_customer_shipping_address(
        self,
    ) -> dict[str, typing.Any] | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.deleteCustomerShippingAddress` using the Authorizenet API.

        `deleteCustomerShippingAddressRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-delete-customer-shipping-address>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """

        assert self.id, "Address profile id wasn't set."

        request = apicontractsv1.deleteCustomerShippingAddressRequest()
        request.merchantAuthentication = self.merchantAuthentication
        request.customerProfileId = self.customerProfileId
        request.customerAddressId = self.id

        return self.execute_controller(
            apicontrollers.deleteCustomerShippingAddressController(request)
        )
