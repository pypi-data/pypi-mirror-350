from sunra_apispec.base.adapter_interface import IFalAdapter
from ...sunra_schema import PikascenesInput
from .schema import FalInput, PikaImage


class FalPikascenesAdapter(IFalAdapter):
    """Adapter for Pikascenes video generation using Pika 2.2 model on FAL."""
    
    def convert_input(self, data: dict, skip_validation: bool = True) -> dict:
        """Convert from Sunra's PikascenesInput to FAL's input format."""
        # Validate the input data if required
        if not skip_validation:
            input_model = PikascenesInput.model_validate(data)
        else:
            input_model = PikascenesInput.model_construct(**data)
        
        # Convert image items to the format expected by FAL
        pika_images = []
        for img in input_model.images:
            pika_images.append(PikaImage(image_url=img.image_url))
        
        # Create FalInput instance with mapped values
        fal_input = FalInput(
            prompt=input_model.prompt,
            images=pika_images,
            aspect_ratio=input_model.aspect_ratio,
            resolution=input_model.resolution,
            ingredients_mode=input_model.ingredients_mode,
        )
        
        # Convert to dict, excluding None values
        return fal_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_fal_model(self) -> str:
        """Return the FAL model identifier."""
        return "fal-ai/pika/v2.2/pikascenes"
    
    def convert_output(self, data: dict) -> str:
        """Convert the FAL output to the format expected by Sunra."""
        # Extract the video URL from the output
        if isinstance(data, dict) and "video" in data and "url" in data["video"]:
            return data["video"]["url"]
        raise ValueError(f"Invalid output {data}")
