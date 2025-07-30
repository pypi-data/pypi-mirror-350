"""
Adapter for Black Forest Labs Official FLUX 1.0 Depth Pro API service provider.
Converts Sunra schema to BFL Official API format.
"""

import base64
from pydantic import HttpUrl
import requests
from sunra_apispec.base.adapter_interface import IBlackForestLabsAdapter
from ...sunra_schema import ImageToImageInput
from .schema import BFLFluxV1DepthProInput, OutputFormat


class BFLFluxV1DepthProImageToImageAdapter(IBlackForestLabsAdapter):
    """Adapter for FLUX 1.0 Depth Pro image-to-image generation using BFL Official API."""
    
    def convert_input(self, data: dict) -> dict:
        """Convert Sunra ImageToImageInput to BFL Official BFLFluxV1DepthProInput format."""
        input_model = ImageToImageInput.model_validate(data)
        
        bfl_input = BFLFluxV1DepthProInput(
            prompt=input_model.prompt,
            control_image=self._convert_image_to_base64(input_model.control_image),
            preprocessed_image=self._convert_image_to_base64(input_model.preprocessed_image) if input_model.preprocessed_image else None,
            prompt_upsampling=input_model.prompt_enhancer,
            seed=input_model.seed,
            steps=input_model.number_of_steps,
            output_format=OutputFormat.JPEG if input_model.output_format == "jpeg" else OutputFormat.PNG,
            guidance=input_model.guidance_scale,
            safety_tolerance=input_model.safety_tolerance,
        )
        
        return bfl_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_bfl_model(self) -> str:
        """Get the BFL model identifier for FLUX 1.0 Depth Pro."""
        return "flux-pro-depth" 
    
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
