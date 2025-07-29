from typing import List
from pydantic import BaseModel, Field

class File(BaseModel):
    content_type: str = Field(
        ...,
        description='The mime type of the file.',
        title='Content Type',
    )
    file_name: str = Field(
        ...,
        description='The name of the file. It will be auto-generated if not provided.',
        title='File Name',
    )
    file_size: int = Field(
        ...,
        description='The size of the file in bytes.',
        title='File Size',
    )
    url: str = Field(
        ...,
        description='The URL where the file can be downloaded from.',
        title='Url',
    )

class VideoOutput(BaseModel):
    video: File

class VideosOutput(BaseModel):
    videos: List[VideoOutput]

class ImageOutput(BaseModel):
    image: File

class ImagesOutput(BaseModel):
    images: List[ImageOutput]


class AudioOutput(BaseModel):
    audio: File

class AudioOutputs(BaseModel):
    audios: List[AudioOutput]

class ModelOutput(BaseModel):
    model: File

class ModelsOutput(BaseModel):
    models: List[ModelOutput]
