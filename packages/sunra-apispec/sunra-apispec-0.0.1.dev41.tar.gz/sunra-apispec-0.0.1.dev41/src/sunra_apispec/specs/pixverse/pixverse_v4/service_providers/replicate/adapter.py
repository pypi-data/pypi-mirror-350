from sunra_apispec.base.adapter_interface import IReplicateAdapter
from ...sunra_schema import TextToVideoInput, ImageToVideoInput, EffectInput
from .schema import ReplicateInput


class ReplicateTextToVideoAdapter(IReplicateAdapter):
    """Adapter for text-to-video generation using Pixverse v4 model on Replicate."""
    
    def convert_input(self, data: dict) -> dict:
        """Convert from Sunra's TextToVideoInput to Replicate's input format."""
        # Validate the input data if required
        input_model = TextToVideoInput.model_validate(data)
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            negative_prompt=input_model.negative_prompt,
            quality=input_model.resolution,
            duration=input_model.duration,
            motion_mode=input_model.motion,
            style=input_model.style,
            seed=input_model.seed
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_replicate_model(self) -> str:
        """Return the Replicate model identifier."""
        return "pixverse/pixverse-v4"

    def convert_output(self, data: dict) -> str | list[str]:
        """Convert Replicate output to Sunra output format."""
        return data


class ReplicateImageToVideoAdapter(IReplicateAdapter):
    """Adapter for image-to-video generation using Pixverse v4 model on Replicate."""
    
    def convert_input(self, data: dict) -> dict:
        """Convert from Sunra's ImageToVideoInput to Replicate's input format."""
        # Validate the input data
        input_model = ImageToVideoInput.model_validate(data)
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            negative_prompt=input_model.negative_prompt,
            image=input_model.start_image,
            last_frame_image=input_model.end_image,
            quality=input_model.resolution,
            duration=input_model.duration,
            motion_mode=input_model.motion,
            style=input_model.style,
            seed=input_model.seed
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_replicate_model(self) -> str:
        """Return the Replicate model identifier."""
        return "pixverse/pixverse-v4"

    def convert_output(self, data: dict) -> str | list[str]:
        """Convert Replicate output to Sunra output format."""
        return data


class ReplicateEffectAdapter(IReplicateAdapter):
    """Adapter for effect generation using Pixverse v4 model on Replicate."""
    
    def convert_input(self, data: dict) -> dict:
        """Convert from Sunra's EffectInput to Replicate's input format."""
        # Validate the input data
        input_model = EffectInput.model_validate(data)
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            negative_prompt=input_model.negative_prompt,
            image=input_model.start_image,
            effect=input_model.effects,
            quality=input_model.resolution,
            duration=input_model.duration,
            motion_mode=input_model.motion,
            style=input_model.style,
            seed=input_model.seed
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_replicate_model(self) -> str:
        """Return the Replicate model identifier."""
        return "pixverse/pixverse-v4" 
    
    def convert_output(self, data: dict) -> str | list[str]:
        """Convert Replicate output to Sunra output format."""
        return data
