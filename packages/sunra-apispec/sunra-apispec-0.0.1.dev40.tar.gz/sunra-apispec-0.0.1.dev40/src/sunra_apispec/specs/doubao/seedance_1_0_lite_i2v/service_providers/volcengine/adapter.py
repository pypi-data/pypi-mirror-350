from sunra_apispec.base.adapter_interface import IVolcengineAdapter
from ...sunra_schema import ImageToVideoInput
from .schema import VolcengineImageToVideoInput, TextContent, ImageContent, ImageUrl


class VolcengineImageToVideoAdapter(IVolcengineAdapter):
    """Adapter for image-to-video generation using Volcengine Seedance 1.0 Lite I2V model."""
    
    def convert_input(self, data: dict) -> dict:
        """Convert from Sunra's ImageToVideoInput to Volcengine's input format."""
        # Validate the input data if required
        input_model = ImageToVideoInput.model_validate(data)
        
        # Build text content with command parameters
        text_content = self._build_text_content(input_model)
        
        # Build image content
        image_content = ImageContent(
            type="image_url",
            image_url=ImageUrl(url=input_model.start_image)
        )
        
        # Create Volcengine input instance
        volcengine_input = VolcengineImageToVideoInput(
            model="doubao-seedance-1-0-lite-i2v-250428",
            content=[text_content, image_content]
        )
        
        # Convert to dict, excluding None values
        return volcengine_input.model_dump(exclude_none=True, by_alias=True)
    
    def _build_text_content(self, input_model: ImageToVideoInput) -> TextContent:
        """Build text content with command parameters."""
        text_parts = [input_model.prompt]
        
        # Add resolution parameter
        if input_model.resolution == "adaptive":
            text_parts.append(f"--rt {input_model.resolution}")
        else:
            # Add aspect ratio parameter
            if input_model.aspect_ratio:
                text_parts.append(f"--rt {input_model.aspect_ratio}")

        # Add seed parameter
        if input_model.seed:
            text_parts.append(f"--seed {input_model.seed}")
        
        # Add duration parameter
        if input_model.duration:
            text_parts.append(f"--dur {input_model.duration}")
        
        text_content = TextContent(
            type="text",
            text=" ".join(text_parts)
        )
        
        return text_content
    
    def convert_output(self, data: dict) -> str:
        """Convert from Volcengine's output format to Sunra's output format."""
        if "content" in data and "video_url" in data["content"]:
            return data["content"]["video_url"]
        raise ValueError(f"Invalid output format: {data}") 

    def get_request_url(self) -> str:
        return "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"

    def get_status_url(self, task_id: str) -> str:
        return f"https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}"
