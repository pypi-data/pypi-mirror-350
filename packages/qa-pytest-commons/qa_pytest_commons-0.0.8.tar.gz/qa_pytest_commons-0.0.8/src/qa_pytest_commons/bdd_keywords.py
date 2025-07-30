# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod


class BddKeywords[TSteps:BddKeywords](ABC):
    """
    Base class for defining Behavior-Driven Development (BDD) keywords.

    This class provides a set of properties that represent the common BDD keywords
    such as `given`, `when`, `then`, `and_`, `with_`. Implementations might be
    of two types: step implementations (GenericSteps) or scenario implementations
    (AbstractTestsBase). In both cases, these properties must return an object
    that provides same step implementation, allowing a fluent-style coding::

        given.something(...) \

            .with.another_thing(...) \

            .when.doing_this(...) \

            .and.doing_that(...) \

            ... and so on, and so on ...
            ... eventually, expecting something ...
            .then.the_other_thing(is like that and like...)

    For more information on BDD, see the `Behavior-Driven Development
    <https://en.wikipedia.org/wiki/Behavior-driven_development>`_ Wikipedia article.

    This BDD implementation is an internal DSL, meaning it relies on the Python
    language, hence does not require a parser to read the scenarios from text
    files, nor additional tools to support IDE features for debugging, completion,
    refactoring, etc.

    Generic scenarios are available in BddScenarioTests, and basic PAM scenarios
    are available in FileScenarioTests.

    For more information on DSL, see the `Domain Specific Language
    <https://en.wikipedia.org/wiki/Domain-specific_language>`_ Wikipedia article.


    Args:
        TSteps (TSteps:BddKeywords): The actual steps implementation, or partial implementation.
    """

    @property
    @abstractmethod
    def given(self) -> TSteps:
        """
        Use to start definition of given stage.

        The given stage is the start-up point of a test.

        This might be a network connection, a file, a database, anything that
        is required for executing any further operations and verifications::

            given.a_connection(...connection details...)
        """
        pass

    @property
    @abstractmethod
    def when(self) -> TSteps:
        """
        Use to start definition of operations stage.

        The operations stage is the part that triggers some behavior on the SUT.

        This might be sending a command via a network connection, writing
        something to a file, or anything that will cause the SUT to output
        something verifiable::

            when.doing_something(...parameters...)
        """
        pass

    @property
    @abstractmethod
    def then(self) -> TSteps:
        """
        Use to start definition of verifications stage.

        The verifications stage is the part that samples actual output of the
        SUT and compares it against a predefined condition (a.k.a. rule).

        This might be sampling a file, a network response, or anything that
        can be asserted upon. For example, this might be a network response
        containing information about some file, like its size, which we might
        expected to be greater than 0 and lesser than something else::

            then.the_file(...rule to assert upon...)
        """
        pass

    @property
    @abstractmethod
    def and_(self) -> TSteps:
        """
        Use to continue definition of previous stage::

            given.a_connection(...whatever...) \

            .and_.an_umbrella(...) \

            .and_.some_thing_else....
        """
        pass

    @property
    @abstractmethod
    def with_(self) -> TSteps:
        """
        Same as `and_`, sometimes it just sounds better::

            given.a_connection(...whatever...) \

            .with_.authentication(...method details...)
        """
        pass
