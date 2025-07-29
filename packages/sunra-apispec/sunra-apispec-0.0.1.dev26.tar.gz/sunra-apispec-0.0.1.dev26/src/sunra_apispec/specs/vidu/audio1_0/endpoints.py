import os
from sunra_apispec.base.base_api_service import BaseAPIService, SubmitResponse
from sunra_apispec.base.output_schema import AudioOutput
from sunra_apispec.base.adapter_interface import ServiceProviderEnum
from sunra_apispec.model_mapping import model_mapping
from .sunra_schema import Text2AudioInput, Timing2VideoInput
from .service_providers.vidu_official.adapter import (
    ViduTextToAudioAdapter,
    ViduTimingToAudioAdapter,
)


model_name = os.path.basename(os.path.dirname(__file__))
model_provider = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
model_path = model_mapping[f"{model_provider}/{model_name}"]


service = BaseAPIService(
    title="Vidu API",
    description="API for Vidu audio generation model",
    version="1.0.0",
    output_schema=AudioOutput,
)


@service.app.post(
    f"/{model_path}/text-to-audio",
    response_model=SubmitResponse,
    description="Generate audio from text prompts",
)
def text_to_audio(body: Text2AudioInput) -> SubmitResponse:
    pass


@service.app.post(
    f"/{model_path}/timing-to-audio",
    response_model=SubmitResponse,
    description="Generate a controllable sound effect clip based on input text prompts. (BGM not supported.)",
)
def timing_to_audio(body: Timing2VideoInput) -> SubmitResponse:
    pass


registry_items = {
    f"{model_path}/text-to-audio": [
        {
            "service_provider": ServiceProviderEnum.VIDU.value,
            "adapter": ViduTextToAudioAdapter,
        }
    ],
    f"{model_path}/timing-to-audio": [
        {
            "service_provider": ServiceProviderEnum.VIDU.value,
            "adapter": ViduTimingToAudioAdapter,
        }
    ]
}
