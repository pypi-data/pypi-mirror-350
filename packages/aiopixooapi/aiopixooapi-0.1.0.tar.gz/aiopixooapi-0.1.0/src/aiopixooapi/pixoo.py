"""Main Pixoo device control class.

Documentation: https:///docin.divoom-gz.com/web/#/5/24
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional

import aiohttp

from .exceptions import PixooConnectionError, PixooCommandError

logger = logging.getLogger(__name__)


class Pixoo:
    """Control class for Divoom Pixoo64 device."""

    def __init__(self, host: str, port: int = 80, timeout: int = 10):
        """Initialize Pixoo device connection.

        Args:
            host: IP address of the Pixoo device
            port: Port number (default: 80)
            timeout: Request timeout in seconds (default: 10)
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self._session: Optional[aiohttp.ClientSession] = None
        # noinspection HttpUrlsUsage
        self._base_url = f"http://{host}:{port}/post"

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def connect(self) -> None:
        """Create aiohttp session."""
        if self._session is None:
            self._session = aiohttp.ClientSession(
                headers={
                    "Content-Type": "application/json"
                },
                # Automatically call ClientResponse.raise_for_status() for each response
                raise_for_status=True,
            )
            logger.debug("Created new aiohttp session")

    async def _make_request(self, command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the Pixoo device.

        Args:
            command: Command string
            params: Optional parameters dictionary

        Returns:
            Response dictionary
            with an error_code number = 0 on success

        Raises:
            PixooCommandError: If the device returns an error or invalid response.
            PixooConnectionError: If the request fails.
        """
        if self._session is None:
            await self.connect()

        data = {"Command": command}
        if params:
            data.update(params)

        try:
            async with self._session.post(
                    self._base_url,
                    json=data,
                    timeout=self.timeout
            ) as response:
                text = await response.text()
                try:
                    result = json.loads(text)
                except Exception as json_err:
                    logger.error(f"Failed to parse JSON from response: {text}")
                    raise PixooCommandError(
                        f"Failed to parse JSON from response: {text}"
                    ) from json_err
                if result.get("error_code", 0) != 0:
                    raise PixooCommandError(f"Device returned error: {result}")
                return result
        except Exception as e:
            logger.error(f"Error making request to {command}: {e}")
            raise PixooConnectionError(f"Failed to connect to device: {e}")

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self._session:
            await self._session.close()
            # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
            # Zero-sleep to allow underlying connections to close
            await asyncio.sleep(0)
            self._session = None
            logger.debug("Closed aiohttp session")

    async def sys_reboot(self) -> Dict[str, Any]:
        """Reboot the Pixoo device.

        Sends the 'Device/SysReboot' command to the device, causing it to reboot.

        Returns:
            Response dictionary from the device.

        Raises:
            PixooCommandError: If the device returns an error or invalid response.
            PixooConnectionError: If the request fails.
        """
        logger.debug("Rebooting Pixoo device")
        return await self._make_request("Device/SysReboot")

    async def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings from the Pixoo device.

        Sends the 'Channel/GetAllConf' command to the device to retrieve all configuration settings.

        Returns:
            Response dictionary containing all settings.

        Raises:
            PixooCommandError: If the device returns an error or invalid response.
            PixooConnectionError: If the request fails.
        """
        logger.debug("Requesting all settings from Pixoo device")
        return await self._make_request("Channel/GetAllConf")
