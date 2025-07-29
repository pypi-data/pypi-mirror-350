"""
Adapter for Vidu Official Vidu1.5 API service provider.
Converts Sunra schema to Vidu Official API format.
"""

from sunra_apispec.base.adapter_interface import IViduAdapter
from ...sunra_schema import TextToVideoInput, ImageToVideoInput
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
            input_model = TextToVideoInput.model_validate(data)
        else:
            input_model = TextToVideoInput.model_construct(**data)
            
        vidu_input = ViduTextToVideoInput(
            model=ModelEnum.VIDU1_5.value,
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
            input_model = ImageToVideoInput.model_validate(data)
        else:
            input_model = ImageToVideoInput.model_construct(**data)
        
        if input_model.start_image and input_model.end_image:
            # Use StartEndToVideoInput format
            vidu_input = ViduStartEndToVideoInput(
                model=ModelEnum.VIDU1_5.value,
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
                model=ModelEnum.VIDU1_5.value,
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
        return "https://api.vidu.com/ent/v2/image2video" 
