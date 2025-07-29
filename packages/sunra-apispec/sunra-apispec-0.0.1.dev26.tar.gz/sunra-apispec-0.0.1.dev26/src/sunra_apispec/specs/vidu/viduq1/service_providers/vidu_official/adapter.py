"""
Adapter for Vidu Official ViduQ1 API service provider.
Converts Sunra schema to Vidu Official API format.
"""

from sunra_apispec.base.adapter_interface import IViduAdapter
from ...sunra_schema import Text2VideoInput, Image2VideoInput
from .schema import (
    ViduTextToVideoInput, 
    ViduImageToVideoInput, 
    ViduStartEndToVideoInput,
    ModelEnum,
)


class ViduTextToVideoAdapter(IViduAdapter):
    """Adapter for text-to-video generation using Vidu Official API."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert Sunra Text2VideoInput to Vidu Official TextToVideoInput format."""
        if not skip_validation:
            input_model = Text2VideoInput.model_validate(data)
        else:
            input_model = Text2VideoInput.model_construct(**data)
            
        vidu_input = ViduTextToVideoInput(
            model=ModelEnum.VIDUQ1.value,
            prompt=input_model.prompt,
            style=input_model.style,
            aspect_ratio=input_model.aspect_ratio,
            duration=input_model.duration,
            resolution=input_model.resolution,
            movement_amplitude=input_model.movement_amplitude,
            seed=input_model.seed,
        )
        
        return vidu_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_request_url(self) -> str:
        """Get the Vidu Official API endpoint URL for text-to-video."""
        return "https://api.vidu.com/ent/v2/text2video"


class ViduImageToVideoAdapter(IViduAdapter):
    """Adapter for image-to-video generation using Vidu Official API."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert Sunra Image2VideoInput to Vidu Official ImageToVideoInput or StartEndToVideoInput format."""
        if not skip_validation:
            input_model = Image2VideoInput.model_validate(data)
        else:
            input_model = Image2VideoInput.model_construct(**data)
            
        # Check if both start_image and end_image are provided
        if input_model.start_image and input_model.end_image:
            # Use StartEndToVideoInput format
            vidu_input = ViduStartEndToVideoInput(
                model=ModelEnum.VIDUQ1.value,
                prompt=input_model.prompt,
                images=[input_model.start_image, input_model.end_image],
                duration=input_model.duration,
                resolution=input_model.resolution,
                movement_amplitude=input_model.movement_amplitude,
                seed=input_model.seed,
            )
                
        else:
            # Use ImageToVideoInput format
            vidu_input = ViduImageToVideoInput(
                model=ModelEnum.VIDUQ1.value,
                prompt=input_model.prompt,
                images=[input_model.start_image],
                duration=input_model.duration,
                resolution=input_model.resolution,
                movement_amplitude=input_model.movement_amplitude,
                seed=input_model.seed,
            )
            
        return vidu_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_request_url(self) -> str:
        """Get the Vidu Official API endpoint URL for image-to-video."""
        return "https://api.vidu.com/ent/v2/img2video"
