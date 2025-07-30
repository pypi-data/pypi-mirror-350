from unittest.mock import AsyncMock, patch

import pytest
from aiopixooapi.exceptions import PixooCommandError
from aiopixooapi.pixoo import Pixoo


@pytest.mark.asyncio
async def test_sys_reboot_success():
    pixoo = Pixoo("127.0.0.1")
    mock_response = {"error_code": 0, "result": "ok"}
    with patch.object(pixoo, "_make_request", AsyncMock(return_value=mock_response)):
        result = await pixoo.sys_reboot()
        assert result == mock_response


@pytest.mark.asyncio
async def test_sys_reboot_error():
    pixoo = Pixoo("127.0.0.1")
    with patch.object(pixoo, "_make_request", AsyncMock(side_effect=PixooCommandError("Device error"))):
        with pytest.raises(PixooCommandError):
            await pixoo.sys_reboot()


@pytest.mark.asyncio
async def test_get_all_settings_success():
    pixoo = Pixoo("127.0.0.1")
    mock_response = {
        "error_code": 0,
        "Brightness": 100,
        "RotationFlag": 1,
        "ClockTime": 60,
        "GalleryTime": 60,
        "SingleGalleyTime": 5,
        "PowerOnChannelId": 1,
        "GalleryShowTimeFlag": 1,
        "CurClockId": 1,
        "Time24Flag": 1,
        "TemperatureMode": 1,
        "GyrateAngle": 1,
        "MirrorFlag": 1,
        "LightSwitch": 1
    }
    with patch.object(pixoo, "_make_request", AsyncMock(return_value=mock_response)):
        result = await pixoo.get_all_settings()
        assert result == mock_response


@pytest.mark.asyncio
async def test_get_all_settings_error():
    pixoo = Pixoo("127.0.0.1")
    with patch.object(pixoo, "_make_request", AsyncMock(side_effect=PixooCommandError("Device error"))):
        with pytest.raises(PixooCommandError):
            await pixoo.get_all_settings()


@pytest.mark.asyncio
async def test_connect_and_close():
    pixoo = Pixoo("127.0.0.1")
    await pixoo.connect()
    assert pixoo._session is not None
    await pixoo.close()
    assert pixoo._session is None
