# Schema for Text-to-Image generation
from pydantic import BaseModel, Field
from typing import Literal


class Text2ImageInput(BaseModel):
    """Input model for text-to-image generation."""
    prompt: str = Field(
        ...,
        json_schema_extra={"x-sr-order": 200},
        max_length=2500,
        description='The prompt for the image'
    )

    prompt_enhancer: bool = Field(
        True,
        json_schema_extra={"x-sr-order": 201},
        description="Whether to use the model's prompt enhancer"
    )
    
    aspect_ratio: Literal['1:1', '16:9', '9:16', '4:3', '3:4'] = Field(
        '16:9',
        json_schema_extra={"x-sr-order": 401},
        description='Aspect ratio of the image'
    )

    number_of_images: int = Field(
        4,
        ge=1,
        le=4,
        multiple_of=1,
        json_schema_extra={"x-sr-order": 402},
        description='Number of images to generate'
    )

