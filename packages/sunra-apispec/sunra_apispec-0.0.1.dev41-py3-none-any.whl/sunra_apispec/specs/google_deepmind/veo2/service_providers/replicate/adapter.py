from sunra_apispec.base.adapter_interface import IReplicateAdapter
from ...sunra_schema import TextToVideoInput, ImageToVideoInput
from .schema import ReplicateVeo2Input


class ReplicateTextToVideoAdapter(IReplicateAdapter):
    """Adapter for text-to-video generation using Veo2 model on Replicate."""
    
    def convert_input(self, data: dict) -> dict:
        """Convert from Sunra's TextToVideoInput to Replicate's input format."""
        # Validate the input data
        input_model = TextToVideoInput.model_validate(data)
        
        # Create Replicate Input instance with mapped values
        replicate_input = ReplicateVeo2Input(
            prompt=input_model.prompt,
            aspect_ratio=input_model.aspect_ratio,
            duration=input_model.duration,
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_replicate_model(self) -> str:
        """Return the Replicate model identifier."""
        return "google/veo-2"
    
    def convert_output(self, data: dict) -> str | list[str]:
        """Convert Replicate output to Sunra output format."""
        return data


class ReplicateImageToVideoAdapter(IReplicateAdapter):
    """Adapter for image-to-video generation using Veo2 model on Replicate."""
    
    def convert_input(self, data: dict) -> dict:
        """Convert from Sunra's ImageToVideoInput to Replicate's input format."""
        # Validate the input data
        input_model = ImageToVideoInput.model_validate(data)
        
        # Create Replicate Input instance with mapped values
        replicate_input = ReplicateVeo2Input(
            prompt=input_model.prompt,
            image=input_model.image,
            aspect_ratio=input_model.aspect_ratio,
            duration=input_model.duration,
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_replicate_model(self) -> str:
        """Return the Replicate model identifier."""
        return "google/veo-2" 
    
    def convert_output(self, data: dict) -> str | list[str]:
        """Convert Replicate output to Sunra output format."""
        return data
