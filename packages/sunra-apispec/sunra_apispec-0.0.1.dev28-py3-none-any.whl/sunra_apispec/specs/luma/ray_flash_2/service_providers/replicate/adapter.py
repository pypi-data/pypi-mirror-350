from sunra_apispec.base.adapter_interface import IReplicateAdapter
from ...sunra_schema import Text2VideoInput, Image2VideoInput
from .schema import RayFlash2540PInput, RayFlash2720PInput


class ReplicateTextToVideoAdapter(IReplicateAdapter):
    """Adapter for text-to-video generation using Ray Flash 2 model on Replicate."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert from Sunra's Text2VideoInput to Replicate's input format."""
        # Validate the input data if required
        if not skip_validation:
            input_model = Text2VideoInput.model_validate(data)
        else:
            input_model = Text2VideoInput.model_construct(**data)
        
        if input_model.resolution == "720p":
            # Create Input instance with mapped values
            replicate_input = RayFlash2720PInput(
                prompt=input_model.prompt,
                duration=input_model.duration,
                aspect_ratio=input_model.aspect_ratio,
                loop=input_model.loop,
                concepts=input_model.concepts
            )
            self.model = "luma/ray-flash-2-720p"
        elif input_model.resolution == "540p":
            replicate_input = RayFlash2540PInput(
                prompt=input_model.prompt,
                duration=input_model.duration,
                aspect_ratio=input_model.aspect_ratio,
                loop=input_model.loop,
                concepts=input_model.concepts
            )
            self.model = "luma/ray-flash-2-540p"
        else:
            raise ValueError(f"Invalid resolution {input_model.resolution}")
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True)
    
    # This must be called after convert_input
    def get_replicate_model(self) -> str:
        """Return the Replicate model identifier based on resolution."""
        return self.model


class ReplicateImageToVideoAdapter(IReplicateAdapter):
    """Adapter for image-to-video generation using Ray Flash 2 model on Replicate."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert from Sunra's Image2VideoInput to Replicate's input format."""
        # Validate the input data if required
        if not skip_validation:
            input_model = Image2VideoInput.model_validate(data)
        else:
            input_model = Image2VideoInput.model_construct(**data)
        
        if input_model.resolution == "720p":
            # Create Input instance with mapped values
            replicate_input = RayFlash2720PInput(
                prompt=input_model.prompt,
                start_image_url=input_model.start_image,
                end_image_url=input_model.end_image,
                duration=input_model.duration,
                aspect_ratio=input_model.aspect_ratio,
                loop=input_model.loop,
                concepts=input_model.concepts
            )
            self.model = "luma/ray-flash-2-720p"
        elif input_model.resolution == "540p":
            replicate_input = RayFlash2540PInput(
                prompt=input_model.prompt,
                start_image_url=input_model.start_image,
                end_image_url=input_model.end_image,
                duration=input_model.duration,
                aspect_ratio=input_model.aspect_ratio,
                loop=input_model.loop,
                concepts=input_model.concepts
            )
            self.model = "luma/ray-flash-2-540p"
        else:
            raise ValueError(f"Invalid resolution {input_model.resolution}")
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True)
    
    # This must be called after convert_input
    def get_replicate_model(self) -> str:
        """Return the Replicate model identifier based on resolution."""
        return self.model
