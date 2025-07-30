import pytest
from simple_logger.logger import get_logger
from typing import Any, Generator
from ocp_resources.inference_service import InferenceService
from ocp_resources.pod import Pod
from utilities.constants import KServeDeploymentType
from tests.model_serving.model_runtime.vllm.utils import (
    validate_raw_openai_inference_request,
    validate_raw_tgis_inference_request,
    validate_serverless_openai_inference_request,
)
from tests.model_serving.model_runtime.vllm.constant import (
    COMPLETION_QUERY,
    CHAT_QUERY,
    BASE_RAW_DEPLOYMENT_CONFIG,
    BASE_SEVERRLESS_DEPLOYMENT_CONFIG,
)

LOGGER = get_logger(name=__name__)


SERVING_ARGUMENT: list[str] = [
    "--model=/mnt/models",
    "--uvicorn-log-level=debug",
    "--dtype=float16",
    "--chat-template=/app/data/template/template_chatglm.jinja",
]

MODEL_PATH: str = "merlinite-7b-lab"

BASE_RAW_DEPLOYMENT_CONFIG["runtime_argument"] = SERVING_ARGUMENT
BASE_SEVERRLESS_DEPLOYMENT_CONFIG["runtime_argument"] = SERVING_ARGUMENT

pytestmark = pytest.mark.usefixtures("skip_if_no_supported_accelerator_type", "valid_aws_config")


@pytest.mark.parametrize(
    "model_namespace, s3_models_storage_uri, serving_runtime, vllm_inference_service",
    [
        pytest.param(
            {"name": "merlinite-lab-raw"},
            {"model-dir": MODEL_PATH},
            {"deployment_type": KServeDeploymentType.RAW_DEPLOYMENT},
            {
                **BASE_RAW_DEPLOYMENT_CONFIG,
                "gpu_count": 1,
                "name": "merlinite-lab-raw",
            },
            id="merlinite-lab-7b-raw-single-gpu",
        ),
        pytest.param(
            {"name": "merlinite-lab-7b-serverless"},
            {"model-dir": MODEL_PATH},
            {"deployment_type": KServeDeploymentType.SERVERLESS},
            {
                **BASE_SEVERRLESS_DEPLOYMENT_CONFIG,
                "gpu_count": 1,
                "name": "merlinite-lab-ser",
            },
            id="merlinite-lab-7b-serverless-single-gpu",
        ),
    ],
    indirect=True,
)
class TestMerliniteLabModel:
    def test_merlinite_lab_7b_raw_simple_openai_model_inference(
        self,
        vllm_inference_service: Generator[InferenceService, Any, Any],
        skip_if_serverless_deployemnt: Any,
        vllm_pod_resource: Pod,
        response_snapshot: Any,
    ):
        validate_raw_openai_inference_request(
            pod_name=vllm_pod_resource.name,
            isvc=vllm_inference_service,
            response_snapshot=response_snapshot,
            chat_query=CHAT_QUERY,
            completion_query=COMPLETION_QUERY,
        )

    def test_merlinite_lab_7b_raw_simple_tgis_model_inference(
        self,
        vllm_inference_service: Generator[InferenceService, Any, Any],
        skip_if_serverless_deployemnt: Any,
        vllm_pod_resource: Pod,
        response_snapshot: Any,
    ):
        validate_raw_tgis_inference_request(
            pod_name=vllm_pod_resource.name,
            isvc=vllm_inference_service,
            response_snapshot=response_snapshot,
            completion_query=COMPLETION_QUERY,
        )

    def test_merlinite_lab_7b_model_inference_serverless(
        self,
        vllm_inference_service: Generator[InferenceService, Any, Any],
        skip_if_raw_deployemnt: Any,
        response_snapshot: Any,
    ):
        validate_serverless_openai_inference_request(
            url=vllm_inference_service.instance.status.url,
            model_name=vllm_inference_service.instance.metadata.name,
            response_snapshot=response_snapshot,
            chat_query=CHAT_QUERY,
            completion_query=COMPLETION_QUERY,
        )


@pytest.mark.parametrize(
    "model_namespace, s3_models_storage_uri, serving_runtime, vllm_inference_service",
    [
        pytest.param(
            {"name": "merlinite-lab-7b-raw-multi"},
            {"model-dir": MODEL_PATH},
            {"deployment_type": KServeDeploymentType.RAW_DEPLOYMENT},
            {
                **BASE_RAW_DEPLOYMENT_CONFIG,
                "gpu_count": 2,
                "name": "merlinite-lab-rm",
            },
            id="merlinite-lab-7b-raw-multi-gpu",
        ),
        pytest.param(
            {"name": "merlinite-lab-7b-serverless-multi"},
            {"model-dir": MODEL_PATH},
            {"deployment_type": KServeDeploymentType.SERVERLESS},
            {
                **BASE_SEVERRLESS_DEPLOYMENT_CONFIG,
                "gpu_count": 2,
                "name": "merlinite-lab-sm",
            },
            id="merlinite-lab-7b-serverless-multi-gpu",
        ),
    ],
    indirect=True,
)
class TestMultiMerliniteLabModel:
    def test_merlinite_lab_7b_raw_multi_openai_model_inference(
        self,
        vllm_inference_service: Generator[InferenceService, Any, Any],
        skip_if_serverless_deployemnt: Any,
        vllm_pod_resource: Pod,
        response_snapshot: Any,
    ):
        validate_raw_openai_inference_request(
            pod_name=vllm_pod_resource.name,
            isvc=vllm_inference_service,
            response_snapshot=response_snapshot,
            chat_query=CHAT_QUERY,
            completion_query=COMPLETION_QUERY,
        )

    def test_merlinite_lab_7b_raw_multi_tgis_model_inference(
        self,
        vllm_inference_service: Generator[InferenceService, Any, Any],
        skip_if_serverless_deployemnt: Any,
        vllm_pod_resource: Pod,
        response_snapshot: Any,
    ):
        validate_raw_tgis_inference_request(
            pod_name=vllm_pod_resource.name,
            isvc=vllm_inference_service,
            response_snapshot=response_snapshot,
            completion_query=COMPLETION_QUERY,
        )

    def test_merlinite_lab_7b_multi_model_inference_serverless(
        self,
        vllm_inference_service: Generator[InferenceService, Any, Any],
        skip_if_raw_deployemnt: Any,
        response_snapshot: Any,
    ):
        validate_serverless_openai_inference_request(
            url=vllm_inference_service.instance.status.url,
            model_name=vllm_inference_service.instance.metadata.name,
            response_snapshot=response_snapshot,
            chat_query=CHAT_QUERY,
            completion_query=COMPLETION_QUERY,
        )
