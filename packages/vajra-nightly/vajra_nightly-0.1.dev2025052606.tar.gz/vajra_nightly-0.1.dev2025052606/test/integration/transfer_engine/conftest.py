import pytest

test_counter = -1


def pytest_runtest_logstart(nodeid):
    global test_counter
    test_counter += 1


@pytest.fixture(scope="function")
def test_number():
    global test_counter
    return test_counter
