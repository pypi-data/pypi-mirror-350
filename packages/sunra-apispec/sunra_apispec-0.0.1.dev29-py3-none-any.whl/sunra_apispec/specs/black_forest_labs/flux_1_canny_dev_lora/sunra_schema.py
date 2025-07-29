# Schema for Image-to-Image generation with Canny control (LoRA version)
from pydantic import BaseModel, Field, HttpUrl
from typing import Literal


class Image2ImageInput(BaseModel):
    """Input model for image-to-image generation with canny control (LoRA version)."""
    prompt: str = Field(
        ...,
        json_schema_extra={"x-sr-order": 200},
        description="Text prompt for image generation",
    )
    number_of_steps: int = Field(
        default=30,  # Further reduced number_of_steps for dev-lora version
        ge=15,
        le=50,
        multiple_of=1,
        json_schema_extra={"x-sr-order": 201},
        description="Number of steps for the image generation process"
    )
    guidance_scale: float = Field(
        default=30,  # Lower guidance_scale for dev-lora version
        ge=1.0,
        le=100.0,
        multiple_of=1,
        json_schema_extra={"x-sr-order": 202},
        description="Guidance strength for the image generation process"
    )
    seed: int = Field(
        default=None,
        json_schema_extra={"x-sr-order": 203},
        description="Optional seed for reproducibility",
        examples=[42]
    )
    control_image: HttpUrl | str = Field(
        ...,
        json_schema_extra={"x-sr-order": 301},
        description="Image used to control the generation. The canny edge detection will be automatically generated."
    )
