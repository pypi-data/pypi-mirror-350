import typing

from authorizenet import apicontractsv1, apicontrollers

from .base import AuthorizenetBase


class AuthorizenetCustomerProfile(AuthorizenetBase):
    """An Authorizenet customer profile."""

    def __init__(self, email: str, merchant_id: str, *args, **kwargs) -> None:
        """
        Sets :py:attr:`_email` and :py:attr:`_merchant_id`.

        :param email: An email address.
        :type email: :py:obj:`str`
        :param merchant_id: A merchant designated id string.
        :type merchant_id: :py:obj:`str`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        super().__init__(*args, **kwargs)
        self._email = email
        self._merchant_id = merchant_id

    @property
    def email(self) -> str:
        """An email address assigned to the customer profile."""
        return str(self._email)

    @property
    def merchant_id(self) -> str:
        """A merchant designated id assigned to the customer profile."""
        return str(self._merchant_id)

    @email.setter
    def email(self, other: str) -> None:
        """Sets :py:attr:`email` to ``other``."""
        self._email = str(other)

    @merchant_id.setter
    def merchant_id(self, other: str) -> None:
        """Sets :py:attr:`merchant_id` to ``other``."""
        self._merchant_id = str(other)

    def create(self, desc: str | None = None, validate: bool = False) -> int:
        """
        Creates an Authorizenet customer profile and returns its id as an integer.

        If successfully created, sets :py:attr:`id` to the new customer profile id.

        :param desc: An optional customer profile description. Default is :py:obj:`None`
        :type desc: :py:obj:`str` | :py:obj:`None`
        :param validate: Whether or not to validate a payment on the new customer profile. Default is :py:obj:`False`.
        :type validate: :py:obj:`bool`
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: A customer profile id integer.
        :rtype: :py:obj:`int`

        """

        profile = apicontractsv1.customerProfileType()
        profile.merchantCustomerId = self.merchant_id
        if desc:
            profile.description = desc

        response = self._authorizenet_create_customer_profile(profile, validate)
        profile_id = int(response.customerProfileId)
        self.id = profile_id

        return profile_id

    def delete(self) -> None:
        """
        Deletes the Authorizenet customer profile.

        If successfully deleted, sets :py:attr:`id` to :py:obj:`None`.

        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """

        if self.id:
            self._authorizenet_delete_customer_profile()
            self._id = None

    def update(self, desc: str | None = None, validate: bool = False) -> None:
        """
        Updates the Authorizenet customer profile if :py:attr:`id` is set.

        :param desc: An optional customer profile description. Default is :py:obj:`None`
        :type desc: :py:obj:`str` | :py:obj:`None`
        :param validate: Whether or not to validate a payment on the customer profile. Default is :py:obj:`False`.
        :type validate: :py:obj:`bool`
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """

        if self.id:
            profile = apicontractsv1.customerProfileExType()
            profile.customerProfileId = self.id
            profile.merchantCustomerId = self.merchant_id
            profile.email = self.email
            if desc is not None:
                profile.description = desc

            self._authorizenet_update_customer_profile(profile, validate)

    def _authorizenet_get_customer_profile(
        self, issuer_info: bool = False
    ) -> dict[str, typing.Any] | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.getCustomerProfileRequest` using the Authorizenet API.

        `getCustomerProfileRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-get-customer-profile>`_

        :param issuer_info: Whether or not to include issuer information in the response. Default is :py:obj:`False`.
        :type issuer_info: :py:obj:`bool`
        :raises AssertionError: If none of :py:attr:`id`, :py:attr:`email` or :py:attr:`merchant_id` were set.
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """

        assert any([self.id, self.email, self.merchant_id]), (
            "At least one of 'id', 'email' or 'merchant_id' must be set."
        )

        request = apicontractsv1.getCustomerProfileRequest()
        request.merchantAuthentication = self.merchantAuthentication
        request.includeIssuerInfo = str(issuer_info).lower()

        if self.id:
            request.customerProfileId = self.id
        if self.email:
            request.email = self.email
        if self.merchant_id:
            request.customerMerchantId = self.merchant_id

        return self.execute_controller(
            apicontrollers.getCustomerProfileController(request)
        )

    def _authorizenet_create_customer_profile(
        self, profile: apicontractsv1.customerProfileType, validate: bool = False
    ) -> dict[str, typing.Any] | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.createCustomerProfileRequest` using the Authorizenet API.

        `createCustomerProfileRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-create-customer-profile>`_

        :param profile: A customer profile object.
        :type profile: :py:obj:`~authorizenet.apicontractsv1.customerProfileType`
        :param validate: Whether or not to validate a payment profile for the customer profile. Default is :py:obj:`False`.
        :type validate: :py:obj:`bool`
        :raises AuthorizenetControllerExecutionError: If ``validate`` was :py:obj:`True` but validation was forbidden.
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        request = apicontractsv1.createCustomerProfileRequest()
        request.merchantAuthentication = self.merchantAuthentication
        request.profile = profile
        if validate:
            request.validationMode = self.validationMode

        return self.execute_controller(
            apicontrollers.createCustomerProfileController(request)
        )

    def _authorizenet_update_customer_profile(
        self, profile: apicontractsv1.customerProfileExType, validate: bool = False
    ) -> dict[str, typing.Any] | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.updateCustomerProfileRequest` using the Authorizenet API.

        `updateCustomerProfileRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-update-customer-profile>`_

        :param profile: A customer profile ex object.
        :type profile: :py:obj:`~authorizenet.apicontractsv1.customerProfileExType`
        :param validate: Whether or not to validate a payment profile for the customer profile. Default is :py:obj:`False`.
        :type validate: :py:obj:`bool`
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """

        request = apicontractsv1.updateCustomerProfileRequest()
        request.merchantAuthentication = self.merchantAuthentication
        request.profile = profile
        if validate:
            request.validationMode = self.validationMode

        return self.execute_controller(
            apicontrollers.updateCustomerProfileController(request)
        )

    def _authorizenet_delete_customer_profile(self) -> dict[str, typing.Any] | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.deleteCustomerProfileRequest` using the Authorizenet API.

        `deleteCustomerProfileRequest <https://developer.authorize.net/api/reference/index.html#customer-profiles-delete-customer-profile>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """

        assert self.id, "Customer profile id wasn't set."

        request = apicontractsv1.deleteCustomerProfileRequest()
        request.merchantAuthentication = self.merchantAuthentication
        request.customerProfileId = self.id

        return self.execute_controller(
            apicontrollers.deleteCustomerProfileController(request)
        )
