# ruff: noqa: PLR2004, Magic value used in comparison
# ruff: noqa: S101, Use of `assert` detected

"""Unit tests for the Pixoo64 device functionality."""
import pytest
from aioresponses import aioresponses

from aiopixooapi.pixoo64 import ChannelSelectIndex, CloudChannelIndex, Pixoo64


@pytest.mark.asyncio
async def test_sys_reboot() -> None:
    """Test the sys_reboot method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"ReturnCode": 0, "ReturnMessage": "Success"},
            )
            response = await pixoo64.sys_reboot()
            assert response["ReturnCode"] == 0
            assert response["ReturnMessage"] == "Success"


@pytest.mark.asyncio
async def test_get_all_settings() -> None:
    """Test the get_all_settings method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={
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
                    "LightSwitch": 1,
                },
            )
            response = await pixoo64.get_all_settings()
            assert response["error_code"] == 0
            assert response["Brightness"] == 100
            assert response["RotationFlag"] == 1
            assert response["ClockTime"] == 60
            assert response["GalleryTime"] == 60
            assert response["SingleGalleyTime"] == 5
            assert response["PowerOnChannelId"] == 1
            assert response["GalleryShowTimeFlag"] == 1
            assert response["CurClockId"] == 1
            assert response["Time24Flag"] == 1
            assert response["TemperatureMode"] == 1
            assert response["GyrateAngle"] == 1
            assert response["MirrorFlag"] == 1
            assert response["LightSwitch"] == 1


@pytest.mark.asyncio
async def test_set_clock_select_id() -> None:
    """Test the set_clock_select_id method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_clock_select_id(42)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_get_clock_info() -> None:
    """Test the get_clock_info method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"ClockId": 12, "Brightness": 100},
            )
            response = await pixoo64.get_clock_info()
            assert response["ClockId"] == 12
            assert response["Brightness"] == 100


@pytest.mark.asyncio
async def test_set_channel() -> None:
    """Test the set_channel method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_channel(ChannelSelectIndex.VISUALIZER)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_custom_page_index() -> None:
    """Test the set_custom_page_index method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_custom_page_index(1)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_custom_page_index_invalid() -> None:
    """Test the set_custom_page_index method with an invalid index."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="Invalid custom page index: 3. Must be between 0 and 2."):
            await pixoo64.set_custom_page_index(3)


@pytest.mark.asyncio
async def test_set_visualizer_position() -> None:
    """Test the set_visualizer_position method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_visualizer_position(3)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_visualizer_position_invalid() -> None:
    """Test the set_visualizer_position method with an invalid position."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="Invalid visualizer position: -1. Must be 0 or greater."):
            await pixoo64.set_visualizer_position(-1)


@pytest.mark.asyncio
async def test_set_cloud_channel() -> None:
    """Test the set_cloud_channel method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_cloud_channel(CloudChannelIndex.FAVOURITE)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_get_current_channel() -> None:
    """Test the get_current_channel method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"SelectIndex": 2},
            )
            response = await pixoo64.get_current_channel()
            assert response["SelectIndex"] == 2


@pytest.mark.asyncio
async def test_set_brightness() -> None:
    """Test the set_brightness method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_brightness(75)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_brightness_invalid() -> None:
    """Test the set_brightness method with an invalid brightness value."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="Invalid brightness value: 150. Must be between 0 and 100."):
            await pixoo64.set_brightness(150)


@pytest.mark.asyncio
async def test_set_weather_area() -> None:
    """Test the set_weather_area method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_weather_area("30.29", "20.58")
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_weather_area_invalid() -> None:
    """Test the set_weather_area method with invalid inputs."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="Longitude and Latitude must be provided."):
            await pixoo64.set_weather_area("", "20.58")
        with pytest.raises(ValueError, match="Longitude and Latitude must be provided."):
            await pixoo64.set_weather_area("30.29", "")


@pytest.mark.asyncio
async def test_set_time_zone() -> None:
    """Test the set_time_zone method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_time_zone("GMT-5")
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_time_zone_invalid() -> None:
    """Test the set_time_zone method with an invalid input."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="TimeZoneValue must be provided."):
            await pixoo64.set_time_zone("")


@pytest.mark.asyncio
async def test_set_system_time() -> None:
    """Test the set_system_time method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_system_time(1672416000)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_system_time_invalid() -> None:
    """Test the set_system_time method with an invalid UTC time."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="UTC time must be a positive integer."):
            await pixoo64.set_system_time(-1)


@pytest.mark.asyncio
async def test_set_screen_switch() -> None:
    """Test the set_screen_switch method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_screen_switch(1)
            assert response["error_code"] == 0

            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_screen_switch(0)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_screen_switch_invalid() -> None:
    """Test the set_screen_switch method with an invalid input."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="OnOff must be 0 \\(off\\) or 1 \\(on\\)."):
            await pixoo64.set_screen_switch(2)


@pytest.mark.asyncio
async def test_get_device_time() -> None:
    """Test the get_device_time method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={
                    "error_code": 0,
                    "UTCTime": 1647200428,
                    "LocalTime": "2022-03-14 03:40:28",
                },
            )
            response = await pixoo64.get_device_time()
            assert response["error_code"] == 0
            assert response["UTCTime"] == 1647200428
            assert response["LocalTime"] == "2022-03-14 03:40:28"


