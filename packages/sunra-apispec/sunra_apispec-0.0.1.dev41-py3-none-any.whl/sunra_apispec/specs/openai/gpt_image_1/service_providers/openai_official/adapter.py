"""
Adapter for OpenAI Official GPT Image 1 API service provider.
Converts Sunra schema to OpenAI Official API format.
"""

from sunra_apispec.base.adapter_interface import IOpenAIAdapter
from ...sunra_schema import TextToImageInput, ImageEditingInput
from .schema import OpenaiTextToImageInput, OpenaiImageEditingInput


class OpenAITextToImageAdapter(IOpenAIAdapter):
    """Adapter for text-to-image generation using OpenAI Official API."""
    
    def convert_input(self, data: dict) -> dict:
        """Convert Sunra TextToImageInput to OpenAI Official TextToImageInput format."""
        input_model = TextToImageInput.model_validate(data)
        
        # Map aspect ratio to size
        size_mapping = {
            "auto": "auto",
            "1:1": "1024x1024",
            "3:2": "1536x1024",
            "2:3": "1024x1536"
        }

        if input_model.background == "transparent":
            input_model.output_format = "png"
        
        openai_input = OpenaiTextToImageInput(
            prompt=input_model.prompt,
            model="gpt-image-1",
            size=size_mapping.get(input_model.aspect_ratio, "auto"),
            background=input_model.background,
            quality=input_model.quality,
            output_compression=input_model.output_compression,
            output_format=input_model.output_format,
            moderation="low",  # Hidden from users, defaults to "low"
            user=input_model.user,
        )
        
        return openai_input.model_dump(exclude_none=True, by_alias=True)
    
    def convert_output(self, data: dict) -> str | list[str]:
        """Convert OpenAI Official API response to Sunra format."""
        # OpenAI returns base64 encoded images for gpt-image-1
        if "data" in data and isinstance(data["data"], list):
            images = []
            for item in data["data"]:
                if "b64_json" in item:
                    images.append(item["b64_json"])
            return images if len(images) > 1 else images[0] if images else ""
        return ""
    
    def get_request_url(self) -> str:
        """Get the OpenAI Official API endpoint URL for text-to-image."""
        return "https://api.openai.com/v1/images/generations"



class OpenAIImageEditingAdapter(IOpenAIAdapter):
    """Adapter for image editing using OpenAI Official API."""
    
    def convert_input(self, data: dict) -> dict:
        """Convert Sunra ImageEditingInput to OpenAI Official ImageEditingInput format."""
        input_model = ImageEditingInput.model_validate(data)
        
        # Map aspect ratio to size
        size_mapping = {
            "auto": "auto",
            "1:1": "1024x1024",
            "3:2": "1536x1024",
            "2:3": "1024x1536"
        }
        
        openai_input = OpenaiImageEditingInput(
            image=input_model.image,
            prompt=input_model.prompt,
            model="gpt-image-1",
            mask=input_model.mask,
            size=size_mapping.get(input_model.aspect_ratio, "auto"),
            background=input_model.background,
            quality=input_model.quality,
            user=input_model.user,
        )
        
        return openai_input.model_dump(exclude_none=True, by_alias=True)
    
    def convert_output(self, data: dict) -> str | list[str]:
        """Convert OpenAI Official API response to Sunra format."""
        # OpenAI returns base64 encoded images for gpt-image-1
        if "data" in data and isinstance(data["data"], list):
            return [item["b64_json"] for item in data["data"]] 

    
    def get_request_url(self) -> str:
        """Get the OpenAI Official API endpoint URL for image editing."""
        return "https://api.openai.com/v1/images/edits"
    