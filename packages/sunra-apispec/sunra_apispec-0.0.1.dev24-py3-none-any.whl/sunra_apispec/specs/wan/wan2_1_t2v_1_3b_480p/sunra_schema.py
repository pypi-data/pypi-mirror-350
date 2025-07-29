# Schema for Text-to-Video generation
from pydantic import BaseModel, Field
from typing import Literal

class TextToVideoInput(BaseModel):
    """Input model for text-to-video generation."""
    prompt: str = Field(
        ...,
        json_schema_extra={"x-sr-order": 201},
        description="Text prompt for video generation.",
    )
    
    number_of_steps: int = Field(
        default=30,
        ge=10,
        le=50,
        multiple_of=1,
        json_schema_extra={"x-sr-order": 204},
        description="Number of sampling steps (higher = better quality but slower).",
    )
    
    guidance_scale: float = Field(
        default=6.0,
        ge=0,
        le=20.0,
        multiple_of=0.1,
        json_schema_extra={"x-sr-order": 205},
        description="Classifier free guidance scale (higher values strengthen prompt adherence).",
    )
    
    seed: int = Field(
        default=None,
        json_schema_extra={"x-sr-order": 206},
        description="Random seed for reproducibility (leave blank for random).",
    )
    
    aspect_ratio: Literal["16:9", "9:16"] = Field(
        "16:9",
        json_schema_extra={"x-sr-order": 401},
        description="Aspect ratio of video. 16:9 corresponds to landscape, and 9:16 is portrait.",
    )
    
    number_of_frames: Literal[17, 33, 49, 65, 81] = Field(
        default=81,
        json_schema_extra={"x-sr-order": 404},
        description="Video duration in frames (based on standard 16fps playback).",
    )
