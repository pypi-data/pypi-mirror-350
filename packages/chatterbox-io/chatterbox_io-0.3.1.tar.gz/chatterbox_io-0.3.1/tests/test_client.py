import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from chatterbox import ChatterBox, Session
from chatterbox.models import SendBotRequest, TemporaryToken


@pytest.fixture
def client():
    return ChatterBox(authorization_token="test_token")


@pytest.fixture
def mock_session():
    return Session(
        id="test_session_id",
        platform="zoom",
        meeting_id="1234567890",
        bot_name="TestBot"
    )


@pytest.mark.asyncio
async def test_send_bot(client, mock_session):
    mock_response = AsyncMock()
    mock_response.json.return_value = mock_session.model_dump(by_alias=True)
    mock_response.__aenter__.return_value = mock_response

    mock_session_instance = AsyncMock()
    mock_session_instance.post.return_value = mock_response

    with patch("aiohttp.ClientSession", return_value=mock_session_instance):
        result = await client.send_bot(
            platform="zoom",
            meeting_id="1234567890",
            bot_name="TestBot"
        )
        
        assert isinstance(result, Session)
        assert result.id == mock_session.id
        assert result.platform == mock_session.platform
        assert result.meeting_id == mock_session.meeting_id
        assert result.bot_name == mock_session.bot_name
        
        mock_session_instance.post.assert_called_once_with(
            "https://bot.chatter-box.io/join",
            json={
                "platform": "zoom",
                "meetingId": "1234567890",
                "botName": "TestBot"
            }
        )


@pytest.mark.asyncio
async def test_connect_socket(client):
    socket = client.connect_socket("test_session_id")
    assert socket.session_id == "test_session_id"
    assert socket.base_url == "wss://ws.chatter-box.io"


@pytest.mark.asyncio
async def test_close(client):
    mock_session_instance = AsyncMock()
    
    with patch("aiohttp.ClientSession", return_value=mock_session_instance):
        client._session = mock_session_instance
        await client.close()
        
        # Use await to properly check the async mock
        await mock_session_instance.close.aclose()


@pytest.mark.asyncio
async def test_get_temporary_token(client):
    mock_response = AsyncMock()
    mock_response.json.return_value = {
        "token": "test_token",
        "expiresIn": 3600
    }
    mock_response.__aenter__.return_value = mock_response

    mock_session_instance = AsyncMock()
    mock_session_instance.post.return_value = mock_response

    with patch("aiohttp.ClientSession", return_value=mock_session_instance):
        result = await client.get_temporary_token(expires_in=3600)
        
        assert isinstance(result, TemporaryToken)
        assert result.token == "test_token"
        assert result.expires_in == 3600
        
        mock_session_instance.post.assert_called_once_with(
            "https://bot.chatter-box.io/token",
            json={"expiresIn": 3600}
        )


@pytest.mark.asyncio
async def test_get_temporary_token_invalid_expiration(client):
    with pytest.raises(ValueError, match="expires_in must be between 60 and 86400 seconds"):
        await client.get_temporary_token(expires_in=30) 