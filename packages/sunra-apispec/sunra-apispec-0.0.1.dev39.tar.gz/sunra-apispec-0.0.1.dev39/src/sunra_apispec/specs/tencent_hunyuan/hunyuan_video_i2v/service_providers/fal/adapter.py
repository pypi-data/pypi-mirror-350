from sunra_apispec.base.adapter_interface import IFalAdapter
from ...sunra_schema import ImageToVideoInput
from .schema import FalInput


class FalImageToVideoAdapter(IFalAdapter):
    """Adapter for image-to-video generation using Tencent Hunyuan Video model on FAL."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert from Sunra's ImageToVideoInput to FAL's input format."""
        # Validate the input data if required
        if not skip_validation:
            input_model = ImageToVideoInput.model_validate(data)
        else:
            input_model = ImageToVideoInput.model_construct(**data)
        
        # Create FalInput instance with mapped values
        fal_input = FalInput(
            prompt=input_model.prompt,
            image_url=input_model.start_image,
            # Using default values for the rest of the parameters
            aspect_ratio="16:9",
            resolution="720p",
            num_frames=129,
            i2v_stability=False,
        )
        
        # Convert to dict, excluding None values
        return fal_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_fal_model(self) -> str:
        """Return the FAL model identifier."""
        return "fal-ai/hunyuan-video-image-to-video"
    
    def convert_output(self, data: dict) -> str:
        """Convert the FAL output to the format expected by Sunra."""
        # Extract the video URL from the output
        if isinstance(data, dict) and "video" in data and "url" in data["video"]:
            return data["video"]["url"]
        raise ValueError(f"Invalid output {data}")
    