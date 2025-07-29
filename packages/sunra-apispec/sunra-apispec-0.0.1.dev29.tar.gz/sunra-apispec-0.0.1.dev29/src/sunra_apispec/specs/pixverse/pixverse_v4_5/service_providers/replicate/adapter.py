from sunra_apispec.base.adapter_interface import IReplicateAdapter
from ...sunra_schema import Text2VideoInput, Image2VideoInput, EffectInput
from .schema import ReplicateInput


class ReplicateTextToVideoAdapter(IReplicateAdapter):
    """Adapter for text-to-video generation using Pixverse v4.5 model on Replicate."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert from Sunra's Text2VideoInput to Replicate's input format."""
        # Validate the input data if required
        if not skip_validation:
            input_model = Text2VideoInput.model_validate(data)
        else:
            input_model = Text2VideoInput.model_construct(**data)
        
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
        return "pixverse/pixverse-v4.5"


class ReplicateImageToVideoAdapter(IReplicateAdapter):
    """Adapter for image-to-video generation using Pixverse v4.5 model on Replicate."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert from Sunra's Image2VideoInput to Replicate's input format."""
        # Validate the input data if required
        if not skip_validation:
            input_model = Image2VideoInput.model_validate(data)
        else:
            input_model = Image2VideoInput.model_construct(**data)
        
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
        return "pixverse/pixverse-v4.5"


class ReplicateEffectsAdapter(IReplicateAdapter):
    """Adapter for applying effects using Pixverse v4.5 model on Replicate."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert from Sunra's EffectInput to Replicate's input format."""
        # Validate the input data if required
        if not skip_validation:
            input_model = EffectInput.model_validate(data)
        else:
            input_model = EffectInput.model_construct(**data)
        
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
        return "pixverse/pixverse-v4.5" 