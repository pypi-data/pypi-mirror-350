from sunra_apispec.base.adapter_interface import IReplicateAdapter
from ...sunra_schema import TextToVideoInput
from .schema import ReplicateInput


class ReplicateTextToVideoAdapter(IReplicateAdapter):
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        # Validate the input data if required
        if not skip_validation:
            input_model = TextToVideoInput.model_validate(data)
        else:
            input_model = TextToVideoInput.model_construct(**data)

        # Map fast_mode from "On"/"Off" to Replicate's options
        fast_mode_mapping = {
            "Off": "Balanced",
            "On": "Fast"  # Map "On" to "Fast" as default acceleration level
        }
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            seed=input_model.seed,
            sample_steps=input_model.number_of_steps,
            sample_guide_scale=input_model.guidance_scale,
            aspect_ratio=input_model.aspect_ratio,
            num_frames=input_model.number_of_frames,
            frames_per_second=input_model.frames_per_second,
            fast_mode=fast_mode_mapping.get(input_model.fast_mode, "Balanced")
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True)

    def get_replicate_model(self) -> str:
        return "wavespeedai/wan-2.1-t2v-480p"
