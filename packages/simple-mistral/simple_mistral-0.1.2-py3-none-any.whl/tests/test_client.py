import pytest
from tests.builders.testcase_builder import ClientTestCaseBuilder


def test_send_request(test_case_builder: ClientTestCaseBuilder, mock_requests):
    client = test_case_builder.prepare_scenario.send_request(mock=mock_requests)
    response = test_case_builder.call_scenario.send_request(client=client)
    test_case_builder.check_scenario.send_request(response=response)


@pytest.mark.asyncio
async def test_send_async_request(test_case_builder: ClientTestCaseBuilder, mock_aioresponse):
    client = await test_case_builder.prepare_scenario.send_async_request(mock=mock_aioresponse)
    response = await test_case_builder.call_scenario.send_async_request(client=client)
    await test_case_builder.check_scenario.send_async_request(response=response)
