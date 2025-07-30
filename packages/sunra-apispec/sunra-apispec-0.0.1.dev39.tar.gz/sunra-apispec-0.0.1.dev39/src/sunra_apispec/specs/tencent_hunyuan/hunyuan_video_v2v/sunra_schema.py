from pydantic import BaseModel, Field
from pydantic import HttpUrl

class VideoToVideoInput(BaseModel):
    prompt: str = Field(
        ...,
        json_schema_extra={"x-sr-order": 201},
        description="Text prompt describing the desired video.",
    )

    video: HttpUrl | str = Field(
        ...,
        title="Video",
        json_schema_extra={"x-sr-order": 202},
        description="Path to the video to use for video generation.",
    )
