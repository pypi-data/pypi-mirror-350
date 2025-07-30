"""
Adapter for Black Forest Labs Official FLUX 1.0 Fill Pro API service provider.
Converts Sunra schema to BFL Official API format.
"""

import base64
from pydantic import HttpUrl
import requests
from sunra_apispec.base.adapter_interface import IBlackForestLabsAdapter
from ...sunra_schema import ImageToImageInput
from .schema import BFLFluxV1FillProInput, OutputFormat


class BFLFluxV1FillImageToImageProAdapter(IBlackForestLabsAdapter):
    """Adapter for FLUX 1.0 Fill Pro image-to-image generation using BFL Official API."""
    
    def convert_input(self, data: dict) -> dict:
        """Convert Sunra ImageToImageInput to BFL Official BFLFluxV1FillProInput format."""
        input_model = ImageToImageInput.model_validate(data)
        
        bfl_input = BFLFluxV1FillProInput(
            image=self._convert_image_to_base64(input_model.image),
            mask=self._convert_image_to_base64(input_model.mask) if input_model.mask else None,
            prompt=input_model.prompt,
            steps=input_model.number_of_steps,
            prompt_upsampling=input_model.prompt_enhancer,
            seed=input_model.seed,
            guidance=input_model.guidance_scale,
            output_format=OutputFormat.JPEG if input_model.output_format == "jpeg" else OutputFormat.PNG,
            safety_tolerance=input_model.safety_tolerance,
        )
        
        return bfl_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_bfl_model(self) -> str:
        """Get the BFL model identifier for FLUX 1.0 Fill Pro."""
        return "flux-pro-fill" 
    
    def convert_output(self, data: dict) -> list[str]:
        """Convert BFL Official output to Sunra output format."""
        return [data["result"]["sample"]]

    def _convert_image_to_base64(self, image: HttpUrl | str) -> str:
        """Convert image URL or base64 string to base64 encoded string.
        
        Args:
            image: Either a HTTP URL or base64 encoded string
        
        Returns:
            Base64 encoded string of the image
        
        Raises:
            ValueError: If input is invalid or image cannot be fetched
        """
        if isinstance(image, HttpUrl) or image.startswith(('http')):
            try:
                # Fetch image from URL
                response = requests.get(str(image))
                response.raise_for_status()

                # Get content type from headers (default to 'image/png' if missing)
                content_type = response.headers.get('Content-Type', 'image/png')
                
                # Encode binary data to base64
                base64_data = base64.b64encode(response.content).decode('utf-8')
                return f"data:{content_type};base64,{base64_data}"
            except Exception as e:
                raise ValueError(f"Failed to fetch image from URL: {e}")
        elif isinstance(image, str) and image.startswith(('data:image')):
            return image
        else: 
            raise ValueError("Input must be either HttpUrl or base64 string")
    
    def _convert_aspect_ratio(self, aspect_ratio: str, width: int = None, height: int = None) -> tuple[int, int]:
        """Convert aspect ratio to width and height."""
        if aspect_ratio == "custom" and width and height:
            return width, height
        
        aspect_ratios = {
            "1:1": (640, 640),
            "16:9": (1024, 576),
            "9:16": (576, 1024),
            "4:3": (1024, 768),
            "3:4": (768, 1024),
            "21:9": (1216, 512),
            "9:21": (512, 1216),
        }
        
        return aspect_ratios.get(aspect_ratio, (1024, 576)) 