@pytest.mark.asyncio
async def test_set_temperature_mode() -> None:
    """Test the set_temperature_mode method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_temperature_mode(0)  # Celsius
            assert response["error_code"] == 0

            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_temperature_mode(1)  # Fahrenheit
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_temperature_mode_invalid() -> None:
    """Test the set_temperature_mode method with an invalid mode."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="Mode must be 0 \\(Celsius\\) or 1 \\(Fahrenheit\\)."):
            await pixoo64.set_temperature_mode(2)


@pytest.mark.asyncio
async def test_set_screen_rotation_angle() -> None:
    """Test the set_screen_rotation_angle method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_screen_rotation_angle(0)  # Normal
            assert response["error_code"] == 0

            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_screen_rotation_angle(1)  # 90 degrees
            assert response["error_code"] == 0

            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_screen_rotation_angle(2)  # 180 degrees
            assert response["error_code"] == 0

            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_screen_rotation_angle(3)  # 270 degrees
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_screen_rotation_angle_invalid() -> None:
    """Test the set_screen_rotation_angle method with an invalid mode."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="Mode must be 0 \\(normal\\), 1 \\(90\\), 2 \\(180\\), or 3 \\(270\\)."):
            await pixoo64.set_screen_rotation_angle(4)


@pytest.mark.asyncio
async def test_set_mirror_mode() -> None:
    """Test the set_mirror_mode method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_mirror_mode(0)  # Disable
            assert response["error_code"] == 0

            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_mirror_mode(1)  # Enable
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_mirror_mode_invalid() -> None:
    """Test the set_mirror_mode method with an invalid mode."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="Mode must be 0 \\(disable\\) or 1 \\(enable\\)."):
            await pixoo64.set_mirror_mode(2)


@pytest.mark.asyncio
async def test_set_hour_mode() -> None:
    """Test the set_hour_mode method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_hour_mode(1)  # 24-hour mode
            assert response["error_code"] == 0

            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_hour_mode(0)  # 12-hour mode
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_hour_mode_invalid() -> None:
    """Test the set_hour_mode method with an invalid mode."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="Mode must be 0 \\(12-hour\\) or 1 \\(24-hour\\)."):
            await pixoo64.set_hour_mode(2)


@pytest.mark.asyncio
async def test_set_high_light_mode() -> None:
    """Test the set_high_light_mode method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_high_light_mode(0)  # Close
            assert response["error_code"] == 0

            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_high_light_mode(1)  # Open
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_high_light_mode_invalid() -> None:
    """Test the set_high_light_mode method with an invalid mode."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="Mode must be 0 \\(close\\) or 1 \\(open\\)."):
            await pixoo64.set_high_light_mode(2)


