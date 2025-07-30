from sunra_apispec.base.adapter_interface import IReplicateAdapter
from ...sunra_schema import TextToImageInput
from .schema import ReplicateImagen3FastInput


class ReplicateTextToImageAdapter(IReplicateAdapter):
    """Adapter for text-to-image generation using Imagen3 Fast model on Replicate."""
    
    def convert_input(self, data: dict) -> dict:
        """Convert from Sunra's TextToImageInput to Replicate's input format."""
        # Validate the input data
        input_model = TextToImageInput.model_validate(data)
        
        # Create Replicate Input instance with mapped values
        replicate_input = ReplicateImagen3FastInput(
            prompt=input_model.prompt,
            aspect_ratio=input_model.aspect_ratio,
            safety_filter_level="block_only_high"
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_replicate_model(self) -> str:
        """Return the Replicate model identifier."""
        return "google/imagen-3-fast"
    
    def convert_output(self, data: dict) -> str | list[str]:
        """Convert Replicate output to Sunra output format."""
        return data
