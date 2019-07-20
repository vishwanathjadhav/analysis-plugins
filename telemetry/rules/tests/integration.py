from insights.tests import run_test
from insights.tests.integration import generate_tests
import pytest


def test_integration(component, compare_func, input_data, expected):
    actual = run_test(component, input_data)
    compare_func(actual, expected)


def pytest_generate_tests(metafunc):
    pattern = getattr(pytest, "-k", None)
    generate_tests(metafunc, test_integration, "telemetry/rules/tests", pattern=pattern)
