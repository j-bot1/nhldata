"""unit tests for Api class"""

import pytest
import responses
from requests.exceptions import ConnectionError, HTTPError
from enum import Enum
from nhldata.nhl_api import NhlApi


# Arrange - Get everything we'll need for our tests set up
JSON = {"x": [1, 2, 3, 4], "y": {"some_strings": ["a", "b", "c", "d"]}}
PARAMS = {"hello": "world"}


class Endpoint(Enum):
    ENDPOINT_200 = "http://example.com"
    ENDPOINT_200_WITH_QUERYSTRING = "http://example.com?hello=world"
    ENDPOINT_503 = "http://different_example.com"
    not_mocked = "http://response_never_mocked.com"


@pytest.fixture()
def mocked_responses():
    with responses.RequestsMock() as mock:
        yield mock


class TestNhlApiThrowsExceptions:
    def test_NhlApi_throws_connection_error(self):

        with pytest.raises(ConnectionError):
            x = NhlApi(Endpoint.not_mocked)
            x.request()

    def test_NhlApi_throws_exception_with_503(self, mocked_responses):

        mocked_responses.get(
            url=Endpoint.ENDPOINT_503.value,
            status=503,
        )
        with pytest.raises(HTTPError):
            x = NhlApi(Endpoint.ENDPOINT_503)
            x.request()

    def test_NhlApi_successfully_calls_an_endpoint(self, mocked_responses):

        mocked_responses.get(
            url=Endpoint.ENDPOINT_200.value,
        )

        try:
            x = NhlApi(Endpoint.ENDPOINT_200)
            x.request()
        except:
            assert False


class TestNhLApiDict:
    """Test that NhlApi can return the right data"""

    def test_returns_dict(self, mocked_responses):

        mocked_responses.get(
            url=Endpoint.ENDPOINT_200.value,
            json=JSON,
        )

        x = NhlApi(Endpoint.ENDPOINT_200)
        x.request()

        actual = x.to_dict()
        expected = JSON

        assert isinstance(actual, dict)
        assert actual["y"]["some_strings"] == ["a", "b", "c", "d"]
        assert actual == expected

    def test_returns_dict_from_call_with_params(self, mocked_responses):

        mocked_responses.get(
            url=Endpoint.ENDPOINT_200_WITH_QUERYSTRING.value,
            match_querystring=False,
            json=JSON,
        )

        x = NhlApi(
            Endpoint.ENDPOINT_200,
            params=PARAMS,
        )
        x.request()
        actual = x.to_dict()
        expected = JSON

        assert isinstance(actual, dict)
        assert actual == expected
