from sunra_apispec.base.adapter_interface import IReplicateAdapter
from ...sunra_schema import VideoInpaintingInput
from .schema import ReplicateInput


class ReplicateVideoInpaintingAdapter(IReplicateAdapter):
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        # Validate the input data if required
        if not skip_validation:
            input_model = VideoInpaintingInput.model_validate(data)
        else:
            input_model = VideoInpaintingInput.model_construct(**data)
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            input_video=input_model.video,
            prompt=input_model.prompt,
            mask_video=input_model.mask,
            seed=input_model.seed,
            strength=input_model.strength,
            expand_mask=input_model.expand_mask,
            guide_scale=input_model.guidance_scale,
            sampling_steps=input_model.number_of_steps,
            frames_per_second=input_model.frames_per_second,
            keep_aspect_ratio=input_model.keep_aspect_ratio,
            inpaint_fixup_steps=input_model.inpaint_fixup_steps,
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True) 

    def get_replicate_model(self) -> str:
        return "andreasjansson/wan-1.3b-inpaint:7abfdb3370aba087f9a5eb8b733c2174bc873a957e5c2c4835767247287dbf89"

