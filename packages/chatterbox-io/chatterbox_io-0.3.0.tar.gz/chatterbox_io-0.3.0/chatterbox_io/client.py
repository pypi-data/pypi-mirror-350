import aiohttp
from typing import Optional
from .models import Session, SendBotRequest, TemporaryToken
from .websocket import WebSocketClient


class ChatterBox:
    """Main client for interacting with the ChatterBox API."""

    def __init__(
        self,
        authorization_token: str,
        base_url: str = "https://bot.chatter-box.io",
        websocket_base_url: str = "wss://ws.chatter-box.io",
    ):
        self.authorization_token = authorization_token
        self.base_url = base_url
        self.websocket_base_url = websocket_base_url
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp ClientSession."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.authorization_token}"}
            )
        return self._session

    async def close(self) -> None:
        """Close the client session."""
        if self._session is not None and not self._session.closed:
            await self._session.close()
            self._session = None

    async def get_temporary_token(self, expires_in: int = 3600) -> TemporaryToken:
        """
        Generate a temporary token for enhanced security.
        
        Args:
            expires_in: The duration in seconds for which the token should be valid.
                       Must be between 60 and 86400 seconds (1 minute to 24 hours).
                       Defaults to 3600 seconds (1 hour).
            
        Returns:
            TemporaryToken: Contains the temporary token and its expiration time
            
        Raises:
            ValueError: If expires_in is not between 60 and 86400 seconds
        """
        if not 60 <= expires_in <= 86400:
            raise ValueError("expires_in must be between 60 and 86400 seconds")
            
        session = await self._get_session()
        response = await session.post(
            f"{self.base_url}/token",
            json={"expiresIn": expires_in}
        )
        response.raise_for_status()
        data = await response.json()
        return TemporaryToken(**data)

    async def send_bot(self, **kwargs) -> Session:
        """
        Send a bot to a meeting.
        
        Args:
            platform: The platform to send the bot to ('zoom', 'googlemeet')
            meeting_id: The ID of the meeting
            meeting_password: (Optional) The meeting password
            bot_name: (Optional) Custom name for the bot
            webhook_url: (Optional) Webhook URL for meeting events
            language: (Optional) The language for transcription. Defaults to 'multi'
            model: (Optional) The Deepgram model to use for transcription. Defaults to 'nova-3'
            
        Returns:
            Session: The created session
        """
        # Create the request with proper field mapping
        request = SendBotRequest(**kwargs)
        
        session = await self._get_session()
        
        # Convert to camelCase for API call
        request_data = request.model_dump(by_alias=True, exclude_none=True)
        
        response = await session.post(
            f"{self.base_url}/join",
            json=request_data
        )
        response.raise_for_status()
        data = await response.json()
        
        # Add the request data to the response for context
        data.update({
            'platform': kwargs.get('platform'),
            'meetingId': kwargs.get('meeting_id'),
            'meetingPassword': kwargs.get('meeting_password'),
            'botName': kwargs.get('bot_name'),
            'webhookUrl': kwargs.get('webhook_url')
        })
            
        return Session(**data)

    def connect_socket(self, session_id: str) -> WebSocketClient:
        """
        Create a WebSocket connection for real-time events.
        
        Args:
            session_id: The ID of the session to connect to
            
        Returns:
            WebSocketClient: The WebSocket client instance
        """
        return WebSocketClient(session_id, self.authorization_token, self.websocket_base_url)