@pytest.mark.asyncio
async def test_set_white_balance() -> None:
    """Test the set_white_balance method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_white_balance(100, 100, 100)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_white_balance_invalid() -> None:
    """Test the set_white_balance method with invalid RGB values."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="RValue must be between 0 and 100. Got: 150"):
            await pixoo64.set_white_balance(150, 100, 100)
        with pytest.raises(ValueError, match="GValue must be between 0 and 100. Got: -10"):
            await pixoo64.set_white_balance(100, -10, 100)
        with pytest.raises(ValueError, match="BValue must be between 0 and 100. Got: 200"):
            await pixoo64.set_white_balance(100, 100, 200)


@pytest.mark.asyncio
async def test_get_weather_info() -> None:
    """Test the get_weather_info method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={
                    "error_code": 0,
                    "Weather": "Cloudy",
                    "CurTemp": 33.68,
                    "MinTemp": 31.85,
                    "MaxTemp": 33.68,
                    "Pressure": 1006,
                    "Humidity": 50,
                    "Visibility": 10000,
                    "WindSpeed": 2.54,
                },
            )
            response = await pixoo64.get_weather_info()
            assert response["error_code"] == 0
            assert response["Weather"] == "Cloudy"
            assert response["CurTemp"] == 33.68
            assert response["MinTemp"] == 31.85
            assert response["MaxTemp"] == 33.68
            assert response["Pressure"] == 1006
            assert response["Humidity"] == 50
            assert response["Visibility"] == 10000
            assert response["WindSpeed"] == 2.54


@pytest.mark.asyncio
async def test_set_countdown_timer() -> None:
    """Test the set_countdown_timer method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_countdown_timer(1, 0, 1)  # Start countdown
            assert response["error_code"] == 0

            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_countdown_timer(0, 30, 0)  # Stop countdown
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_countdown_timer_invalid() -> None:
    """Test the set_countdown_timer method with invalid inputs."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="Minute must be between 0 and 59. Got: 60"):
            await pixoo64.set_countdown_timer(60, 0, 1)
        with pytest.raises(ValueError, match="Second must be between 0 and 59. Got: 70"):
            await pixoo64.set_countdown_timer(0, 70, 1)
        with pytest.raises(ValueError, match="Status must be 0 \\(stop\\) or 1 \\(start\\)."):
            await pixoo64.set_countdown_timer(0, 30, 2)


@pytest.mark.asyncio
async def test_set_stopwatch() -> None:
    """Test the set_stopwatch method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_stopwatch(1)  # Start stopwatch
            assert response["error_code"] == 0

            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_stopwatch(0)  # Stop stopwatch
            assert response["error_code"] == 0

            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_stopwatch(2)  # Reset stopwatch
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_stopwatch_invalid() -> None:
    """Test the set_stopwatch method with an invalid status."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="Status must be 0 \\(stop\\), 1 \\(start\\), or 2 \\(reset\\)."):
            await pixoo64.set_stopwatch(3)


@pytest.mark.asyncio
async def test_set_scoreboard() -> None:
    """Test the set_scoreboard method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_scoreboard(100, 79)  # Set scores
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_scoreboard_invalid() -> None:
    """Test the set_scoreboard method with invalid scores."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="BlueScore must be between 0 and 999. Got: 1000"):
            await pixoo64.set_scoreboard(1000, 79)
        with pytest.raises(ValueError, match="RedScore must be between 0 and 999. Got: -1"):
            await pixoo64.set_scoreboard(100, -1)


@pytest.mark.asyncio
async def test_set_noise_tool() -> None:
    """Test the set_noise_tool method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_noise_tool(1)  # Start noise tool
            assert response["error_code"] == 0

            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.set_noise_tool(0)  # Stop noise tool
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_set_noise_tool_invalid() -> None:
    """Test the set_noise_tool method with an invalid noise_status."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="NoiseStatus must be 0 \\(stop\\) or 1 \\(start\\)."):
            await pixoo64.set_noise_tool(2)


@pytest.mark.asyncio
async def test_play_gif() -> None:
    """Test the play_gif method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.play_gif(2, "http://f.divoom-gz.com/64_64.gif")
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_play_gif_invalid() -> None:
    """Test the play_gif method with invalid inputs."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="FileType must be 2 \\(net file\\)."):
            await pixoo64.play_gif(1, "http://f.divoom-gz.com/64_64.gif")
        with pytest.raises(ValueError, match="FileName must be provided."):
            await pixoo64.play_gif(2, "")


@pytest.mark.asyncio
async def test_play_divoom_gif() -> None:
    """Test the play_divoom_gif method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.play_divoom_gif("group1/M00/1C/80/eEwpPWQZFUmEQwsOAAAAAM8RSLs0290624")
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_play_divoom_gif_invalid() -> None:
    """Test the play_divoom_gif method with an invalid FileId."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="FileId must be provided."):
            await pixoo64.play_divoom_gif("")


@pytest.mark.asyncio
async def test_get_http_gif_id() -> None:
    """Test the get_http_gif_id method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={
                    "error_code": 0,
                    "PicId": 100,
                },
            )
            response = await pixoo64.get_http_gif_id()
            assert response["error_code"] == 0
            assert response["PicId"] == 100


