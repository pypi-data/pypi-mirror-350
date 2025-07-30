import pytest

from tests.model_serving.model_server.utils import verify_inference_response
from utilities.constants import (
    KServeDeploymentType,
    ModelAndFormat,
    ModelFormat,
    ModelStoragePath,
    ModelVersion,
    Protocols,
    ModelInferenceRuntime,
)
from utilities.inference_utils import Inference
from utilities.manifests.openvino import OPENVINO_KSERVE_INFERENCE_CONFIG

pytestmark = [pytest.mark.serverless, pytest.mark.usefixtures("valid_aws_config")]


@pytest.mark.serverless
@pytest.mark.parametrize(
    "unprivileged_model_namespace, ovms_kserve_serving_runtime, ovms_kserve_inference_service",
    [
        pytest.param(
            {"name": "kserve-serverless-openvino"},
            {
                "runtime-name": ModelInferenceRuntime.OPENVINO_KSERVE_RUNTIME,
                "model-format": {ModelAndFormat.OPENVINO_IR: ModelVersion.OPSET1},
            },
            {
                "name": ModelFormat.OPENVINO,
                "model-version": ModelVersion.OPSET1,
                "model-dir": ModelStoragePath.KSERVE_OPENVINO_EXAMPLE_MODEL,
                "deployment-mode": KServeDeploymentType.SERVERLESS,
            },
        )
    ],
    indirect=True,
)
class TestOpenVINOServerless:
    @pytest.mark.smoke
    @pytest.mark.polarion("ODS-2626")
    def test_serverless_openvino_rest_inference(self, ovms_kserve_inference_service):
        """Verify that kserve Serverless OpenVINO model can be queried using REST"""
        verify_inference_response(
            inference_service=ovms_kserve_inference_service,
            inference_config=OPENVINO_KSERVE_INFERENCE_CONFIG,
            inference_type=Inference.INFER,
            protocol=Protocols.HTTPS,
            use_default_query=True,
        )
