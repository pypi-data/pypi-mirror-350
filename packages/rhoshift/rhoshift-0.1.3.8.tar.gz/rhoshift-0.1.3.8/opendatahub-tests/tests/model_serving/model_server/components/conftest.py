from typing import Any, Generator

import pytest
from ocp_resources.data_science_cluster import DataScienceCluster
from _pytest.fixtures import FixtureRequest
from kubernetes.dynamic import DynamicClient
from ocp_resources.inference_service import InferenceService
from ocp_resources.namespace import Namespace
from ocp_resources.resource import ResourceEditor
from ocp_resources.service_account import ServiceAccount
from ocp_resources.serving_runtime import ServingRuntime

from utilities.data_science_cluster_utils import update_components_in_dsc
from utilities.constants import DscComponents
from utilities.inference_utils import create_isvc


@pytest.fixture(scope="class")
def managed_modelmesh_kserve_in_dsc(
    dsc_resource: DataScienceCluster,
) -> Generator[DataScienceCluster, Any, Any]:
    with update_components_in_dsc(
        dsc=dsc_resource,
        components={
            DscComponents.MODELMESHSERVING: DscComponents.ManagementState.MANAGED,
            DscComponents.KSERVE: DscComponents.ManagementState.MANAGED,
        },
        wait_for_components_state=False,
    ) as dsc:
        yield dsc


@pytest.fixture(scope="class")
def invalid_s3_models_inference_service(
    request: FixtureRequest,
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
    serving_runtime_from_template: ServingRuntime,
    models_s3_bucket_name: str,
    model_service_account: ServiceAccount,
) -> Generator[InferenceService, Any, Any]:
    with create_isvc(
        client=unprivileged_client,
        name=request.param["name"],
        namespace=unprivileged_model_namespace.name,
        runtime=serving_runtime_from_template.name,
        storage_uri=f"s3://{models_s3_bucket_name}/non-existing-path/",
        model_format=serving_runtime_from_template.instance.spec.supportedModelFormats[0].name,
        model_service_account=model_service_account.name,
        deployment_mode=request.param["deployment-mode"],
        wait=False,
        wait_for_predictor_pods=False,
    ) as isvc:
        yield isvc


@pytest.fixture
def updated_s3_models_inference_service(
    invalid_s3_models_inference_service: InferenceService, s3_models_storage_uri: str
) -> Generator[InferenceService, Any, Any]:
    with ResourceEditor(
        patches={
            invalid_s3_models_inference_service: {
                "spec": {
                    "predictor": {"model": {"storageUri": s3_models_storage_uri}},
                }
            }
        }
    ):
        yield invalid_s3_models_inference_service
