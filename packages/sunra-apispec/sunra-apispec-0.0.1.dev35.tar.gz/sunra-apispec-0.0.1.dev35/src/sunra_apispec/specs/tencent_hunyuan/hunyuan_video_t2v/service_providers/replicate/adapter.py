from sunra_apispec.base.adapter_interface import IReplicateAdapter
from ...sunra_schema import TextToVideoInput
from .schema import ReplicateInput


class ReplicateTextToVideoAdapter(IReplicateAdapter):
    """Adapter for text-to-video generation using Tencent Hunyuan Video model on Replicate."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert from Sunra's TextToVideoInput to Replicate's input format."""
        # Validate the input data if required
        if not skip_validation:
            input_model = TextToVideoInput.model_validate(data)
        else:
            input_model = TextToVideoInput.model_construct(**data)
        
        # Determine width and height based on aspect_ratio and resolution
        width, height = self._get_dimensions(input_model)
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            infer_steps=input_model.number_of_steps,
            width=width,
            height=height,
            # Default value for video_length (can be customized later if needed)
            video_length=129,
            # Use embedded_guidance_scale of 6.0 as default (from Replicate schema)
            embedded_guidance_scale=6.0,
            # Use 24 FPS as default (from Replicate schema)
            fps=24,
            # No seed by default
            seed=None
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_replicate_model(self) -> str:
        """Return the Replicate model identifier."""
        return "tencent/hunyuan-video:6c9132aee14409cd6568d030453f1ba50f5f3412b844fe67f78a9eb62d55664f"
    
    def _get_dimensions(self, input_model: TextToVideoInput) -> tuple:
        """Determine video dimensions based on aspect ratio and resolution."""
        # Custom dimensions if explicitly provided
        if input_model.aspect_ratio == "custom" and input_model.width and input_model.height:
            return input_model.width, input_model.height
        
        # Standard dimensions based on aspect ratio and resolution
        if input_model.resolution == "480p":
            if input_model.aspect_ratio == "16:9":
                return 864, 480
            elif input_model.aspect_ratio == "9:16":
                return 480, 864
            elif input_model.aspect_ratio == "1:1":
                return 480, 480
        elif input_model.resolution == "720p":
            if input_model.aspect_ratio == "16:9":
                return 1280, 720
            elif input_model.aspect_ratio == "9:16":
                return 720, 1280
            elif input_model.aspect_ratio == "1:1":
                return 768, 768
        
        # Default fallback
        return 864, 480
