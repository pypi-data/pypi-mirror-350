"""
Adapter for FLUX.1-Redux-Dev Replicate API service provider.
Converts Sunra schema to Replicate API format.
"""

from sunra_apispec.base.adapter_interface import IReplicateAdapter
from ...sunra_schema import ImageToImageInput
from .schema import ReplicateInput, OutputFormatEnum, MegapixelsEnum


class ReplicateImageToImageAdapter(IReplicateAdapter):
    """Adapter for image-to-image generation using FLUX.1-Redux-Dev on Replicate."""
    
    def convert_input(self, data: dict) -> dict:
        """Convert Sunra ImageToImageInput to Replicate input format."""
        input_model = ImageToImageInput.model_validate(data)
            
        # Map output format
        output_format_mapping = {
            "jpeg": OutputFormatEnum.JPG,
            "png": OutputFormatEnum.PNG
        }
        
        # Map megapixels
        megapixels_mapping = {
            "1": MegapixelsEnum.ONE,
            "0.25": MegapixelsEnum.QUARTER
        }
        
        replicate_input = ReplicateInput(
            redux_image=str(input_model.image),
            aspect_ratio=input_model.aspect_ratio,
            num_outputs=input_model.number_of_images,
            num_inference_steps=input_model.number_of_steps,
            guidance=input_model.guidance_scale,
            seed=input_model.seed,
            output_format=output_format_mapping.get(input_model.output_format, OutputFormatEnum.JPG),
            output_quality=80,  # Default quality
            disable_safety_checker=False,  # Default safety
            megapixels=megapixels_mapping.get(input_model.megapixels, MegapixelsEnum.ONE)
        )
        
        return replicate_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_replicate_model(self) -> str:
        """Return the Replicate model identifier."""
        return "black-forest-labs/flux-redux-dev" 

    def convert_output(self, data: dict) -> str | list[str]:
        """Convert Replicate output to Sunra output format."""
        return data
