import pytest
from simple_logger.logger import get_logger
from utilities.constants import KServeDeploymentType, Ports
from tests.model_serving.model_runtime.vllm.utils import fetch_openai_response, run_raw_inference

LOGGER = get_logger(name=__name__)

serving_arument = ["--dtype=bfloat16", "--model=/mnt/models", "--max-model-len=2048", "--uvicorn-log-level=debug"]


pytestmark = pytest.mark.usefixtures("skip_if_no_supported_accelerator_type", "valid_aws_config")


@pytest.mark.parametrize(
    "model_namespace, s3_models_storage_uri, serving_runtime, vllm_inference_service",
    [
        pytest.param(
            {"name": "granite-serverless-serv"},
            {"model-dir": "granite-2b-instruct-preview-4k-r240917a"},
            {"deployment_type": KServeDeploymentType.SERVERLESS},
            {
                "deployment_mode": KServeDeploymentType.SERVERLESS,
                "runtime_argument": serving_arument,
                "gpu_count": 1,
                "name": "granite-ser",
                "min-replicas": 1,
            },
        ),
        pytest.param(
            {"name": "granite-serverless-raw"},
            {"model-dir": "granite-2b-instruct-preview-4k-r240917a"},
            {"deployment_type": KServeDeploymentType.RAW_DEPLOYMENT},
            {
                "deployment_mode": KServeDeploymentType.RAW_DEPLOYMENT,
                "runtime_argument": serving_arument,
                "gpu_count": 1,
                "name": "granite-raw",
                "min-replicas": 1,
            },
        ),
    ],
    indirect=True,
)
class TestGranite2BModel:
    def test_deploy_model_inference(self, vllm_inference_service, vllm_pod_resource, response_snapshot):
        if (
            vllm_inference_service.instance.metadata.annotations["serving.kserve.io/deploymentMode"]
            == KServeDeploymentType.SERVERLESS
        ):
            model_info, chat_responses, completion_responses = fetch_openai_response(
                url=vllm_inference_service.instance.status.url,
                model_name=vllm_inference_service.instance.metadata.name,
            )
            assert model_info == response_snapshot
            assert chat_responses == response_snapshot
            assert completion_responses == response_snapshot
        if (
            vllm_inference_service.instance.metadata.annotations["serving.kserve.io/deploymentMode"]
            == KServeDeploymentType.RAW_DEPLOYMENT
        ):
            pod = vllm_pod_resource.name
            model_details, grpc_chat_response, grpc_chat_stream_responses = run_raw_inference(
                pod_name=pod, isvc=vllm_inference_service, port=Ports.GRPC_PORT, endpoint="tgis"
            )
            assert model_details == response_snapshot
            assert grpc_chat_response == response_snapshot
            assert grpc_chat_stream_responses == response_snapshot
            model_info, chat_responses, completion_responses = run_raw_inference(
                pod_name=pod, isvc=vllm_inference_service, port=Ports.REST_PORT, endpoint="openai"
            )
            assert model_info == response_snapshot
            assert chat_responses == response_snapshot
            assert completion_responses == response_snapshot


@pytest.mark.parametrize(
    "model_namespace, s3_models_storage_uri, serving_runtime, vllm_inference_service",
    [
        pytest.param(
            {"name": "granite-multiser"},
            {"model-dir": "granite-2b-instruct-preview-4k-r240917a"},
            {"deployment_type": KServeDeploymentType.SERVERLESS},
            {
                "deployment_mode": KServeDeploymentType.SERVERLESS,
                "runtime_argument": serving_arument,
                "gpu_count": 2,
                "name": "granite-ser",
                "min-replicas": 1,
            },
        ),
        pytest.param(
            {"name": "granite-multiraw"},
            {"model-dir": "granite-2b-instruct-preview-4k-r240917a"},
            {"deployment_type": KServeDeploymentType.RAW_DEPLOYMENT},
            {
                "deployment_mode": KServeDeploymentType.RAW_DEPLOYMENT,
                "runtime_argument": serving_arument,
                "gpu_count": 2,
                "name": "granite-raw",
                "min-replicas": 1,
            },
        ),
    ],
    indirect=True,
)
class TestGranite2BModelMultiGPU:
    def test_deploy_model_inference(self, vllm_inference_service, vllm_pod_resource, response_snapshot):
        if (
            vllm_inference_service.instance.metadata.annotations["serving.kserve.io/deploymentMode"]
            == KServeDeploymentType.SERVERLESS
        ):
            model_info, chat_responses, completion_responses = fetch_openai_response(
                url=vllm_inference_service.instance.status.url,
                model_name=vllm_inference_service.instance.metadata.name,
            )
            assert model_info == response_snapshot
            assert chat_responses == response_snapshot
            assert completion_responses == response_snapshot
        if (
            vllm_inference_service.instance.metadata.annotations["serving.kserve.io/deploymentMode"]
            == KServeDeploymentType.RAW_DEPLOYMENT
        ):
            pod = vllm_pod_resource.name
            model_detail, grpc_chat_response, grpc_chat_stream_responses = run_raw_inference(
                pod_name=pod, isvc=vllm_inference_service, port=Ports.GRPC_PORT, endpoint="tgis"
            )
            assert model_detail == response_snapshot
            assert grpc_chat_response == response_snapshot
            assert grpc_chat_stream_responses == response_snapshot
            model_info, chat_responses, completion_responses = run_raw_inference(
                pod_name=pod, isvc=vllm_inference_service, port=Ports.REST_PORT, endpoint="openai"
            )
            assert model_info == response_snapshot
            assert chat_responses == response_snapshot
            assert completion_responses == response_snapshot
