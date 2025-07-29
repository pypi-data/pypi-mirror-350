from sunra_apispec.base.adapter_interface import IReplicateAdapter
from ...sunra_schema import Text2ImageInput
from .schema import ReplicateInput


class ReplicateTextToImageAdapter(IReplicateAdapter):
    """Adapter for text-to-image generation using Photo Flash model on Replicate."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert from Sunra's Text2ImageInput to Replicate's input format."""
        # Validate the input data if required
        if not skip_validation:
            input_model = Text2ImageInput.model_validate(data)
        else:
            input_model = Text2ImageInput.model_construct(**data)
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            aspect_ratio=input_model.aspect_ratio,
            image_reference_url=input_model.image_reference,
            image_reference_weight=input_model.image_reference_weight,
            style_reference_url=input_model.style_reference,
            style_reference_weight=input_model.style_reference_weight,
            character_reference_url=input_model.character_reference,
            seed=input_model.seed
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_replicate_model(self) -> str:
        """Return the Replicate model identifier."""
        return "luma/photon-flash" 