"""Main module for the aiopixooapi project.

This module demonstrates interacting with Divoom and Pixoo64 devices
using asynchronous API calls.
"""

import asyncio
import logging

from aiopixooapi.divoom import Divoom
from aiopixooapi.pixoo64 import Pixoo64, ChannelSelectIndex

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main() -> None:
    """Interact with Divoom and Pixoo64 devices asynchronously."""
    async with Divoom() as divoom:
        # Get dial types
        dial_types = await divoom.get_dial_type()
        logger.info(dial_types)

        # Get dial list for a specific type and page
        dial_list = await divoom.get_dial_list("Social", 1)
        logger.info(dial_list)

        # Get font list
        font_list = await divoom.get_font_list()
        logger.info(font_list)

        # Get image upload list
        img_upload_list = await divoom.get_img_upload_list(device_id=123, device_mac="00:11:22:33:44:55", page=1)
        logger.info(img_upload_list)

        # Get image like list
        img_like_list = await divoom.get_img_like_list(device_id=123, device_mac="00:11:22:33:44:55", page=1)
        logger.info(img_like_list)

    async with Pixoo64("10.116.4.238") as pixoo64:
        # Get all settings
        settings = await pixoo64.get_all_settings()
        logger.info(settings)

        # # Get clock info
        # clock_info = await pixoo64.get_clock_info()
        # logger.info(clock_info)
        #
        # # Get current channel
        # current_channel = await pixoo64.get_current_channel()
        # logger.info(current_channel)
        #
        # # Get device time
        # device_time = await pixoo64.get_device_time()
        # logger.info(device_time)
        #
        # # Get weather info
        # weather_info = await pixoo64.get_weather_info()
        # logger.info(weather_info)
        #
        # # Play buzzer
        # buzzer_response = await pixoo64.play_buzzer(100, 100, 1000)
        # logger.info(buzzer_response)
        #
        # # Get HTTP GIF ID
        # http_gif_id = await pixoo64.get_http_gif_id()
        # logger.info(http_gif_id)




        # # Set channel
        # channel_response = await pixoo64.set_channel(ChannelSelectIndex.FACES)
        # logger.info(channel_response)
        #
        # # Set clock face
        # clock_response = await pixoo64.set_clock_select_id(1)
        # logger.info(clock_response)
    #
    #     # Set custom page index
    #     custom_page_response = await pixoo64.set_custom_page_index(1)
    #     logger.info(custom_page_response)
    #
    #     # Set visualizer position
    #     visualizer_response = await pixoo64.set_visualizer_position(0)
    #     logger.info(visualizer_response)
    #
    #     # Set cloud channel
    #     cloud_channel_response = await pixoo64.set_cloud_channel(CloudChannelIndex.RECOMMEND_GALLERY)
    #     logger.info(cloud_channel_response)
    #
    #     # Set brightness
    #     brightness_response = await pixoo64.set_brightness(50)
    #     logger.info(brightness_response)
    #
    #     # Set weather area
    #     weather_response = await pixoo64.set_weather_area("37.7749", "-122.4194")
    #     logger.info(weather_response)
    #
    #     # Set time zone
    #     timezone_response = await pixoo64.set_time_zone("GMT-8")
    #     logger.info(timezone_response)
    #
    #     # Set system time
    #     system_time_response = await pixoo64.set_system_time(1672531200)
    #     logger.info(system_time_response)
    #
    #     # Set screen switch
    #     screen_switch_response = await pixoo64.set_screen_switch(1)
    #     logger.info(screen_switch_response)
    #
    #     # Set temperature mode
    #     temp_mode_response = await pixoo64.set_temperature_mode(0)
    #     logger.info(temp_mode_response)
    #
    #     # Set screen rotation angle
    #     rotation_response = await pixoo64.set_screen_rotation_angle(1)
    #     logger.info(rotation_response)
    #
    #     # Set mirror mode
    #     mirror_mode_response = await pixoo64.set_mirror_mode(1)
    #     logger.info(mirror_mode_response)
    #
    #     # Set hour mode
    #     hour_mode_response = await pixoo64.set_hour_mode(1)
    #     logger.info(hour_mode_response)
    #
    #     # Set high light mode
    #     high_light_response = await pixoo64.set_high_light_mode(1)
    #     logger.info(high_light_response)
    #
    #     # Set white balance
    #     white_balance_response = await pixoo64.set_white_balance(50, 50, 50)
    #     logger.info(white_balance_response)
    #
    #     # Set countdown timer
    #     countdown_response = await pixoo64.set_countdown_timer(1, 30, 1)
    #     logger.info(countdown_response)
    #
    #     # Set stopwatch
    #     stopwatch_response = await pixoo64.set_stopwatch(1)
    #     logger.info(stopwatch_response)
    #
    #     # Set scoreboard
    #     scoreboard_response = await pixoo64.set_scoreboard(10, 20)
    #     logger.info(scoreboard_response)
    #
    #     # Set noise tool
    #     noise_tool_response = await pixoo64.set_noise_tool(1)
    #     logger.info(noise_tool_response)
    #
    #     # Play GIF
    #     gif_response = await pixoo64.play_gif(2, "http://example.com/sample.gif")
    #     logger.info(gif_response)
    #
    #     # Play Divoom GIF
    #     divoom_gif_response = await pixoo64.play_divoom_gif("12345")
    #     logger.info(divoom_gif_response)
    #    #
    #     # Reset HTTP GIF ID
    #     reset_http_gif_id_response = await pixoo64.reset_http_gif_id()
    #     logger.info(reset_http_gif_id_response)
    #
    #     # Send animation frame
    #     animation_frame_response = await pixoo64.send_animation_frame(
    #         pic_num=10, pic_width=64, pic_offset=0, pic_id=1, pic_speed=100, pic_data="base64data"
    #     )
    #     logger.info(animation_frame_response)
    #
    #     # Send text
    #     text_response = await pixoo64.send_text(
    #         text_id=1, x=0, y=0, direction=0, font=1, text_width=32, text_string="Hello", speed=100, color="#FF0000"
    #     )
    #     logger.info(text_response)
    #
    #     # Clear text
    #     clear_text_response = await pixoo64.clear_text()
    #     logger.info(clear_text_response)
    #
    #     # Send display list
    #     display_list_response = await pixoo64.send_display_list(
    #         [{"TextId": 1, "type": 0, "x": 0, "y": 0, "dir": 0, "font": 1, "TextWidth": 32, "TextString": "Hello"}]
    #     )
    #     logger.info(display_list_response)

    #
    #     # Run command list
    #     command_list_response = await pixoo64.run_command_list(
    #         [{"Command": "Channel/SetBrightness", "Brightness": 50}]
    #     )
    #     logger.info(command_list_response)
    #
    #     # Use HTTP command source
    #     http_command_response = await pixoo64.use_http_command_source("http://example.com/commands.json")
    #     logger.info(http_command_response)

asyncio.run(main())
