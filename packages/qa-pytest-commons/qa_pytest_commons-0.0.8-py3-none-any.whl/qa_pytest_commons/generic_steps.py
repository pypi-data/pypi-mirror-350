# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

import logging
from datetime import timedelta
from typing import Any, Callable, Self, final, override

from functional import seq
from hamcrest import assert_that
from hamcrest.core.matcher import Matcher
from tenacity import Retrying, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log
from typing import Callable
from qa_testing_utils.exception_utils import safely

from qa_testing_utils.logger import LoggerMixin, traced
from qa_testing_utils.object_utils import Valid, valid
from qa_pytest_commons.base_configuration import BaseConfiguration
from qa_pytest_commons.bdd_keywords import BddKeywords
from qa_testing_utils.stream_utils import Supplier
from qa_testing_utils.thread_utils import sleep_for


class GenericSteps[TConfiguration: BaseConfiguration](
        BddKeywords['GenericSteps'],
        LoggerMixin):
    """
    Generic steps beyond the BDD-keywords and diagnostics methods, most important:
    - retrying, for attempting a step that sporadically fails
    - eventually_assert_that, for asserting on sporadically failing operations

    IMPORTANT: if parallel testing will be required, and supported by the SUT,
    then internal state must be either thread-safe, or protected by TLS vars.

    The state it holds is mutated by steps. In a scenario there might be an
    operation o1 reading some info to be used by o2, followed by o1 later on,
    effectively rewriting previous value.

    Subtypes, such as PamSteps, may provide real system steps, relying on these
    ones. As such, these types might choose to redefine the _retry_policy herein::

                            +---------------+
                            |  BddKeyWords  |
                            +---------------+
                                            ^
                                            |
                                        implements
                                            |
        +-------------------+               +--------------+
        | AbstractTestsBase |---contains--->| GenericSteps |
        +-------------------+               +--------------+

    """

    _retrying: Retrying
    _configuration: TConfiguration

    def __init__(self, configuration: TConfiguration):
        self._configuration = configuration
        # NOTE: waits 1 sec after 1st failure, 2, 4, and 8 secs on subsequent;
        # see BddScenarioTests#should_retry
        self._retrying = Retrying(
            stop=stop_after_attempt(4),
            wait=wait_exponential(min=1, max=10),
            retry=retry_if_exception_type(Exception),
            before_sleep=before_sleep_log(self.log, logging.DEBUG)
        )

    @final
    @property
    def configured(self) -> TConfiguration:
        return self._configuration

    @final
    @property
    def retry_policy(self) -> Retrying:
        return self._retrying

    @final
    @property
    @override
    def given(self) -> Self:
        return self

    @final
    @property
    @override
    def when(self) -> Self:
        return self

    @final
    @property
    @override
    def then(self) -> Self:
        return self

    @final
    @property
    @override
    def and_(self) -> Self:
        return self

    @final
    @property
    @override
    def with_(self) -> Self:
        return self

    @final
    @property
    def nothing(self) -> Self:
        """
        Intended to support self-testing which does not rely on outer world
        system::

            given.nothing \

            .when.... doing your stuff here...

        Returns:
            Self: these steps
        """
        return self

    # DELETEME
    # # @traced -- nothing to trace here...
    # def configuration(self, configuration: TConfiguration) -> Self:
    #     """
    #     Sets the configuration to use.

    #     Args:
    #         configuration (TConfiguration): the configuration

    #     Returns:
    #         Self: these steps
    #     """
    #     self._configuration = configuration
    #     return self

    def set[T:Valid](self, field_name: str, field_value: T) -> T:
        """
        Sets field to specified value

        Args:
            field_name (str): name of field; the field should be defined as annotation
            field_value (T:Valid): value of field that can be validated

        Raises:
            AttributeError: if the field is not defined
            TypeError: if the object does not support the Valid protocol
            InvalidValueException: if the object is invalid

        Returns:
            _type_: the value of set field
        """
        if field_name not in self.__class__.__annotations__:
            raise AttributeError(
                f"{field_name} is not a valid attribute of "
                f"{self.__class__.__name__}.")

        setattr(self, field_name, valid(field_value))
        return field_value

    @final
    def step(self, *args: Any) -> Self:
        """
        Casts anything to a step.

        Returns:
            Self: these steps
        """
        return self

    @final
    def tracing(self, value: Any) -> Self:
        """
        Logs value at DEBUG level using the logger of this steps class.

        Use to trace something as a step, usually in a lambda expression::

            when.retrying(lambda: self.trace(valid(...call some API...))) \

                .and_....this can be further chained with other steps....

        Args:
            value (Any): _description_

        Returns:
            Self: these steps
        """
        self.log.debug(f"=== {value}")
        return self

    @final
    @traced
    def waiting(self, duration: timedelta = timedelta(seconds=0)) -> Self:
        """
        Blocks current thread for specified duration.

        Consider using retrying or eventually_assert_that instead of this.

        Args:
            duration (timedelta, optional): Defaults to timedelta(seconds=0).

        Returns:
            Self: these steps
        """
        sleep_for(duration)
        return self

    @final
    @traced
    def failing(self, exception: Exception) -> Self:
        """
        Intended to support self-testing of retrying and eventually_assert_that
        steps below.

        Args:
            exception (Exception): some exception

        Raises:
            exception: that exception

        Returns:
            Self: these steps
        """
        raise exception

    @final
    @traced
    def repeating(self, range: range, step: Callable[[int], Self]) -> Self:
        """
        Intended for stress testing -- repeats specified steps.

        Args:
            range (range): a range
            step (Callable[[int], Self]): lambda of step to repeat with counter

        Returns:
            Self: these steps
        """
        seq(range).for_each(step)  # type: ignore
        return self

    # TODO parallel_repeating

    @final
    @traced
    def safely(self, step: Callable[[], Self]) -> Self:
        """
        Executes specified step, swallowing its exceptions.

        Args:
            step (Callable[[], Self]): a lambda expression returning Self

        Returns:
            Self: these steps
        """
        return safely(lambda: step()).value_or(self)

    # TODO implement a raises decorator to mark method as raising some exception
    # at run-time the decorator shall check if raised exception matches the declared list.
    # This one would be:
    # @raises(tenacity.RetryError)
    @final
    # @traced
    def retrying(self, step: Callable[[], Self]) -> Self:
        '''
        Retries specified step according to _retry_policy.

        The default _retry_policy can be overridden by sub-types.

        Args:
            step (Callable[[], Self]): a lambda expression returning Self

        Returns:
            Self: these steps
        '''
        return self._retrying(step)

    @final
    # @traced
    def eventually_assert_that[T](
            self, supplier: Supplier[T],
            by_rule: Matcher[T]) -> Self:
        '''
        Repeatedly applies specified rule on specified supplier, according to
        _retry_policy.

        The default _retry_policy can be overridden by sub-types.

        Args:
            supplier (Callable[[], T]): a lambda expression returning T
            by_rule (Matcher[T]): a Hamcrest Matcher on T; basically, this is \
            just a predicate with a description, read more on \
                https://github.com/hamcrest/PyHamcrest

        Returns:
            Self: these steps
        '''
        return self._retrying(lambda: self._assert_that(supplier(), by_rule))

    @final
    @traced
    def it_works(self, matcher: Matcher[bool]) -> Self:
        """
        Intended to support self-testing of reports.

        Args:
            matcher (Matcher[bool]): is_(True) will trigger a green report, \
            while is_(False) will trigger a red report

        Returns:
            Self: these steps
        """
        assert_that(True, matcher)
        return self

    @final
    # NOTE @traced here is redundant
    def _assert_that[T](self, value: T, by_rule: Matcher[T]) -> Self:
        """
        Adapts PyHamcrest's assert_that to the BDD world by returning Self.

        Args:
            value (T): the value to assert upon
            by_rule (Matcher[T]): the Hamcrest matcher to apply

        Returns:
            Self: these steps
        """
        assert_that(value, by_rule)
        return self
