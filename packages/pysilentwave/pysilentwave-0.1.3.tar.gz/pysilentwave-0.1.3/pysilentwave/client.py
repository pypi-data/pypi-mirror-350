"""Client for TheSilentWave devices."""

import aiohttp
from .exceptions import SilentWaveError


class SilentWaveClient:
    """Client to interact with TheSilentWave API."""

    def __init__(self, host, session=None):
        """Initialize the client.

        Args:
            host: The host address of the SilentWave device
            session: Optional aiohttp ClientSession (e.g., from Home Assistant)
        """
        self._host = host
        self._base_url = f"http://{host}:8080/api"
        self._session = session

    async def get_status(self):
        """Get the current status."""
        if self._session:
            # Use the injected session
            return await self._fetch_status(self._session)
        else:
            # Create a temporary session
            async with aiohttp.ClientSession() as session:
                return await self._fetch_status(session)

    async def _fetch_status(self, session):
        """Fetch status using the provided session."""
        try:
            url = f"{self._base_url}/status"
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.text()
                return "on" if data.strip() == "1" else "off"
        except aiohttp.ClientError as err:
            raise SilentWaveError(f"Error communicating with device: {err}") from err
