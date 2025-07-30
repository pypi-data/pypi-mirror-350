from sunra_apispec.base.adapter_interface import IMinimaxAdapter
from ...sunra_schema import ImageToVideoInput
from .schema import MinimaxVideoGenInput, ModelEnum


class MinimaxImageToVideoAdapter(IMinimaxAdapter):
    """Adapter for image-to-video generation using MiniMax I2V-01 model."""
    
    def convert_input(self, data: dict) -> dict:
        """Convert from Sunra's ImageToVideoInput to MiniMax's input format."""
        # Validate the input data
        input_model = ImageToVideoInput.model_validate(data)
        
        # Create MiniMax input instance with mapped values
        minimax_input = MinimaxVideoGenInput(
            model=ModelEnum.I2V_01,
            prompt=input_model.prompt,
            prompt_optimizer=input_model.prompt_enhancer,
            first_frame_image=input_model.start_image
        )
        
        # Convert to dict, excluding None values
        return minimax_input.model_dump(exclude_none=True, by_alias=True)
    
    def get_request_url(self) -> str:
        """Return the MiniMax API endpoint for video generation."""
        return "https://api.minimaxi.chat/v1/video_generation"
    
    def get_status_url(self, task_id: str) -> str:
        """Return the MiniMax API endpoint for checking task status."""
        return f"https://api.minimaxi.chat/v1/query/video_generation?task_id={task_id}"
    
    def get_file_url(self, file_id: str) -> str:
        """Return the MiniMax API endpoint for retrieving files."""
        return f"https://api.minimaxi.chat/v1/files/retrieve?file_id={file_id}" 

    def convert_output(self, data: dict) -> str | list[str]:
        """Convert from MiniMax's output format to Sunra's output format."""
        return data['file']['download_url']
