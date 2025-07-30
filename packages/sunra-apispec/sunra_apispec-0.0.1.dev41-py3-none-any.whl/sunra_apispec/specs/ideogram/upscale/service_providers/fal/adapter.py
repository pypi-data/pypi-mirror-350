from sunra_apispec.base.adapter_interface import IFalAdapter
from ...sunra_schema import UpscaleInput
from .schema import FalUpscaleInput


class FalUpscaleAdapter(IFalAdapter):
    """Adapter for Ideogram upscale using FAL."""
    
    def convert_input(self, data: dict) -> dict:
        """Convert from Sunra's UpscaleInput to FAL's input format."""
        input_model = UpscaleInput.model_validate(data)
        
        # Create FalUpscaleInput instance with mapped values
        fal_input = FalUpscaleInput(
            image_url=input_model.image,
            prompt=input_model.prompt or "",
            detail=input_model.detail,
            resemblance=input_model.resemblance,
            expand_prompt=input_model.prompt_enhancer or False,
        )
        
        return fal_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_fal_model(self) -> str:
        """Return the FAL model identifier."""
        return "fal-ai/ideogram/upscale"
    
    def convert_output(self, data: dict) -> list[str]:
        """Convert the FAL output to the format expected by Sunra."""
        if isinstance(data, dict) and "images" in data:
            return [img["url"] for img in data["images"]]
        raise ValueError(f"Invalid output {data}")
