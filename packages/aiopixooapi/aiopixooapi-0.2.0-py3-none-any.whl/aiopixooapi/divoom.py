"""Provides functionality for interacting with Divoom devices."""

from .base import BasePixoo


class Divoom(BasePixoo):
    """Subclass for handling online Divoom API calls."""

    def __init__(self, timeout: int = 10) -> None:
        """Initialize the online Divoom API.

        Args:
            timeout: Request timeout in seconds (default: 10).

        """
        base_url = "https://app.divoom-gz.com"
        super().__init__(base_url, timeout)

    async def get_dial_type(self) -> dict:
        """Fetch the list of dial types from the Divoom API."""
        return await self._make_request("Channel/GetDialType")

    async def get_dial_list(self, dial_type: str, page: int) -> dict:
        """Fetch the list of dials for a specific type and page.

        Args:
            dial_type: The type of dial (e.g., "Social", "Game").
            page: The page number to fetch (30 items per page).

        Returns:
            Response dictionary containing ReturnCode, TotalNum, and DialList.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.
            PixooConnectionError: If the request fails.

        """
        data = {"DialType": dial_type, "Page": page}
        return await self._make_request("Channel/GetDialList", data)

    async def get_font_list(self) -> dict:
        """Fetch the list of available fonts from the Divoom API.

        Returns:
            Response dictionary containing ReturnCode, ReturnMessage, and FontList.

        Raises:
            PixooCommandError: If the API returns an error or invalid response.
            PixooConnectionError: If the request fails.

        """
        return await self._make_request("Device/GetTimeDialFontList")

    async def get_img_upload_list(self, device_id: int, device_mac: str, page: int = 1) -> dict:
        """Fetch the image upload list from the Divoom API.

        Args:
            device_id: The ID of the device.
            device_mac: The MAC address of the device.
            page: The page number to fetch (default: 1).

        Returns:
            Response dictionary containing ReturnCode, ReturnMessage, and ImgList.

        Raises:
            ValueError: If device_id or device_mac is not provided.
            PixooCommandError: If the API returns an error or invalid response.
            PixooConnectionError: If the request fails.

        """
        if not device_id or not device_mac:
            msg = "DeviceId and DeviceMac must be provided."
            raise ValueError(msg)

        data = {"DeviceId": device_id, "DeviceMac": device_mac, "Page": page}
        return await self._make_request("Device/GetImgUploadList", data)

    async def get_img_like_list(self, device_id: int, device_mac: str, page: int = 1) -> dict:
        """Fetch the liked image list from the Divoom API.

        Args:
            device_id: The ID of the device.
            device_mac: The MAC address of the device.
            page: The page number to fetch (default: 1).

        Returns:
            Response dictionary containing ReturnCode, ReturnMessage, and ImgList.

        Raises:
            ValueError: If device_id or device_mac is not provided.
            PixooCommandError: If the API returns an error or invalid response.
            PixooConnectionError: If the request fails.

        """
        if not device_id or not device_mac:
            msg = "DeviceId and DeviceMac must be provided."
            raise ValueError(msg)

        data = {"DeviceId": device_id, "DeviceMac": device_mac, "Page": page}
        return await self._make_request("Device/GetImgLikeList", data)
