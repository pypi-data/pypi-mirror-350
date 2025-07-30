# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from typing import Any, Generic, TypeVar, override

from qa_pytest_rest.rest_configuration import RestConfiguration
from qa_pytest_rest.rest_steps import RestSteps
from qa_pytest_commons.abstract_tests_base import AbstractTestsBase
import requests

# NOTE: python limitation; we cannot declare it such as:
# class RestTests[TSteps:RestSteps[TConfiguration], TConfiguration: RestConfiguration](AbstractTestsBase[TSteps, TConfiguration]):
TConfiguration = TypeVar("TConfiguration", bound=RestConfiguration)
# TSteps can be any subclass of RestSteps, with any configuration type parameter.
# However, Python's type system cannot enforce that the parameter to RestSteps is
# itself a subclass of RestConfiguration; this is the closest we can get:
TSteps = TypeVar("TSteps", bound=RestSteps[Any])


class RestTests(
        Generic[TSteps, TConfiguration],
        AbstractTestsBase[TSteps, TConfiguration]):
    """
    Base class for REST API test cases.

    This class provides a reusable test base for REST API testing, managing a `requests.Session`
    for each test method. It is generic over the types of steps and configuration used.

    Attributes:
        _rest_session (requests.Session): The HTTP session used for making REST requests.
            Note: This session is not thread-safe.

    Type Parameters:
        TSteps: The type of the steps class, typically derived from RestSteps.
        TConfiguration: The type of the configuration class, typically derived from RestConfiguration.

    Methods:
        setup_method(self):
            Initializes a new requests.Session before each test method.

        teardown_method(self):
            Closes the requests.Session after each test method.
    """
    _rest_session: requests.Session  # not thread safe

    @override
    def setup_method(self):
        super().setup_method()
        self._rest_session = requests.Session()

    @override
    def teardown_method(self):
        try:
            self._rest_session.close()
        finally:
            super().teardown_method()
