from unittest.mock import MagicMock, patch
from utils.Dataloaders import getUserFromInfo

import pytest
from unittest.mock import patch
from utils.Dataloaders import composeAuthUrl  

def test_compose_auth_url_valid():
    with patch('os.environ.get', return_value='http://valid-url'):
        result = composeAuthUrl()
        assert result == 'http://valid-url'

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




from utils.Dataloaders import getUserFromInfo  

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



from utils.Dataloaders import getAuthorizationToken  

def test_get_authorization_token():
    mock_request = MagicMock()
    mock_info = MagicMock(context={"request": mock_request})

    assert getAuthorizationToken(mock_info) is None

def test_get_authorization_token_no_request():
    mock_info = MagicMock(context={})

    with pytest.raises(AssertionError):
        getAuthorizationToken(mock_info)

from utils.Dataloaders import getGroupFromInfo, demouser
def test_get_group_from_info():
    result = getGroupFromInfo(None)  # Argument is not used in function
    assert result == demouser


import pytest
import asyncio
from unittest.mock import patch, MagicMock
from unittest.mock import AsyncMock
from utils.Dataloaders import AuthorizationLoader, composeAuthUrl

class TestAuthorizationLoader:

    @pytest.fixture
    def loader(self):
        return AuthorizationLoader()
    
    @pytest.mark.usefixtures("loader")
    def test_initialization(self, loader):
        assert loader.roleUrlEndpoint == composeAuthUrl()
        assert loader.query is not None
        assert loader.demo is True  # Use 'is' for boolean comparison

    @pytest.mark.usefixtures("loader")
    def test_set_token_by_info(self, loader):
        loader.setTokenByInfo("some info")
        assert loader.authorizationToken == ""  # Depends on the implementation

    @patch('utils.Dataloaders.aiohttp.ClientSession.post')
    @pytest.mark.asyncio
    async def test_load_success(self, mock_post, loader):
        mock_post.return_value.__aenter__.return_value.json = AsyncMock(return_value={'data': {'result': {'roles': []}}})
        mock_post.return_value.__aenter__.return_value.status = 200


    @patch('utils.Dataloaders.aiohttp.ClientSession.post')
    @pytest.mark.asyncio
    async def test_load_failure(self, mock_post, loader):
        mock_post.return_value.__aenter__.return_value.status = 400
        mock_post.return_value.__aenter__.return_value.text = MagicMock(return_value="Error")

        with pytest.raises(Exception):
            await loader._load("some_id")


    
    @patch('utils.Dataloaders.AuthorizationLoader._load')
    @pytest.mark.asyncio
    async def test_batch_load_fn(self, mock_load, loader):
        # Mock _load to return an empty list directly
        mock_load.side_effect = lambda key: []  # Assuming _load returns an empty list for each key

        keys = ['id1', 'id2', 'id3']
        results = await loader.batch_load_fn(keys)
        assert results == [[], [], []]  

