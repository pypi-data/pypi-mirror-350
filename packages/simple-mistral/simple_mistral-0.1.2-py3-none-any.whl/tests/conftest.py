import pytest
import pytest_asyncio
from aioresponses import aioresponses
from requests_mock import Mocker

from tests.builders.testcase_builder import ClientTestCaseBuilder


@pytest.fixture(scope='function')
def test_case_builder():
    return ClientTestCaseBuilder()


@pytest_asyncio.fixture
async def mock_aioresponse() -> aioresponses:
    with aioresponses() as mock:
        yield mock


@pytest.fixture
def mock_requests() -> Mocker:
    with Mocker() as mock:
        yield mock
