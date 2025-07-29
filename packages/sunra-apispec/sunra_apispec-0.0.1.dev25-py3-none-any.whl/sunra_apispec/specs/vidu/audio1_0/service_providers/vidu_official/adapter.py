"""
Adapter for Vidu Official Audio1.0 API service provider.
Converts Sunra schema to Vidu Official API format.
"""

from sunra_apispec.base.adapter_interface import IViduAdapter
from ...sunra_schema import Text2AudioInput, Timing2VideoInput
from .schema import TextToAudioInput, TimingToAudioInput, TimingPrompt, AudioModelEnum


class ViduTextToAudioAdapter(IViduAdapter):
    """Adapter for text-to-audio generation using Vidu Official API."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert Sunra Text2AudioInput to Vidu Official TextToAudioInput format."""
        if not skip_validation:
            input_model = Text2AudioInput.model_validate(data)
        else:
            input_model = Text2AudioInput.model_construct(**data)
            
        vidu_input = TextToAudioInput(
            model=AudioModelEnum.AUDIO1_0.value,
            prompt=input_model.prompt,
            seed=input_model.seed,
            duration=input_model.duration,
        )
        
        return vidu_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_request_url(self) -> str:
        """Get the Vidu Official API endpoint URL for text-to-audio."""
        return "https://api.vidu.com/ent/v2/text2audio"


class ViduTimingToAudioAdapter(IViduAdapter):
    """Adapter for timing-to-audio generation using Vidu Official API."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert Sunra Timing2VideoInput to Vidu Official TimingToAudioInput format."""
        if not skip_validation:
            input_model = Timing2VideoInput.model_validate(data)
        else:
            input_model = Timing2VideoInput.model_construct(**data)
            
        # Convert timing prompts format
        timing_prompts = []
        for timing_prompt in input_model.timing_prompts:
            timing_prompts.append(
                TimingPrompt(
                    from_time=timing_prompt.from_second,
                    to_time=timing_prompt.to_second,
                    prompt=timing_prompt.prompt
                )
            )
            
        vidu_input = TimingToAudioInput(
            model=AudioModelEnum.AUDIO1_0.value,
            duration=input_model.duration,
            timing_prompts=timing_prompts,
            seed=input_model.seed,
        )
        
        return vidu_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_request_url(self) -> str:
        """Get the Vidu Official API endpoint URL for timing-to-audio."""
        return "https://api.vidu.com/ent/v2/timing2audio" 
