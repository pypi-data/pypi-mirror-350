from ...sunra_schema import (
    TextToVideoInput,
    ImageToVideoInput,
    ReferenceImagesToVideoInput,
    VideoToVideoInput,
    VideoInpaintingInput,
)
from .schema import ReplicateInput
from sunra_apispec.base.adapter_interface import IReplicateAdapter

def get_speed_mode(motion):
    return {
        "consistent": "Lightly Juiced 🍋 (more consistent)",
        "fast": "Juiced 🍊 (default)",
        "extra_fast": "Extra Juiced 🍊 (more speed)"
    }[motion]


def get_size(resolution, aspect_ratio):
    if resolution == "480p":
        if aspect_ratio == "16:9":
            return "832*480"
        elif aspect_ratio == "9:16":
            return "480*832"
        else:
            return "832*480"
    elif resolution == "720p":
        if aspect_ratio == "16:9":
            return "1280*720"
        elif aspect_ratio == "9:16":
            return "720*1280"
        else:
            return "1280*720"
    else:
        return "1280*720"

class ReplicateTextToVideoAdapter(IReplicateAdapter):    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        # Validate the input data if required
        if not skip_validation:
            input_model = TextToVideoInput.model_validate(data)
        else:
            input_model = TextToVideoInput.model_construct(**data)
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            seed=input_model.seed,
            frame_num=input_model.number_of_frames,
            sample_steps=input_model.number_of_steps,
            sample_guide_scale=input_model.guidance_scale,
            speed_mode=get_speed_mode(input_model.motion),
            size=get_size(input_model.resolution, input_model.aspect_ratio),
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True) 
    
    def get_replicate_model(self) -> str:
        return "prunaai/vace-14b:bbafc615de3e3903470a335f94294810ced166309adcba307ac8692113a7b273"


class ReplicateImageToVideoAdapter(IReplicateAdapter):    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        # Validate the input data if required
        if not skip_validation:
            input_model = ImageToVideoInput.model_validate(data)
        else:
            input_model = ImageToVideoInput.model_construct(**data)

        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            seed=input_model.seed,
            frame_num=input_model.number_of_frames,
            sample_steps=input_model.number_of_steps,
            sample_guide_scale=input_model.guidance_scale,
            speed_mode=get_speed_mode(input_model.motion),
            size=get_size(input_model.resolution, input_model.aspect_ratio),
            src_ref_images=[input_model.start_image],
        )

        return replicate_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_replicate_model(self) -> str:
        return "prunaai/vace-14b:bbafc615de3e3903470a335f94294810ced166309adcba307ac8692113a7b273"


class ReplicateReferenceImagesToVideoAdapter(IReplicateAdapter):    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        # Validate the input data if required
        if not skip_validation:
            input_model = ReferenceImagesToVideoInput.model_validate(data)
        else:
            input_model = ReferenceImagesToVideoInput.model_construct(**data)
        
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            seed=input_model.seed,
            frame_num=input_model.number_of_frames,
            sample_steps=input_model.number_of_steps,
            sample_guide_scale=input_model.guidance_scale,
            speed_mode=get_speed_mode(input_model.motion),
            size=get_size(input_model.resolution, input_model.aspect_ratio),
            src_ref_images=input_model.reference_images,
        )
        
        return replicate_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_replicate_model(self) -> str:
        return "prunaai/vace-14b:bbafc615de3e3903470a335f94294810ced166309adcba307ac8692113a7b273"


class ReplicateVideoToVideoAdapter(IReplicateAdapter):    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        # Validate the input data if required
        if not skip_validation:
            input_model = VideoToVideoInput.model_validate(data)
        else:
            input_model = VideoToVideoInput.model_construct(**data)
        
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            seed=input_model.seed,
            frame_num=input_model.number_of_frames,
            sample_steps=input_model.number_of_steps,
            sample_guide_scale=input_model.guidance_scale,
            speed_mode=get_speed_mode(input_model.motion),
            size=get_size(input_model.resolution, input_model.aspect_ratio),
            src_video=input_model.video,
        )
        
        return replicate_input.model_dump(exclude_none=True, by_alias=True)

    def get_replicate_model(self) -> str:
        return "prunaai/vace-14b:bbafc615de3e3903470a335f94294810ced166309adcba307ac8692113a7b273"


class ReplicateVideoInpaintingAdapter(IReplicateAdapter):    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        # Validate the input data if required
        if not skip_validation:
            input_model = VideoInpaintingInput.model_validate(data)
        else:
            input_model = VideoInpaintingInput.model_construct(**data)
        
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            seed=input_model.seed,
            frame_num=input_model.number_of_frames,
            sample_steps=input_model.number_of_steps,
            sample_guide_scale=input_model.guidance_scale,
            speed_mode=get_speed_mode(input_model.motion),
            size=get_size(input_model.resolution, input_model.aspect_ratio),
            src_video=input_model.video,
            src_mask=input_model.mask,
        )
        
        return replicate_input.model_dump(exclude_none=True, by_alias=True)

    def get_replicate_model(self) -> str:
        return "prunaai/vace-14b:bbafc615de3e3903470a335f94294810ced166309adcba307ac8692113a7b273"
