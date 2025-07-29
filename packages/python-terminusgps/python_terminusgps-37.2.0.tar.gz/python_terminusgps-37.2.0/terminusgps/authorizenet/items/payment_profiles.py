import typing

from authorizenet import apicontractsv1, apicontrollers

from .base import AuthorizenetBase


class AuthorizenetPaymentProfile(AuthorizenetBase):
    """An Authorizenet payment profile."""

    def __init__(self, customerProfileId: int | str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if isinstance(customerProfileId, str) and not customerProfileId.isdigit():
            raise ValueError(
                f"'customerProfileId' can only contain digits, got '{customerProfileId}'."
            )
        self.customerProfileId = customerProfileId

    def create(
        self,
        payment: apicontractsv1.paymentType,
        address: apicontractsv1.customerAddressType,
        default: bool = False,
        validate: bool = False,
    ) -> int:
        """
        Creates an Authorizenet payment profile and returns its id as an integer.

        If successfully created, sets :py:attr:`id` to the new payment profile id.

        :param payment: A payment object.
        :type payment: :py:obj:`~authorizenet.apicontractsv1.paymentType`
        :param address: A customer address object.
        :type address: :py:obj:`~authorizenet.apicontractsv1.customerAddressType`
        :param default: Whether or not to set the payment profile as default.
        :type default: :py:obj:`bool`
        :param validate: Whether or not to validate the payment profile.
        :type validate: :py:obj:`bool`
        :raises AuthorizenetControllerExecutionError: If something went wrong during an Authorizenet API call.
        :returns: The new payment profile id.
        :rtype: :py:obj:`int`

        """
        response = self._authorizenet_create_customer_payment_profile(
            payment=payment, address=address, default=default, validate=validate
        )

        payment_id = int(response.customerPaymentProfileId)
        self.id = payment_id

        return payment_id

    def update(
        self,
        payment: apicontractsv1.paymentType,
        address: apicontractsv1.customerAddressType,
        default: bool = False,
        validate: bool = False,
    ) -> None:
        """
        Updates the Authorizenet payment profile if :py:attr:`id` is set.

        :param payment: A payment object.
        :type payment: :py:obj:`~authorizenet.apicontractsv1.paymentType`
        :param address: A customer address object.
        :type address: :py:obj:`~authorizenet.apicontractsv1.customerAddressType`
        :param default: Whether or not to set the payment profile as default.
        :type default: :py:obj:`bool`
        :param validate: Whether or not to validate the payment profile.
        :type validate: :py:obj:`bool`
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        if self.id:
            self._authorizenet_update_customer_payment_profile(
                payment=payment, address=address, default=default, validate=validate
            )

    def delete(self) -> None:
        """
        Deletes the Authorizenet payment profile.

        If successfully deleted, sets :py:attr:`id` to :py:obj:`None`.

        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """

        if self.id:
            self._authorizenet_delete_customer_payment_profile()
            self.id = None

    def _authorizenet_create_customer_payment_profile(
        self,
        payment: apicontractsv1.paymentType,
        address: apicontractsv1.customerAddressType,
        default: bool = False,
        validate: bool = False,
    ) -> dict[str, typing.Any] | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.createCustomerPaymentProfileRequest` using the Authorizenet API.

        `createCustomerPaymentProfileRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-create-customer-payment-profile>`_

        :param payment: A payment object.
        :type payment: :py:obj:`~authorizenet.apicontractsv1.paymentType`
        :param address: A customer address object.
        :type address: :py:obj:`~authorizenet.apicontractsv1.customerAddressType`
        :param default: Whether or not to set the payment profile as default.
        :type default: :py:obj:`bool`
        :param validate: Whether or not to validate the payment profile in Authorizenet.
        :type validate: :py:obj:`bool`
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """

        request = apicontractsv1.createCustomerPaymentProfileRequest()
        request.merchantAuthentication = self.merchantAuthentication
        request.paymentProfile = apicontractsv1.customerPaymentProfileType()
        request.paymentProfile.payment = payment
        request.paymentProfile.address = address
        request.paymentProfile.defaultPaymentProfile = str(default).lower()

        if validate:
            request.validationMode = self.validationMode

        return self.execute_controller(
            apicontrollers.createCustomerPaymentProfileController(request)
        )

    def _authorizenet_get_customer_payment_profile(
        self, issuer_info: bool = False
    ) -> dict[str, typing.Any] | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.getCustomerPaymentProfileRequest` using the Authorizenet API.

        `getCustomerPaymentProfileRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-get-customer-payment-profile>`_

        :param issuer_info: Whether or not to include issuer information in the response.
        :type issuer_info: :py:obj:`bool`
        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """

        assert self.id, "Customer payment profile id wasn't set."

        request = apicontractsv1.getCustomerPaymentProfileRequest()
        request.merchantAuthentication = self.merchantAuthentication
        request.customerProfileId = self.customerProfileId
        request.customerPaymentProfileId = self.id
        request.includeIssuerInfo = str(issuer_info).lower()

        return self.execute_controller(
            apicontrollers.getCustomerPaymentProfileController(request)
        )

    def _authorizenet_validate_customer_payment_profile(
        self,
    ) -> dict[str, typing.Any] | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.validateCustomerPaymentProfileRequest` using the Authorizenet API.

        `validateCustomerPaymentProfileRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-validate-customer-payment-profile>`_

        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """

        request = apicontractsv1.validateCustomerPaymentProfileRequest()
        request.merchantAuthentication = self.merchantAuthentication
        request.customerProfileId = self.customerProfileId
        request.customerPaymentProfileId = self.id
        request.validationMode = self.validationMode

        return self.execute_controller(
            apicontrollers.validateCustomerPaymentProfileController(request)
        )

    def _authorizenet_update_customer_payment_profile(
        self,
        payment: apicontractsv1.paymentType,
        address: apicontractsv1.customerAddressType,
        default: bool = False,
        validate: bool = False,
    ) -> dict[str, typing.Any] | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.updateCustomerPaymentProfileRequest` using the Authorizenet API.

        `updateCustomerPaymentProfileRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-update-customer-payment-profile>`_

        :param payment: A payment object.
        :type payment: :py:obj:`~authorizenet.apicontractsv1.paymentType`
        :param address: A customer address object.
        :type address: :py:obj:`~authorizenet.apicontractsv1.customerAddressType`
        :param default: Whether or not to set the payment profile as default.
        :type default: :py:obj:`bool`
        :param validate: Whether or not to validate the payment profile in Authorizenet.
        :type validate: :py:obj:`bool`
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """

        request = apicontractsv1.updateCustomerPaymentProfileRequest()
        request.merchantAuthentication = self.merchantAuthentication
        request.customerProfileId = self.customerProfileId

        request.paymentProfile = apicontractsv1.customerPaymentProfileType()
        request.paymentProfile.payment = payment
        request.paymentProfile.address = address
        request.paymentProfile.defaultPaymentProfile = str(default).lower()
        request.paymentProfile.customerPaymentProfileId = self.id

        if validate:
            request.validationMode = self.validationMode

        return self.execute_controller(
            apicontrollers.updateCustomerPaymentProfileController(request)
        )

    def _authorizenet_delete_customer_payment_profile(
        self,
    ) -> dict[str, typing.Any] | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.deleteCustomerPaymentProfileRequest` using the Authorizenet API.

        `deleteCustomerPaymentProfileRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-delete-customer-payment-profile>`_

        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        request = apicontractsv1.deleteCustomerPaymentProfileRequest()
        request.merchantAuthentication = self.merchantAuthentication
        request.customerProfileId = self.customerProfileId
        request.customerPaymentProfileId = self.id

        return self.execute_controller(
            apicontrollers.deleteCustomerPaymentProfileController(request)
        )