@pytest.mark.asyncio
async def test_reset_http_gif_id() -> None:
    """Test the reset_http_gif_id method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.reset_http_gif_id()
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_send_animation_frame() -> None:
    """Test the send_animation_frame method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.send_animation_frame(
                pic_num=2,
                pic_width=64,
                pic_offset=0,
                pic_id=3,
                pic_speed=100,
                pic_data="AAIpAAIpAAIpAAIpAAIpAAIpAAIpAAIpAAIpAAIpAAIpAAIp",
            )
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_send_animation_frame_invalid() -> None:
    """Test the send_animation_frame method with invalid inputs."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="PicNum must be between 1 and 59. Got: 60"):
            await pixoo64.send_animation_frame(60, 64, 0, 3, 100, "data")
        with pytest.raises(ValueError, match="PicWidth must be one of 16, 32, or 64. Got: 128"):
            await pixoo64.send_animation_frame(2, 128, 0, 3, 100, "data")
        with pytest.raises(ValueError, match="PicOffset must be between 0 and PicNum-1. Got: 2"):
            await pixoo64.send_animation_frame(2, 64, 2, 3, 100, "data")
        with pytest.raises(ValueError, match="PicID must be greater than or equal to 1. Got: 0"):
            await pixoo64.send_animation_frame(2, 64, 0, 0, 100, "data")
        with pytest.raises(ValueError, match="PicSpeed must be a positive integer. Got: -1"):
            await pixoo64.send_animation_frame(2, 64, 0, 3, -1, "data")
        with pytest.raises(ValueError, match="PicData must be provided."):
            await pixoo64.send_animation_frame(2, 64, 0, 3, 100, "")


@pytest.mark.asyncio
async def test_send_text() -> None:
    """Test the send_text method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.send_text(
                text_id=4,
                x=0,
                y=40,
                direction=0,
                font=4,
                text_width=56,
                text_string="hello, Divoom",
                speed=10,
                color="#FFFF00",
                align=1,
            )
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_send_text_invalid() -> None:
    """Test the send_text method with invalid inputs."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="TextId must be between 0 and 19. Got: 20"):
            await pixoo64.send_text(20, 0, 40, 0, 4, 56, "hello", 10, "#FFFF00", 1)
        with pytest.raises(ValueError, match="TextWidth must be between 17 and 63. Got: 64"):
            await pixoo64.send_text(4, 0, 40, 0, 4, 64, "hello", 10, "#FFFF00", 1)
        with pytest.raises(ValueError, match="TextString length must be less than 512. Got: 512"):
            await pixoo64.send_text(4, 0, 40, 0, 4, 56, "a" * 512, 10, "#FFFF00", 1)
        with pytest.raises(ValueError, match="Direction must be 0 \\(scroll left\\) or 1 \\(scroll right\\). Got: 2"):
            await pixoo64.send_text(4, 0, 40, 2, 4, 56, "hello", 10, "#FFFF00", 1)
        with pytest.raises(ValueError, match="Font must be between 0 and 7. Got: 8"):
            await pixoo64.send_text(4, 0, 40, 0, 8, 56, "hello", 10, "#FFFF00", 1)
        with pytest.raises(ValueError, match="Align must be 1 \\(left\\), 2 \\(middle\\), or 3 \\(right\\). Got: 4"):
            await pixoo64.send_text(4, 0, 40, 0, 4, 56, "hello", 10, "#FFFF00", 4)


@pytest.mark.asyncio
async def test_clear_text() -> None:
    """Test the clear_text method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.clear_text()
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_send_display_list() -> None:
    """Test the send_display_list method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            item_list = [
                {
                    "TextId": 5,
                    "type": 6,
                    "x": 32,
                    "y": 32,
                    "dir": 0,
                    "font": 18,
                    "TextWidth": 32,
                    "Textheight": 16,
                    "speed": 100,
                    "align": 1,
                    "color": "#FF0000",
                },
                {
                    "TextId": 2,
                    "type": 22,
                    "x": 16,
                    "y": 16,
                    "dir": 0,
                    "font": 2,
                    "TextWidth": 48,
                    "Textheight": 16,
                    "speed": 100,
                    "align": 1,
                    "TextString": "hello, divoom",
                    "color": "#FFFFFF",
                },
            ]
            response = await pixoo64.send_display_list(item_list)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_send_display_list_invalid() -> None:
    """Test the send_display_list method with invalid inputs."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        invalid_item_list = [
            {"TextId": 40, "type": 6, "x": 32, "y": 32, "font": 18, "TextWidth": 32, "Textheight": 16},
        ]
        with pytest.raises(ValueError, match="TextId must be between 0 and 39. Got: 40"):
            await pixoo64.send_display_list(invalid_item_list)
        invalid_item_list = [
            {"TextId": 2, "type": 22, "TextString": "a" * 512},
        ]
        with pytest.raises(ValueError, match="TextString length must be less than 512. Got: 512"):
            await pixoo64.send_display_list(invalid_item_list)


