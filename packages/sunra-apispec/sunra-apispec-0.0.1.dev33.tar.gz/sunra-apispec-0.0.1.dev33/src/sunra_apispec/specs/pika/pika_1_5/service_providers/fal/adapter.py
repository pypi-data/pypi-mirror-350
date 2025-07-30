from sunra_apispec.base.adapter_interface import IFalAdapter
from ...sunra_schema import PikaffectsInput
from .schema import FalInput


class FalPikaffectsAdapter(IFalAdapter):
    """Adapter for Pikaffects effect generation using Pika 1.5 model on FAL."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert from Sunra's PikaffectsInput to FAL's input format."""
        # Validate the input data if required
        if not skip_validation:
            input_model = PikaffectsInput.model_validate(data)
        else:
            input_model = PikaffectsInput.model_construct(**data)
        
        # Create FalInput instance with mapped values
        fal_input = FalInput(
            prompt=input_model.prompt,
            image_url=input_model.image,
            pikaffect=input_model.pikaffect,
        )
        
        # Convert to dict, excluding None values
        return fal_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_fal_model(self) -> str:
        """Return the FAL model identifier."""
        return "fal-ai/pika/v1.5/pikaffects"
    
    def convert_output(self, data: dict) -> str:
        """Convert the FAL output to the format expected by Sunra."""
        # Extract the video URL from the output
        if isinstance(data, dict) and "video" in data and "url" in data["video"]:
            return data["video"]["url"]
        raise ValueError(f"Invalid output {data}")
