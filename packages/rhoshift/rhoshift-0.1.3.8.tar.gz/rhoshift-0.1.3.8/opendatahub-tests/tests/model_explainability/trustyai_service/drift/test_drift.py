from functools import partial

import pytest

from tests.model_explainability.trustyai_service.constants import DRIFT_BASE_DATA_PATH
from tests.model_explainability.trustyai_service.trustyai_service_utils import (
    send_inferences_and_verify_trustyai_service_registered,
    verify_upload_data_to_trustyai_service,
    verify_trustyai_service_metric_request,
    TrustyAIServiceMetrics,
    verify_trustyai_service_metric_scheduling_request,
    verify_trustyai_service_metric_delete_request,
)
from utilities.constants import MinIo
from utilities.manifests.openvino import OPENVINO_KSERVE_INFERENCE_CONFIG
from utilities.monitoring import validate_metrics_field, get_metric_label


@pytest.mark.parametrize(
    "model_namespace, minio_pod, minio_data_connection",
    [
        pytest.param(
            {"name": "test-drift"},
            MinIo.PodConfig.MODEL_MESH_MINIO_CONFIG,
            {"bucket": MinIo.Buckets.MODELMESH_EXAMPLE_MODELS},
        )
    ],
    indirect=True,
)
@pytest.mark.usefixtures("minio_pod")
@pytest.mark.smoke
class TestDriftMetrics:
    """
    Verifies all the basic operations with a drift metric (meanshift) available in TrustyAI, using PVC storage.

    1. Send data to the model (gaussian_credit_model) and verify that TrustyAI registers the observations.
    2. Send metric request (meanshift) and verify the response.
    3. Send metric scheduling request and verify the response.
    4. Send metric deletion request and verify that the scheduled metric has been deleted.
    """

    def test_drift_send_inference_and_verify_trustyai_service(
        self,
        admin_client,
        current_client_token,
        model_namespace,
        trustyai_service_with_pvc_storage,
        gaussian_credit_model,
    ) -> None:
        send_inferences_and_verify_trustyai_service_registered(
            client=admin_client,
            token=current_client_token,
            data_path=f"{DRIFT_BASE_DATA_PATH}/data_batches",
            trustyai_service=trustyai_service_with_pvc_storage,
            inference_service=gaussian_credit_model,
            inference_config=OPENVINO_KSERVE_INFERENCE_CONFIG,
        )

    def test_upload_data_to_trustyai_service(
        self,
        admin_client,
        minio_data_connection,
        current_client_token,
        trustyai_service_with_pvc_storage,
    ) -> None:
        verify_upload_data_to_trustyai_service(
            client=admin_client,
            trustyai_service=trustyai_service_with_pvc_storage,
            token=current_client_token,
            data_path=f"{DRIFT_BASE_DATA_PATH}/training_data.json",
        )

    def test_drift_metric_meanshift(
        self,
        admin_client,
        current_client_token,
        trustyai_service_with_pvc_storage,
        gaussian_credit_model,
    ):
        verify_trustyai_service_metric_request(
            client=admin_client,
            trustyai_service=trustyai_service_with_pvc_storage,
            token=current_client_token,
            metric_name=TrustyAIServiceMetrics.Drift.MEANSHIFT,
            json_data={
                "modelId": gaussian_credit_model.name,
                "referenceTag": "TRAINING",
            },
        )

    def test_drift_metric_schedule_meanshift(
        self,
        admin_client,
        current_client_token,
        trustyai_service_with_pvc_storage,
        gaussian_credit_model,
    ):
        verify_trustyai_service_metric_scheduling_request(
            client=admin_client,
            trustyai_service=trustyai_service_with_pvc_storage,
            token=current_client_token,
            metric_name=TrustyAIServiceMetrics.Drift.MEANSHIFT,
            json_data={
                "modelId": gaussian_credit_model.name,
                "referenceTag": "TRAINING",
            },
        )

    def test_drift_metric_prometheus(
        self,
        admin_client,
        model_namespace,
        trustyai_service_with_pvc_storage,
        gaussian_credit_model,
        prometheus,
    ):
        validate_metrics_field(
            prometheus=prometheus,
            metrics_query=f'trustyai_{TrustyAIServiceMetrics.Drift.MEANSHIFT}{{namespace="{model_namespace.name}"}}',
            expected_value=TrustyAIServiceMetrics.Drift.MEANSHIFT.upper(),
            field_getter=partial(get_metric_label, label_name="metricName"),
        )

    def test_drift_metric_delete(
        self,
        admin_client,
        minio_data_connection,
        current_client_token,
        trustyai_service_with_pvc_storage,
    ):
        verify_trustyai_service_metric_delete_request(
            client=admin_client,
            trustyai_service=trustyai_service_with_pvc_storage,
            token=current_client_token,
            metric_name=TrustyAIServiceMetrics.Drift.MEANSHIFT,
        )
