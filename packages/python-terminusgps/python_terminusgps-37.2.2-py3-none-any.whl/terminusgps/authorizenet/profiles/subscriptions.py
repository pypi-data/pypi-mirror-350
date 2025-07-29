import decimal

from authorizenet import apicontractsv1, apicontrollers

from terminusgps.authorizenet.constants import AuthorizenetSubscriptionStatus
from terminusgps.authorizenet.profiles.base import AuthorizenetSubProfileBase


class SubscriptionProfile(AuthorizenetSubProfileBase):
    """An Authorizenet subscription profile."""

    @property
    def name(self) -> str | None:
        """
        The subscription name.

        :type: :py:obj:`str` | :py:obj:`None`

        """
        if self.id:
            sub = self._authorizenet_get_subscription().subscription
            return str(sub.name)

    @property
    def amount(self) -> decimal.Decimal | None:
        """
        The subscription amount.

        :type: :py:obj:`~decimal.Decimal` | :py:obj:`None`

        """
        if self.id:
            decimal.getcontext().prec = 4
            sub = self._authorizenet_get_subscription().subscription
            return decimal.Decimal(float(sub.amount)) * 1

    @property
    def status(self) -> AuthorizenetSubscriptionStatus | None:
        """
        Current subscription status.

        :type: :py:obj:`~terminusgps.authorizenet.constants.AuthorizenetSubscriptionStatus` | :py:obj:`None`

        """
        if self.id:
            return AuthorizenetSubscriptionStatus(
                self._authorizenet_get_subscription_status().status
            )

    @property
    def transactions(self) -> list[dict[str, str]]:
        """
        Subscription transactions.

        :type: :py:obj:`list`
        """
        if not self.id:
            return []
        sub = self._authorizenet_get_subscription(
            include_transactions=True
        ).subscription
        return [t.arbTransaction for t in sub.arbTransactions]

    @property
    def address_id(self) -> int | None:
        """
        Returns the address id for the subscription profile.

        :type: :py:obj:`int` | :py:obj:`None`

        """
        if self.id:
            sub = self._authorizenet_get_subscription().subscription
            return int(sub.profile.shippingProfile.customerAddressId)

    @property
    def payment_id(self) -> int | None:
        """
        Returns the payment id for the subscription profile.

        :type: :py:obj:`int` | :py:obj:`None`

        """
        if self.id:
            sub = self._authorizenet_get_subscription().subscription
            return int(sub.profile.paymentProfile.customerPaymentProfileId)

    def create(self, subscription: apicontractsv1.ARBSubscriptionType) -> int:
        """
        Creates a subscription in Authorizenet.

        :param subscription: A subscription.
        :type subscription: :py:obj:`~authorizenet.apicontractsv1.ARBSubscriptionType`
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: A subscription id.
        :rtype: :py:obj:`int`

        """
        return int(self._authorizenet_create_subscription(subscription).subscriptionId)

    def update(self, subscription: apicontractsv1.ARBSubscriptionType) -> None:
        """
        Updates a subscription in Authorizenet if :py:attr:`id` is set.

        :param subscription: A subscription.
        :type subscription: :py:obj:`~authorizenet.apicontractsv1.ARBSubscriptionType`
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        if self.id:
            self._authorizenet_update_subscription(subscription)

    def delete(self) -> None:
        """
        Deletes (cancels) a subscription in Authorizenet if :py:attr:`id` is set.

        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        if self.id:
            self._authorizenet_cancel_subscription()

    def _authorizenet_create_subscription(
        self, subscription: apicontractsv1.ARBSubscriptionType
    ) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.ARBCreateSubscriptionRequest` using the Authorizenet API.

        `ARBCreateSubscriptionRequest <https://developer.authorize.net/api/reference/index.html#recurring-billing-create-a-subscription-from-customer-profile>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        request = apicontractsv1.ARBCreateSubscriptionRequest(
            merchantAuthentication=self.merchantAuthentication,
            subscription=subscription,
        )

        controller = apicontrollers.ARBCreateSubscriptionController(request)
        return self.execute_controller(controller)

    def _authorizenet_get_subscription(
        self, include_transactions: bool = False
    ) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.ARBGetSubscriptionRequest` using the Authorizenet API.

        `ARBGetSubscriptionRequest <https://developer.authorize.net/api/reference/index.html#recurring-billing-get-subscription>`_

        :param include_transactions: Whether or not to include subscription transactions in the Authorizenet API response. Default is :py:obj:`False`.
        :type include_transaction: :py:obj:`bool`
        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        assert self.id, "'id' was not set."

        request = apicontractsv1.ARBGetSubscriptionRequest(
            merchantAuthentication=self.merchantAuthentication,
            subscriptionId=self.id,
            includeTransactions=str(include_transactions).lower(),
        )

        controller = apicontrollers.ARBGetSubscriptionController(request)
        return self.execute_controller(controller)

    def _authorizenet_get_subscription_status(self) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.ARBGetSubscriptionStatusRequest` using the Authorizenet API.

        `ARBGetSubscriptionStatusRequest <https://developer.authorize.net/api/reference/index.html#recurring-billing-get-subscription-status>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        assert self.id, "'id' was not set."

        request = apicontractsv1.ARBGetSubscriptionStatusRequest(
            merchantAuthentication=self.merchantAuthentication, subscriptionId=self.id
        )

        controller = apicontrollers.ARBGetSubscriptionStatusController(request)
        return self.execute_controller(controller)

    def _authorizenet_update_subscription(
        self, subscription: apicontractsv1.ARBSubscriptionType
    ) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.ARBUpdateSubscriptionRequest` using the Authorizenet API.

        `ARBUpdateSubscriptionRequest <https://developer.authorize.net/api/reference/index.html#recurring-billing-update-a-subscription>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        assert self.id, "'id' was not set."

        request = apicontractsv1.ARBUpdateSubscriptionRequest(
            merchantAuthentication=self.merchantAuthentication,
            subscriptionId=self.id,
            subscription=subscription,
        )

        controller = apicontrollers.ARBUpdateSubscriptionController(request)
        return self.execute_controller(controller)

    def _authorizenet_cancel_subscription(self) -> dict | None:
        """
        Executes a :py:obj:`~authorizenet.apicontractsv1.ARBCancelSubscriptionRequest` using the Authorizenet API.

        `ARBCancelSubscriptionRequest <https://developer.authorize.net/api/reference/index.html#recurring-billing-cancel-a-subscription>`_

        :raises AssertionError: If :py:attr:`id` wasn't set.
        :raises AuthorizenetControllerExecutionError: If something goes wrong during an Authorizenet API call.
        :returns: An Authorizenet API response, if any.
        :rtype: :py:obj:`dict` | :py:obj:`None`

        """
        assert self.id, "'id' was not set."

        request = apicontractsv1.ARBCancelSubscriptionRequest(
            merchantAuthentication=self.merchantAuthentication, subscriptionId=self.id
        )

        controller = apicontrollers.ARBCancelSubscriptionController(request)
        return self.execute_controller(controller)
