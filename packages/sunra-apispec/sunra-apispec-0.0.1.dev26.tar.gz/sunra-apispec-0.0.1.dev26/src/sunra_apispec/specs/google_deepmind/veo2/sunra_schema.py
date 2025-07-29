# Schema for Text-to-Image generation
from pydantic import BaseModel, Field
from typing import Literal

class Text2VideoInput(BaseModel):
    """Input model for text-to-video generation."""
    prompt: str = Field(...,
        json_schema_extra={"x-sr-order": 200},
        max_length=2500,
        description='The prompt for the video'
    )

    aspect_ratio: Literal['16:9', '9:16'] = Field(
        '16:9',
        json_schema_extra={"x-sr-order": 401},
        description='Aspect ratio of the video'
    )

    duration: int = Field(
        5,
        ge=5,
        le=8,
        multiple_of=1,
        json_schema_extra={"x-sr-order": 402},
        description='Duration of the video in seconds'
    )
