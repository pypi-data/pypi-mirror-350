from sunra_apispec.base.adapter_interface import IReplicateAdapter
from ...sunra_schema import TextLipSyncInput, AudioLipSyncInput
from .schema import ReplicateInput


class ReplicateTextToVideoAdapter(IReplicateAdapter):
    """Adapter for text-to-video lip sync using Kling Lip Sync model on Replicate."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert from Sunra's TextLipSyncInput to Replicate's input format."""
        # Validate the input data if required
        if not skip_validation:
            input_model = TextLipSyncInput.model_validate(data)
        else:
            input_model = TextLipSyncInput.model_construct(**data)
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            video_url=input_model.video,
            text=input_model.text,
            voice_id=input_model.voice_id,
            voice_speed=input_model.voice_speed
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_replicate_model(self) -> str:
        """Return the Replicate model identifier."""
        return "kwaivgi/kling-lip-sync"


class ReplicateAudioToVideoAdapter(IReplicateAdapter):
    """Adapter for audio-to-video lip sync using Kling Lip Sync model on Replicate."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert from Sunra's AudioLipSyncInput to Replicate's input format."""
        # Validate the input data if required
        if not skip_validation:
            input_model = AudioLipSyncInput.model_validate(data)
        else:
            input_model = AudioLipSyncInput.model_construct(**data)
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            video_url=input_model.video,
            audio_file=input_model.audio,
            voice_id=input_model.voice_id,
            voice_speed=input_model.voice_speed
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_replicate_model(self) -> str:
        """Return the Replicate model identifier."""
        return "kwaivgi/kling-lip-sync" 
