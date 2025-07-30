# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from abc import ABC
from functools import cached_property
from typing import Any, Type, final

from qa_pytest_commons.generic_steps import GenericSteps
from qa_pytest_commons.base_configuration import Configuration
from qa_testing_utils.logger import LoggerMixin
from qa_testing_utils.object_utils import ImmutableMixin


class AbstractTestsBase[
        TSteps: GenericSteps[Any],
        TConfiguration: Configuration](ABC, LoggerMixin, ImmutableMixin):
    """
    Basic test scenario implementation, holding some type of steps and a logger
    facility.

    Subtypes must set `_steps_type` to the actual type of steps implementation::

                            +---------------+
                            |  BddKeyWords  |
                            +---------------+
                                            ^
                                            |
                                        implements
                                            |
        +-------------------+               +--------------+
        | AbstractTestsBase |---contains--->| GenericSteps |
        |                   |               +--------------+
        |                   |                       +---------------+
        |                   |---contains----------->| Configuration |
        +-------------------+                       +---------------+

    Args:
        TSteps (TSteps:GenericSteps): The actual steps implementation, or partial implementation.
    """
    _steps_type: Type[TSteps]  # IMPORTANT: pytest classes must not __init__
    _configuration: TConfiguration

    @final
    @cached_property
    def steps(self) -> TSteps:
        '''
        Lazily initializes and returns an instance of steps implementation.

        Returns:
            TSteps: The instance of steps implementation.
        '''
        self.log.debug(f"initiating {self._steps_type}")
        return self._steps_type(self._configuration)

    def setup_method(self):
        """
        Override in subtypes with specific setup, if any.
        """
        self.log.debug("setup")

    def teardown_method(self):
        """
        Override in subtypes with specific teardown, if any.
        """
        self.log.debug("teardown")
