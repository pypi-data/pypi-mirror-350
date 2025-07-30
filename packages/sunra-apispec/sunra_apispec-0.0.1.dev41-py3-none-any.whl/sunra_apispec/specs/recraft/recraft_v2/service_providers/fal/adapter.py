from sunra_apispec.base.adapter_interface import IFalAdapter
from ...sunra_schema import TextToImageInput
from .schema import RecraftV2TextToImageInput


class FalTextToImageAdapter(IFalAdapter):
    """Adapter for Recraft V2 text-to-image generation using FAL."""
    
    def convert_input(self, data: dict) -> dict:
        """Convert from Sunra's TextToImageInput to FAL's input format."""
        input_model = TextToImageInput.model_validate(data)
        
        # Convert aspect ratio to image_size
        image_size = self._convert_aspect_ratio_to_image_size(input_model.aspect_ratio)
        
        # Create FAL input instance
        fal_input = RecraftV2TextToImageInput(
            prompt=input_model.prompt,
            image_size=image_size,
            style=input_model.style,
            style_id=input_model.style_id,
            enable_safety_checker=False,  # Default value
            colors=[],  # Default empty list
        )
        
        return fal_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_fal_model(self) -> str:
        """Return the FAL model identifier."""
        return "fal-ai/recraft/v2/text-to-image"
    
    def convert_output(self, data: dict) -> list[str]:
        """Convert the FAL output to the format expected by Sunra."""
        if isinstance(data, dict) and "images" in data:
            return [img["url"] for img in data["images"]]
        raise ValueError(f"Invalid output {data}")
    
    def _convert_aspect_ratio_to_image_size(self, aspect_ratio: str) -> str:
        """Convert Sunra aspect ratio to FAL image size."""
        if not aspect_ratio:
            return "square_hd"
        
        mapping = {
            "1:1": "square_hd",
            "4:3": "landscape_4_3",
            "3:4": "portrait_4_3",
            "16:9": "landscape_16_9",
            "9:16": "portrait_16_9",
        }
        return mapping.get(aspect_ratio, "square_hd") 
