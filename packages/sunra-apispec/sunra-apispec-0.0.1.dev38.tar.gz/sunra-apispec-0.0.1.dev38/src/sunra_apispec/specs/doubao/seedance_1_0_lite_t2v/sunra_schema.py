# Schema for Text-to-Video generation
from pydantic import BaseModel, Field
from typing import Literal

class TextToVideoInput(BaseModel):
    """Input model for text-to-video generation."""
    prompt: str = Field(
        ...,
        json_schema_extra={"x-sr-order": 200},
        max_length=2500,
        description="Text prompt for video generation"
    )
    
    resolution: Literal["480p", "720p"] = Field(
        "720p",
        json_schema_extra={"x-sr-order": 401},
        description="Video resolution"
    )
    
    aspect_ratio: Literal["16:9", "9:16", "1:1", "4:3", "3:4", "21:9", "9:21"] = Field(
        "16:9",
        json_schema_extra={"x-sr-order": 402},
        description="Aspect ratio of the video"
    )
    
    duration: Literal[5, 10] = Field(
        5,
        json_schema_extra={"x-sr-order": 403},
        description="Duration of the video in seconds"
    )

    seed: int = Field(
        default=-1,
        ge=-1,
        le=2**32-1,
        json_schema_extra={"x-sr-order": 404},
        description="Seed of the video generation"
    )
