"""unit tests for Api class"""

import responses
import pytest
from enum import Enum
from ...src.core import Api


__EXAMPLE_API__ = "http://example.api.com/api"


class API_URL(Enum):
    example = __EXAMPLE_API__


class TestApiStatusAndConnection:
    def test_connection_error(self):
        @responses.activate
        def run(self):
            responses.add(responses.GET, __EXAMPLE_API__)

            with pytest.raises(ConnectionError):
                Api = Api(API_URL.example)
                x.get()

        run(self)

    def test_Api_get_fails_with_bad_status(self):
        """Test that get method fails when status code is not 200"""

        url = __EXAMPLE_API__
        body = b"test callback"
        status = 404
        headers = {"foo": "bar"}

        def request_callback(request):
            return (status, headers, body)

        @responses.activate
        def run():

            responses.add_callback(
                responses.GET,
                url,
                request_callback,
                content_type=None,
            )

            with pytest.raises(Exception):
                x = Api(API_URL.example)
                x.get()

        run()

    def test_Api_get_with_status_200(self):
        """Test that get method works when status is 200"""

        url = __EXAMPLE_API__
        body = b"test callback"
        status = 200
        headers = {"foo": "bar"}

        def request_callback(request):
            return (status, headers, body)

        @responses.activate
        def run():

            responses.add_callback(
                responses.GET,
                url,
                request_callback,
                content_type=None,
            )

            try:
                x = Api(API_URL.example)
                x.get()
            except:
                assert False

        run()


class TestApiDict:
    def test_to_dict_returns_dict(self):
        data_dict = {
            "x": [1, 2, 3, 4],
            "y": {"some_strings": ["a", "b", "c", "d"]},
        }
        url = __EXAMPLE_API__
        body = json.dumps(data_dict, indent=4)
        headers = {"foo": "bar"}
        status = 200

        expected = data_dict

        def request_callback(request):
            return (status, headers, body)

        @responses.activate
        def run(expected):

            responses.add_callback(
                responses.GET,
                url,
                request_callback,
                content_type=None,
            )

            x = Api(API_URL.example)
            x.get()
            actual = x.to_dict()

            assert isinstance(actual, dict)
            assert actual == expected

        run(expected)

    def test_returns_dict_from_call_with_params(self):

        params = {
            "a": "value1",
            "b": "value2",
        }
        data_dict = {
            "x": [1, 2, 3, 4],
            "y": {"some_strings": ["a", "b", "c", "d"]},
        }
        url = f"{__EXAMPLE_API__}?a=value1?b=value2"
        body = json.dumps(data_dict, indent=4)
        headers = {"foo": "bar"}
        status = 200

        expected = data_dict

        def request_callback(request):
            return (status, headers, body)

        @responses.activate
        def run(expected):

            responses.add_callback(
                responses.GET,
                url,
                request_callback,
                content_type=None,
            )

            x = Api(API_URL.example, params=params)
            x.get()
            actual = x.to_dict()

            assert isinstance(actual, dict)
            assert actual == expected

        run(expected)
