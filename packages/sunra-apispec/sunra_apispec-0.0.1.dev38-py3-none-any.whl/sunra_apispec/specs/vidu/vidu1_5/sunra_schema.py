# Schema for Text-to-Image generation
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Literal


class VideoGenBaseInput(BaseModel):
    """Base class for video generation inputs"""
    seed: int = Field(
        None,
        json_schema_extra={"x-sr-order": 201},
        description="Random seed for generation"
    )
    duration: Literal[4, 8] = Field(
        4,
        json_schema_extra={"x-sr-order": 410},
        description="Duration of the video in seconds"
    )
    movement_amplitude: Literal["auto", "small", "medium", "large"] = Field("auto",
        json_schema_extra={"x-sr-order": 411},
        description="The movement amplitude of objects in the frame"
    )
    resolution: Literal["360p", "720p", "1080p"] = Field("720p",
        json_schema_extra={"x-sr-order": 412},
        description="Resolution of the video"
    )
  

class TextToVideoInput(VideoGenBaseInput):
    """Text to video input"""
    prompt: str = Field(
        ..., 
        json_schema_extra={"x-sr-order": 200}, 
        max_length=1500, 
        description="The prompt for the video"
    )

    style: Literal["general", "anime"] = Field(
        "general", 
        json_schema_extra={"x-sr-order": 401}, 
        description="Style of the video"
    )

    aspect_ratio: Literal["16:9", "9:16", "1:1"] = Field("16:9",
        json_schema_extra={"x-sr-order": 402},
        description="Aspect ratio of the video"
    )


class ImageToVideoInput(VideoGenBaseInput):
    """Image to video input"""
    prompt: str = Field(
        None,
        json_schema_extra={"x-sr-order": 200},
        max_length=1500, description="Optional prompt to guide the video generation")

    start_image: HttpUrl | str = Field(
        ...,
        json_schema_extra={"x-sr-order": 301},
        description='Start image. Required.'
    )
    end_image: HttpUrl | str = Field(
        None,
        json_schema_extra={"x-sr-order": 302},
        description='End image. Optional.'
    )
