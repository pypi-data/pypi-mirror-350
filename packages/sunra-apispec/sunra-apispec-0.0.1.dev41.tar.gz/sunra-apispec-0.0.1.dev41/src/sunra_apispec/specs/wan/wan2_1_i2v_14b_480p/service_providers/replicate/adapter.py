from sunra_apispec.base.adapter_interface import IReplicateAdapter
from ...sunra_schema import ImageToVideoInput
from .schema import ReplicateInput

class ReplicateImageToVideoAdapter(IReplicateAdapter):
    """Mapper class to convert from ImageToVideoInput to Replicate API input format."""
    
    def convert_input(self, data: dict) -> dict:
        # Validate the input data
        input_model = ImageToVideoInput.model_validate(data)
        
        # Map fast_mode from "On"/"Off" to Replicate's options
        fast_mode_mapping = {
            "Off": "Balanced",
            "On": "Fast"  # Map "On" to "Fast" as default acceleration level
        }
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            image=input_model.start_image,
            prompt=input_model.prompt,
            max_area=input_model.max_area,
            seed=input_model.seed,
            sample_steps=input_model.number_of_steps,
            sample_guide_scale=input_model.guidance_scale,
            num_frames=input_model.number_of_frames,
            frames_per_second=input_model.frames_per_second,
            fast_mode=fast_mode_mapping.get(input_model.fast_mode, "Balanced")
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True) 
    
    def get_replicate_model(self) -> str:
        return "wavespeedai/wan-2.1-i2v-480p"

    def convert_output(self, data: dict) -> str | list[str]:
        """Convert Replicate output to Sunra output format."""
        return data
