import os
from sunra_apispec.base.base_api_service import BaseAPIService, SubmitResponse
from sunra_apispec.base.output_schema import VideoOutput
from sunra_apispec.model_mapping import model_mapping
from .sunra_schema import UpscaleProInput

model_name = os.path.basename(os.path.dirname(__file__))
model_provider = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
model_path = model_mapping[f"{model_provider}/{model_name}"]

service = BaseAPIService(
    title="Vidu Upscale Pro API",
    description="API for Vidu Upscale Pro video generation model",
    version="1.0.0",
    output_schema=VideoOutput,
)

@service.app.post(
    f"/{model_path}/upscale",
    response_model=SubmitResponse,
    description="Upscale video",
)
def upscale_pro(body: UpscaleProInput) -> SubmitResponse:
    pass