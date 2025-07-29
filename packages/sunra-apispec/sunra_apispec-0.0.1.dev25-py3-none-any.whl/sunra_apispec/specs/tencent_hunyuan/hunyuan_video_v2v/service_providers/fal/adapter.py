from sunra_apispec.base.adapter_interface import IFalAdapter
from ...sunra_schema import VideoToVideoInput
from .schema import FalInput


class FalVideoToVideoAdapter(IFalAdapter):
    """Adapter for video-to-video generation using Tencent Hunyuan Video model on FAL."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert from Sunra's VideoToVideoInput to FAL's input format."""
        # Validate the input data if required
        if not skip_validation:
            input_model = VideoToVideoInput.model_validate(data)
        else:
            input_model = VideoToVideoInput.model_construct(**data)
        
        # Create FalInput instance with mapped values
        fal_input = FalInput(
            prompt=input_model.prompt,
            video_url=input_model.video,
            # Using default values for the rest of the parameters
            aspect_ratio="16:9",
            resolution="720p",
            strength=0.85,
            enable_safety_checker=False,
        )
        
        # Convert to dict, excluding None values
        return fal_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_fal_model(self) -> str:
        """Return the FAL model identifier."""
        return "fal-ai/hunyuan-video/video-to-video"
    
    def convert_output(self, data: dict) -> str:
        """Convert the FAL output to the format expected by Sunra."""
        # Extract the video URL from the output
        if isinstance(data, dict) and "video" in data and "url" in data["video"]:
            return data["video"]["url"]
        raise ValueError(f"Invalid output {data}")
