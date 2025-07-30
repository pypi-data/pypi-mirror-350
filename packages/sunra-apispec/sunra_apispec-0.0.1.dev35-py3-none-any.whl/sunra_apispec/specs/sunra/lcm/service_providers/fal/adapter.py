from sunra_apispec.base.adapter_interface import IFalAdapter
from ...sunra_schema import TextToImageInput
from .schema import FalInput


class FalTextToImageAdapter(IFalAdapter):
    """Adapter for image-to-video generation using Tencent Hunyuan Video model on FAL."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert from Sunra's ImageToVideoInput to FAL's input format."""
        # Validate the input data if required
        if not skip_validation:
            input_model = TextToImageInput.model_validate(data)
        else:
            input_model = TextToImageInput.model_construct(**data)
        
        # Create FalInput instance with mapped values
        fal_input = FalInput(
            prompt=input_model.prompt,
        )
        
        # Convert to dict, excluding None values
        return fal_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_fal_model(self) -> str:
        """Return the FAL model identifier."""
        return "fal-ai/lcm"
    
    def convert_output(self, data: dict) -> list[str]:
        """Convert the FAL output to the format expected by Sunra."""
        # Extract the video URL from the output
        if isinstance(data, dict) and "images" in data:
            return [file['url'] for file in data["images"]]
        raise ValueError(f"Invalid output {data}")
