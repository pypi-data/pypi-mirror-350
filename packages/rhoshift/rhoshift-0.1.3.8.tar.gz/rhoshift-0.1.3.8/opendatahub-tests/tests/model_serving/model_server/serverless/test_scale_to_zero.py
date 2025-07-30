import pytest

from tests.model_serving.model_server.serverless.utils import verify_no_inference_pods
from tests.model_serving.model_server.utils import verify_inference_response
from utilities.constants import (
    KServeDeploymentType,
    ModelFormat,
    ModelVersion,
    Protocols,
    RunTimeConfigs,
)
from utilities.inference_utils import Inference
from utilities.manifests.onnx import ONNX_INFERENCE_CONFIG
from utilities.infra import wait_for_inference_deployment_replicas

pytestmark = [
    pytest.mark.serverless,
    pytest.mark.sanity,
    pytest.mark.usefixtures("valid_aws_config"),
]

NO_PODS_AFTER_SCALE_TEST_NAME: str = "test_no_serverless_pods_after_scale_to_zero"
INFERENCE_AFTER_SCALE_TEST_NAME: str = "test_serverless_inference_after_scale_to_zero"


@pytest.mark.serverless
@pytest.mark.parametrize(
    "unprivileged_model_namespace, ovms_kserve_serving_runtime, ovms_kserve_inference_service",
    [
        pytest.param(
            {"name": "serverless-scale-zero"},
            RunTimeConfigs.ONNX_OPSET13_RUNTIME_CONFIG,
            {
                "name": ModelFormat.ONNX,
                "model-version": ModelVersion.OPSET13,
                "model-dir": "test-dir",
                "deployment-mode": KServeDeploymentType.SERVERLESS,
            },
        )
    ],
    indirect=True,
)
class TestServerlessScaleToZero:
    @pytest.mark.order(1)
    def test_serverless_before_scale_to_zero(self, ovms_kserve_inference_service):
        """Verify model can be queried before scaling to zero"""
        verify_inference_response(
            inference_service=ovms_kserve_inference_service,
            inference_config=ONNX_INFERENCE_CONFIG,
            inference_type=Inference.INFER,
            protocol=Protocols.HTTPS,
            use_default_query=True,
        )

    @pytest.mark.parametrize(
        "inference_service_patched_replicas",
        [pytest.param({"min-replicas": 0})],
        indirect=True,
    )
    @pytest.mark.order(2)
    @pytest.mark.dependency(name=NO_PODS_AFTER_SCALE_TEST_NAME)
    def test_no_serverless_pods_after_scale_to_zero(self, unprivileged_client, inference_service_patched_replicas):
        """Verify pods are scaled to zero"""
        verify_no_inference_pods(client=unprivileged_client, isvc=inference_service_patched_replicas)

    @pytest.mark.dependency(
        name=INFERENCE_AFTER_SCALE_TEST_NAME,
        depends=[NO_PODS_AFTER_SCALE_TEST_NAME],
    )
    @pytest.mark.order(3)
    def test_serverless_inference_after_scale_to_zero(self, inference_service_patched_replicas):
        """Verify model can be queried after scaling to zero"""
        verify_inference_response(
            inference_service=inference_service_patched_replicas,
            inference_config=ONNX_INFERENCE_CONFIG,
            inference_type=Inference.INFER,
            protocol=Protocols.HTTPS,
            use_default_query=True,
        )

    @pytest.mark.dependency(
        depends=[INFERENCE_AFTER_SCALE_TEST_NAME],
    )
    @pytest.mark.order(4)
    def test_no_serverless_pods_when_no_traffic(self, unprivileged_client, inference_service_patched_replicas):
        """Verify pods are scaled to zero when no traffic is sent"""
        verify_no_inference_pods(client=unprivileged_client, isvc=inference_service_patched_replicas)

    @pytest.mark.parametrize(
        "inference_service_patched_replicas",
        [pytest.param({"min-replicas": 1})],
        indirect=True,
    )
    @pytest.mark.order(5)
    def test_serverless_pods_after_scale_to_one_replica(self, unprivileged_client, inference_service_patched_replicas):
        """Verify pod is running after scaling to 1 replica"""
        wait_for_inference_deployment_replicas(
            client=unprivileged_client,
            isvc=inference_service_patched_replicas,
            expected_num_deployments=1,
            labels="serving.knative.dev/configurationGeneration=3",
        )
