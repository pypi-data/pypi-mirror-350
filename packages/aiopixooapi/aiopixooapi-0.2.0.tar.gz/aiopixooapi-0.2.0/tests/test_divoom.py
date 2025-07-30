# ruff: noqa: PLR2004, Magic value used in comparison
# ruff: noqa: S101, Use of `assert` detected
"""Unit tests for the Divoom device functionality."""

import pytest
from aioresponses import aioresponses

from aiopixooapi.divoom import Divoom


@pytest.mark.asyncio
async def test_get_dial_type() -> None:
    """Test the get_dial_type method."""
    async with Divoom() as divoom:
        with aioresponses() as mock:
            mock.post(
                "https://app.divoom-gz.com/Channel/GetDialType",
                payload={
                    "ReturnCode": 0,
                    "ReturnMessage": "",
                    "DialTypeList": ["Social", "normal", "financial"],
                },
            )
            response = await divoom.get_dial_type()
            assert response["ReturnCode"] == 0
            assert "DialTypeList" in response
            assert response["DialTypeList"] == ["Social", "normal", "financial"]


@pytest.mark.asyncio
async def test_get_dial_list() -> None:
    """Test the get_dial_list method."""
    async with Divoom() as divoom:
        with aioresponses() as mock:
            mock.post(
                "https://app.divoom-gz.com/Channel/GetDialList",
                payload={
                    "ReturnCode": 0,
                    "ReturnMessage": "",
                    "TotalNum": 100,
                    "DialList": [
                        {"ClockId": 10, "Name": "Classic Digital Clock"},
                        {"ClockId": 12, "Name": "US Stock - 2"},
                    ],
                },
            )
            response = await divoom.get_dial_list("Social", 1)
            assert response["ReturnCode"] == 0
            assert response["TotalNum"] == 100
            assert "DialList" in response
            assert len(response["DialList"]) == 2
            assert response["DialList"][0]["ClockId"] == 10
            assert response["DialList"][0]["Name"] == "Classic Digital Clock"


@pytest.mark.asyncio
async def test_get_font_list() -> None:
    """Test the get_font_list method."""
    async with Divoom() as divoom:
        with aioresponses() as mock:
            mock.post(
                "https://app.divoom-gz.com/Device/GetTimeDialFontList",
                payload={
                    "ReturnCode": 0,
                    "ReturnMessage": "",
                    "FontList": [
                        {
                            "id": 2,
                            "name": "8*8 English letters, Arabic figures,punctuation",
                            "width": "8",
                            "high": "8",
                            "charset": "",
                            "type": 0,
                        },
                        {
                            "id": 3,
                            "name": "16*16 Chinese characters",
                            "width": "16",
                            "high": "16",
                            "charset": "Chinese",
                            "type": 1,
                        },
                    ],
                },
            )
            response = await divoom.get_font_list()
            assert response["ReturnCode"] == 0
            assert "FontList" in response
            assert len(response["FontList"]) == 2
            assert response["FontList"][0]["id"] == 2
            assert response["FontList"][0]["name"] == "8*8 English letters, Arabic figures,punctuation"
            assert response["FontList"][1]["id"] == 3
            assert response["FontList"][1]["charset"] == "Chinese"


@pytest.mark.asyncio
async def test_get_img_upload_list() -> None:
    """Test the get_img_upload_list method."""
    async with Divoom() as divoom:
        with aioresponses() as mock:
            mock.post(
                "https://app.divoom-gz.com/Device/GetImgUploadList",
                payload={
                    "ReturnCode": 0,
                    "ReturnMessage": "",
                    "ImgList": [
                        {
                            "FileName": "avaa",
                            "FileId": "group1/M00/10/50/L1ghbmLVLZ6EI5kGAAAAAHM30Do8982712",
                        },
                        {
                            "FileName": "test_image",
                            "FileId": "group1/M00/10/51/L1ghbmLVLZ6EI5kGAAAAAHM30Do8982713",
                        },
                    ],
                },
            )
            response = await divoom.get_img_upload_list(300000001, "a8032aff46b1", 1)
            assert response["ReturnCode"] == 0
            assert "ImgList" in response
            assert len(response["ImgList"]) == 2
            assert response["ImgList"][0]["FileName"] == "avaa"
            assert response["ImgList"][0]["FileId"] == "group1/M00/10/50/L1ghbmLVLZ6EI5kGAAAAAHM30Do8982712"
            assert response["ImgList"][1]["FileName"] == "test_image"
            assert response["ImgList"][1]["FileId"] == "group1/M00/10/51/L1ghbmLVLZ6EI5kGAAAAAHM30Do8982713"


@pytest.mark.asyncio
async def test_get_img_upload_list_invalid() -> None:
    """Test the get_img_upload_list method with invalid inputs."""
    async with Divoom() as divoom:
        with pytest.raises(ValueError, match="DeviceId and DeviceMac must be provided."):
            await divoom.get_img_upload_list(0, "", 1)


@pytest.mark.asyncio
async def test_get_img_like_list() -> None:
    """Test the get_img_like_list method."""
    async with Divoom() as divoom:
        with aioresponses() as mock:
            mock.post(
                "https://app.divoom-gz.com/Device/GetImgLikeList",
                payload={
                    "ReturnCode": 0,
                    "ReturnMessage": "",
                    "ImgList": [
                        {
                            "FileName": "avaa",
                            "FileId": "group1/M00/10/50/L1ghbmLVLZ6EI5kGAAAAAHM30Do8982712",
                        },
                        {
                            "FileName": "test_image",
                            "FileId": "group1/M00/10/51/L1ghbmLVLZ6EI5kGAAAAAHM30Do8982713",
                        },
                    ],
                },
            )
            response = await divoom.get_img_like_list(300000001, "a8032aff46b1", 1)
            assert response["ReturnCode"] == 0
            assert "ImgList" in response
            assert len(response["ImgList"]) == 2
            assert response["ImgList"][0]["FileName"] == "avaa"
            assert response["ImgList"][0]["FileId"] == "group1/M00/10/50/L1ghbmLVLZ6EI5kGAAAAAHM30Do8982712"
            assert response["ImgList"][1]["FileName"] == "test_image"
            assert response["ImgList"][1]["FileId"] == "group1/M00/10/51/L1ghbmLVLZ6EI5kGAAAAAHM30Do8982713"


@pytest.mark.asyncio
async def test_get_img_like_list_invalid() -> None:
    """Test the get_img_like_list method with invalid inputs."""
    async with Divoom() as divoom:
        with pytest.raises(ValueError, match="DeviceId and DeviceMac must be provided."):
            await divoom.get_img_like_list(0, "", 1)
