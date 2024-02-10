from unittest.mock import MagicMock, patch
from utils.Dataloaders import getUserFromInfo

import pytest
from unittest.mock import patch
from utils.Dataloaders import composeAuthUrl  

def test_compose_auth_url_valid():
    with patch('os.environ.get', return_value='http://valid-url'):
        result = composeAuthUrl()
        assert result == 'http://valid-url'


# from utils.Dataloaders import AuthorizationLoader  

# class MockResponse:
#     def __init__(self, json_data, status):
#         self.json_data = json_data
#         self.status = status

#     async def json(self):
#         return self.json_data

#     async def __aenter__(self):
#         return self

#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         pass


# class MockClientSession:
#     def __init__(self, response_data, status_code):
#         self.response_data = response_data
#         self.status_code = status_code

#     async def post(self, url, json=None, headers=None):
#         return MockResponse(self.response_data, self.status_code)

# @pytest.mark.asyncio
# async def test_load_success():
#     mock_response_data = {
#         "data": {
#             "result": {
#                 "roles": [{"user": {"id": "user1"}, "group": {"id": "group1"}, "roletype": {"id": "role1"}}]
#             }
#         }
#     }

#     async def mock_post(*args, **kwargs):
#         return MockResponse(mock_response_data, 200)

#     with patch('aiohttp.ClientSession', return_value = MockClientSession(mock_response_data, 200)):
#         loader = AuthorizationLoader()
#         result = await loader._load("eb46ece6-be1b-4142-a5c5-0aac31e681f0")
#         assert result == mock_response_data["data"]["result"]["roles"]

# @pytest.mark.asyncio
# async def test_load_failure():
#     mock_response_data = {"errors": ["Some error"]}

#     async def mock_post(*args, **kwargs):
#         return MockResponse(mock_response_data, 200)

#     with patch('aiohttp.ClientSession.post', new=mock_post):
#         loader = AuthorizationLoader()
#         result = await loader._load("some_id")
#         assert result == []

# @pytest.mark.asyncio
# async def test_batch_load_fn():
#     # Prepare mock data for multiple keys
#     mock_response_data_key1 = {"data": {"result": {"roles": [{"user": {"id": "user1"}}]}}}
#     mock_response_data_key2 = {"data": {"result": {"roles": [{"user": {"id": "user2"}}]}}}

#     async def mock_post(url, json, headers):
#         if json["variables"]["id"] == "key1":
#             return MockResponse(mock_response_data_key1, 200)
#         elif json["variables"]["id"] == "key2":
#             return MockResponse(mock_response_data_key2, 200)
#         else:
#             return MockResponse({}, 400)

#     with patch('aiohttp.ClientSession.post', new=mock_post):
#         loader = AuthorizationLoader()
#         results = await loader.batch_load_fn(["key1", "key2", "key1"])  # Duplicate key "key1"
        
#         assert len(results) == 3
#         assert results[0] == mock_response_data_key1["data"]["result"]["roles"]
#         assert results[1] == mock_response_data_key2["data"]["result"]["roles"]
#         assert results[2] == mock_response_data_key1["data"]["result"]["roles"]  # Result for the duplicate key







# def test_get_user_from_info_with_no_user():
#     mock_info = MagicMock()
#     mock_info.context = {
#         "request": MagicMock(headers={"Authorization": "Bearer invalid_token"})
#     }

#     # Mock the behavior of getUserFromInfo for an invalid token
#     with patch('utils.Dataloaders.getUserFromInfo', return_value=None):
#         result = getUserFromInfo(mock_info)
#         assert result is None





# def test_get_user_from_info_with_valid_token():
#     demo_user = {"id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003", "name": "Tester"}
#     mock_info = MagicMock()
#     mock_info.context = {
#         "request": MagicMock(headers={"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"})
#     }

#     # Mock the behavior of getUserFromInfo for a valid token
#     with patch('utils.Dataloaders.getUserFromInfo', return_value=demo_user):
#         result = getUserFromInfo(mock_info)
#         assert result == demo_user



from utils.Dataloaders import getUgConnection

def test_get_ug_connection_with_connection_present():
    # Create a mock context with 'ug_connection' present
    mock_context = {"ug_connection": "mock_connection_object"}
    mock_info = MagicMock(context=mock_context)

    # Call the function with the mocked info object
    result = getUgConnection(mock_info)

    # Assert that the result is the mock connection object
    assert result == "mock_connection_object"


def test_get_ug_connection_with_no_connection():
    # Create a mock context without 'ug_connection'
    mock_context = {}
    mock_info = MagicMock(context=mock_context)

    # Call the function with the mocked info object
    result = getUgConnection(mock_info)

    # Assert that the result is None
    assert result is None


@pytest.mark.asyncio
async def test_get_ug_connection_async_context():
    mock_context = {"ug_connection": "mock_async_connection_object"}
    mock_info = MagicMock(context=mock_context)

    result = getUgConnection(mock_info)

    assert result == "mock_async_connection_object"




from utils.Dataloaders import getUserFromInfo  # Replace with the actual module name

def test_get_user_from_info_with_user():
    mock_user = {"name": "Test User"}
    mock_info = MagicMock(context={"user": mock_user})
    
    result = getUserFromInfo(mock_info)
    assert result == mock_user

def test_get_user_from_info_with_request_scope_user():
    mock_user = {"name": "Test User"}
    mock_request = MagicMock(scope={"user": mock_user})
    mock_info = MagicMock(context={"request": mock_request})

    result = getUserFromInfo(mock_info)
    assert result == mock_user

def test_get_user_from_info_no_user():
    mock_request = MagicMock(scope={})
    mock_info = MagicMock(context={"request": mock_request})

    with pytest.raises(AssertionError):
        getUserFromInfo(mock_info)



from utils.Dataloaders import getAuthorizationToken  # Replace with the actual module name

def test_get_authorization_token():
    mock_request = MagicMock()
    mock_info = MagicMock(context={"request": mock_request})

    # Assuming your function is supposed to do something more, adjust the test accordingly
    assert getAuthorizationToken(mock_info) is None

def test_get_authorization_token_no_request():
    mock_info = MagicMock(context={})

    with pytest.raises(AssertionError):
        getAuthorizationToken(mock_info)

from utils.Dataloaders import getGroupFromInfo, demouser
def test_get_group_from_info():
    result = getGroupFromInfo(None)  # Argument is not used in your function
    assert result == demouser