@pytest.mark.asyncio
async def test_play_buzzer() -> None:
    """Test the play_buzzer method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.play_buzzer(500, 500, 3000)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_play_buzzer_invalid() -> None:
    """Test the play_buzzer method with invalid inputs."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="ActiveTimeInCycle must be a non-negative integer. Got: -1"):
            await pixoo64.play_buzzer(-1, 500, 3000)
        with pytest.raises(ValueError, match="OffTimeInCycle must be a non-negative integer. Got: -1"):
            await pixoo64.play_buzzer(500, -1, 3000)
        with pytest.raises(ValueError, match="PlayTotalTime must be a positive integer. Got: 0"):
            await pixoo64.play_buzzer(500, 500, 0)


@pytest.mark.asyncio
async def test_run_command_list() -> None:
    """Test the run_command_list method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            command_list = [
                {
                    "Command": "Device/PlayTFGif",
                    "FileType": 2,
                    "FileName": "http://f.divoom-gz.com/64_64.gif",
                },
                {
                    "Command": "Channel/SetBrightness",
                    "Brightness": 100,
                },
            ]
            response = await pixoo64.run_command_list(command_list)
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_run_command_list_invalid() -> None:
    """Test the run_command_list method with invalid inputs."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="CommandList must be a non-empty list."):
            await pixoo64.run_command_list([])
        with pytest.raises(ValueError, match="CommandList must be a non-empty list."):
            await pixoo64.run_command_list("invalid")


@pytest.mark.asyncio
async def test_use_http_command_source() -> None:
    """Test the use_http_command_source method."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with aioresponses() as mock:
            mock.post(
                "http://192.168.1.100:80/post",
                payload={"error_code": 0},
            )
            response = await pixoo64.use_http_command_source("http://f.divoom-gz.com/all_command.txt")
            assert response["error_code"] == 0


@pytest.mark.asyncio
async def test_use_http_command_source_invalid() -> None:
    """Test the use_http_command_source method with an invalid URL."""
    async with Pixoo64("192.168.1.100") as pixoo64:
        with pytest.raises(ValueError, match="CommandUrl must be provided."):
            await pixoo64.use_http_command_source("")
