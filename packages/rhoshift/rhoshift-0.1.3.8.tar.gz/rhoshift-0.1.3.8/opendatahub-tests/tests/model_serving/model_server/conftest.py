from typing import Any, Generator

import pytest
import yaml
from _pytest.fixtures import FixtureRequest
from kubernetes.dynamic import DynamicClient
from ocp_resources.cluster_service_version import ClusterServiceVersion
from ocp_resources.config_map import ConfigMap
from ocp_resources.inference_service import InferenceService
from ocp_resources.namespace import Namespace
from ocp_resources.persistent_volume_claim import PersistentVolumeClaim
from ocp_resources.secret import Secret
from ocp_resources.service_account import ServiceAccount
from ocp_resources.serving_runtime import ServingRuntime
from ocp_resources.storage_class import StorageClass
from pytest_testconfig import config as py_config
from simple_logger.logger import get_logger

from utilities.constants import (
    KServeDeploymentType,
    ModelFormat,
    ModelInferenceRuntime,
    ModelStoragePath,
    Protocols,
    RuntimeTemplates,
    StorageClassName,
)
from utilities.constants import (
    ModelAndFormat,
    ModelVersion,
)
from utilities.inference_utils import create_isvc
from utilities.infra import (
    s3_endpoint_secret,
    update_configmap_data,
)
from utilities.serving_runtime import ServingRuntimeFromTemplate


LOGGER = get_logger(name=__name__)


@pytest.fixture(scope="class")
def models_endpoint_s3_secret(
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    models_s3_bucket_name: str,
    models_s3_bucket_region: str,
    models_s3_bucket_endpoint: str,
) -> Generator[Secret, Any, Any]:
    with s3_endpoint_secret(
        client=unprivileged_client,
        name="models-bucket-secret",
        namespace=unprivileged_model_namespace.name,
        aws_access_key=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_s3_region=models_s3_bucket_region,
        aws_s3_bucket=models_s3_bucket_name,
        aws_s3_endpoint=models_s3_bucket_endpoint,
    ) as secret:
        yield secret


# HTTP model serving
@pytest.fixture(scope="class")
def model_service_account(
    unprivileged_client: DynamicClient, models_endpoint_s3_secret: Secret
) -> Generator[ServiceAccount, Any, Any]:
    with ServiceAccount(
        client=unprivileged_client,
        namespace=models_endpoint_s3_secret.namespace,
        name="models-bucket-sa",
        secrets=[{"name": models_endpoint_s3_secret.name}],
    ) as sa:
        yield sa


@pytest.fixture(scope="class")
def serving_runtime_from_template(
    request: FixtureRequest,
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
) -> Generator[ServingRuntime, Any, Any]:
    runtime_kwargs = {
        "client": unprivileged_client,
        "name": request.param["name"],
        "namespace": unprivileged_model_namespace.name,
        "template_name": request.param["template-name"],
        "multi_model": request.param["multi-model"],
        "models_priorities": request.param.get("models-priorities"),
        "supported_model_formats": request.param.get("supported-model-formats"),
    }

    if (enable_http := request.param.get("enable-http")) is not None:
        runtime_kwargs["enable_http"] = enable_http

    if (enable_grpc := request.param.get("enable-grpc")) is not None:
        runtime_kwargs["enable_grpc"] = enable_grpc

    with ServingRuntimeFromTemplate(**runtime_kwargs) as model_runtime:
        yield model_runtime


@pytest.fixture(scope="class")
def s3_models_inference_service(
    request: FixtureRequest,
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
    serving_runtime_from_template: ServingRuntime,
    models_endpoint_s3_secret: Secret,
) -> Generator[InferenceService, Any, Any]:
    isvc_kwargs = {
        "client": unprivileged_client,
        "name": request.param["name"],
        "namespace": unprivileged_model_namespace.name,
        "runtime": serving_runtime_from_template.name,
        "model_format": serving_runtime_from_template.instance.spec.supportedModelFormats[0].name,
        "deployment_mode": request.param["deployment-mode"],
        "storage_key": models_endpoint_s3_secret.name,
        "storage_path": request.param["model-dir"],
    }

    if (external_route := request.param.get("external-route")) is not None:
        isvc_kwargs["external_route"] = external_route

    if (enable_auth := request.param.get("enable-auth")) is not None:
        isvc_kwargs["enable_auth"] = enable_auth

    if (scale_metric := request.param.get("scale-metric")) is not None:
        isvc_kwargs["scale_metric"] = scale_metric

    if (scale_target := request.param.get("scale-target")) is not None:
        isvc_kwargs["scale_target"] = scale_target

    with create_isvc(**isvc_kwargs) as isvc:
        yield isvc


@pytest.fixture(scope="class")
def model_pvc(
    request: FixtureRequest,
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
) -> Generator[PersistentVolumeClaim, Any, Any]:
    access_mode = "ReadWriteOnce"
    pvc_kwargs = {
        "name": "model-pvc",
        "namespace": unprivileged_model_namespace.name,
        "client": unprivileged_client,
        "size": request.param["pvc-size"],
    }
    if hasattr(request, "param"):
        access_mode = request.param.get("access-modes")

        if storage_class_name := request.param.get("storage-class-name"):
            pvc_kwargs["storage_class"] = storage_class_name

    pvc_kwargs["accessmodes"] = access_mode

    with PersistentVolumeClaim(**pvc_kwargs) as pvc:
        pvc.wait_for_status(status=pvc.Status.BOUND, timeout=120)
        yield pvc


@pytest.fixture(scope="session")
def skip_if_no_nfs_storage_class(admin_client: DynamicClient) -> None:
    if not StorageClass(client=admin_client, name=StorageClassName.NFS).exists:
        pytest.skip(f"StorageClass {StorageClassName.NFS} is missing from the cluster")


@pytest.fixture(scope="class")
def http_s3_openvino_model_mesh_inference_service(
    request: FixtureRequest,
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
    http_s3_ovms_model_mesh_serving_runtime: ServingRuntime,
    ci_endpoint_s3_secret: Secret,
    ci_service_account: ServiceAccount,
) -> Generator[InferenceService, Any, Any]:
    with create_isvc(
        client=unprivileged_client,
        name=f"{Protocols.HTTP}-{ModelFormat.OPENVINO}",
        namespace=unprivileged_model_namespace.name,
        runtime=http_s3_ovms_model_mesh_serving_runtime.name,
        model_service_account=ci_service_account.name,
        storage_key=ci_endpoint_s3_secret.name,
        storage_path=request.param["model-path"],
        model_format=ModelAndFormat.OPENVINO_IR,
        deployment_mode=KServeDeploymentType.MODEL_MESH,
        model_version=ModelVersion.OPSET1,
    ) as isvc:
        yield isvc


@pytest.fixture(scope="class")
def http_s3_ovms_model_mesh_serving_runtime(
    request: FixtureRequest,
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
) -> Generator[ServingRuntime, Any, Any]:
    runtime_kwargs = {
        "client": unprivileged_client,
        "namespace": unprivileged_model_namespace.name,
        "name": f"{Protocols.HTTP}-{ModelInferenceRuntime.OPENVINO_RUNTIME}",
        "template_name": RuntimeTemplates.OVMS_MODEL_MESH,
        "multi_model": True,
        "protocol": Protocols.REST.upper(),
        "resources": {
            ModelFormat.OVMS: {
                "requests": {"cpu": "1", "memory": "4Gi"},
                "limits": {"cpu": "2", "memory": "8Gi"},
            }
        },
    }

    enable_external_route = False
    enable_auth = False

    if hasattr(request, "param"):
        enable_external_route = request.param.get("enable-external-route")
        enable_auth = request.param.get("enable-auth")
        if supported_model_formats := request.param.get("supported-model-formats"):
            runtime_kwargs["supported_model_formats"] = supported_model_formats

        if runtime_image := request.param.get("runtime-image"):
            runtime_kwargs["runtime_image"] = runtime_image

    runtime_kwargs["enable_external_route"] = enable_external_route
    runtime_kwargs["enable_auth"] = enable_auth

    with ServingRuntimeFromTemplate(**runtime_kwargs) as model_runtime:
        yield model_runtime


@pytest.fixture(scope="class")
def ovms_kserve_serving_runtime(
    request: FixtureRequest,
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
) -> Generator[ServingRuntime, Any, Any]:
    runtime_kwargs = {
        "client": unprivileged_client,
        "namespace": unprivileged_model_namespace.name,
        "name": request.param["runtime-name"],
        "template_name": RuntimeTemplates.OVMS_KSERVE,
        "multi_model": False,
        "resources": {
            ModelFormat.OVMS: {
                "requests": {"cpu": "1", "memory": "4Gi"},
                "limits": {"cpu": "2", "memory": "8Gi"},
            }
        },
    }

    if model_format_name := request.param.get("model-format"):
        runtime_kwargs["model_format_name"] = model_format_name

    if supported_model_formats := request.param.get("supported-model-formats"):
        runtime_kwargs["supported_model_formats"] = supported_model_formats

    if runtime_image := request.param.get("runtime-image"):
        runtime_kwargs["runtime_image"] = runtime_image

    with ServingRuntimeFromTemplate(**runtime_kwargs) as model_runtime:
        yield model_runtime


@pytest.fixture(scope="class")
def ci_endpoint_s3_secret(
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    ci_s3_bucket_name: str,
    ci_s3_bucket_region: str,
    ci_s3_bucket_endpoint: str,
) -> Generator[Secret, Any, Any]:
    with s3_endpoint_secret(
        client=unprivileged_client,
        name="ci-bucket-secret",
        namespace=unprivileged_model_namespace.name,
        aws_access_key=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_s3_region=ci_s3_bucket_region,
        aws_s3_bucket=ci_s3_bucket_name,
        aws_s3_endpoint=ci_s3_bucket_endpoint,
    ) as secret:
        yield secret


@pytest.fixture(scope="class")
def ci_service_account(
    unprivileged_client: DynamicClient, ci_endpoint_s3_secret: Secret
) -> Generator[ServiceAccount, Any, Any]:
    with ServiceAccount(
        client=unprivileged_client,
        namespace=ci_endpoint_s3_secret.namespace,
        name="ci-models-bucket-sa",
        secrets=[{"name": ci_endpoint_s3_secret.name}],
    ) as sa:
        yield sa


@pytest.fixture(scope="class")
def ovms_kserve_inference_service(
    request: FixtureRequest,
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
    ovms_kserve_serving_runtime: ServingRuntime,
    ci_endpoint_s3_secret: Secret,
) -> Generator[InferenceService, Any, Any]:
    deployment_mode = request.param["deployment-mode"]
    isvc_kwargs = {
        "client": unprivileged_client,
        "name": f"{request.param['name']}-{deployment_mode.lower()}",
        "namespace": unprivileged_model_namespace.name,
        "runtime": ovms_kserve_serving_runtime.name,
        "storage_path": request.param["model-dir"],
        "storage_key": ci_endpoint_s3_secret.name,
        "model_format": ModelAndFormat.OPENVINO_IR,
        "deployment_mode": deployment_mode,
        "model_version": request.param["model-version"],
    }

    if env_vars := request.param.get("env-vars"):
        isvc_kwargs["model_env_variables"] = env_vars

    if (min_replicas := request.param.get("min-replicas")) is not None:
        isvc_kwargs["min_replicas"] = min_replicas
        if min_replicas == 0:
            isvc_kwargs["wait_for_predictor_pods"] = False

    if max_replicas := request.param.get("max-replicas"):
        isvc_kwargs["max_replicas"] = max_replicas

    if scale_metric := request.param.get("scale-metric"):
        isvc_kwargs["scale_metric"] = scale_metric

    if (scale_target := request.param.get("scale-target")) is not None:
        isvc_kwargs["scale_target"] = scale_target

    with create_isvc(**isvc_kwargs) as isvc:
        yield isvc


@pytest.fixture(scope="class")
def ovms_raw_inference_service(
    request: FixtureRequest,
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
    ovms_kserve_serving_runtime: ServingRuntime,
    ci_endpoint_s3_secret: Secret,
) -> Generator[InferenceService, Any, Any]:
    with create_isvc(
        client=unprivileged_client,
        name=f"{request.param['name']}-raw",
        namespace=unprivileged_model_namespace.name,
        external_route=True,
        runtime=ovms_kserve_serving_runtime.name,
        storage_path=request.param["model-dir"],
        storage_key=ci_endpoint_s3_secret.name,
        model_format=ModelAndFormat.OPENVINO_IR,
        deployment_mode=KServeDeploymentType.RAW_DEPLOYMENT,
        model_version=request.param["model-version"],
    ) as isvc:
        yield isvc


@pytest.fixture(scope="class")
def http_s3_tensorflow_model_mesh_inference_service(
    request: FixtureRequest,
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
    http_s3_ovms_model_mesh_serving_runtime: ServingRuntime,
    ci_endpoint_s3_secret: Secret,
    ci_service_account: ServiceAccount,
) -> Generator[InferenceService, Any, Any]:
    with create_isvc(
        client=unprivileged_client,
        name=f"{Protocols.HTTP}-{ModelFormat.TENSORFLOW}",
        namespace=unprivileged_model_namespace.name,
        runtime=http_s3_ovms_model_mesh_serving_runtime.name,
        model_service_account=ci_service_account.name,
        storage_key=ci_endpoint_s3_secret.name,
        storage_path=request.param["model-path"],
        model_format=ModelFormat.TENSORFLOW,
        deployment_mode=KServeDeploymentType.MODEL_MESH,
        model_version="2",
    ) as isvc:
        yield isvc


@pytest.fixture(scope="class")
def user_workload_monitoring_config_map(
    admin_client: DynamicClient, cluster_monitoring_config: ConfigMap
) -> Generator[ConfigMap, None, None]:
    uwm_namespace = "openshift-user-workload-monitoring"

    data = {
        "config.yaml": yaml.dump({
            "prometheus": {
                "logLevel": "debug",
                "retention": "15d",
                "volumeClaimTemplate": {"spec": {"resources": {"requests": {"storage": "40Gi"}}}},
            }
        })
    }

    with update_configmap_data(
        client=admin_client,
        name="user-workload-monitoring-config",
        namespace=uwm_namespace,
        data=data,
    ) as cm:
        yield cm

    # UWM PVCs are not deleted once the configmap is deleted; forcefully deleting the PVCs to avoid having left-overs
    for pvc in PersistentVolumeClaim.get(dyn_client=admin_client, namespace=uwm_namespace):
        pvc.clean_up()


@pytest.fixture(scope="class")
def http_s3_ovms_external_route_model_mesh_serving_runtime(
    request: FixtureRequest,
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
) -> Generator[ServingRuntime, Any, Any]:
    runtime_kwargs = {
        "client": unprivileged_client,
        "namespace": unprivileged_model_namespace.name,
        "name": f"{Protocols.HTTP}-{ModelInferenceRuntime.OPENVINO_RUNTIME}-exposed",
        "template_name": RuntimeTemplates.OVMS_MODEL_MESH,
        "multi_model": True,
        "protocol": Protocols.REST.upper(),
        "resources": {
            ModelFormat.OVMS: {
                "requests": {"cpu": "1", "memory": "4Gi"},
                "limits": {"cpu": "2", "memory": "8Gi"},
            },
        },
        "enable_external_route": True,
    }

    if hasattr(request, "param"):
        runtime_kwargs["enable_auth"] = request.param.get("enable-auth")

    with ServingRuntimeFromTemplate(**runtime_kwargs) as model_runtime:
        yield model_runtime


@pytest.fixture(scope="class")
def http_s3_openvino_second_model_mesh_inference_service(
    request: FixtureRequest,
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
    ci_endpoint_s3_secret: Secret,
    ci_service_account: ServiceAccount,
) -> Generator[InferenceService, Any, Any]:
    # Dynamically select the used ServingRuntime by passing "runtime-fixture-name" request.param
    runtime = request.getfixturevalue(argname=request.param["runtime-fixture-name"])
    with create_isvc(
        client=unprivileged_client,
        name=f"{Protocols.HTTP}-{ModelFormat.OPENVINO}-2",
        namespace=unprivileged_model_namespace.name,
        runtime=runtime.name,
        model_service_account=ci_service_account.name,
        storage_key=ci_endpoint_s3_secret.name,
        storage_path=request.param["model-path"],
        model_format=request.param["model-format"],
        deployment_mode=KServeDeploymentType.MODEL_MESH,
        model_version=request.param["model-version"],
    ) as isvc:
        yield isvc


@pytest.fixture(scope="class")
def unprivileged_s3_caikit_raw_inference_service(
    request: FixtureRequest,
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
    unprivileged_s3_caikit_serving_runtime: ServingRuntime,
    unprivileged_models_endpoint_s3_secret: Secret,
) -> Generator[InferenceService, Any, Any]:
    with create_isvc(
        client=unprivileged_client,
        name=f"{Protocols.HTTP}-{ModelFormat.CAIKIT}-raw",
        namespace=unprivileged_model_namespace.name,
        runtime=unprivileged_s3_caikit_serving_runtime.name,
        model_format=unprivileged_s3_caikit_serving_runtime.instance.spec.supportedModelFormats[0].name,
        deployment_mode=KServeDeploymentType.RAW_DEPLOYMENT,
        storage_key=unprivileged_models_endpoint_s3_secret.name,
        storage_path=ModelStoragePath.FLAN_T5_SMALL_CAIKIT,
    ) as isvc:
        yield isvc


@pytest.fixture(scope="class")
def unprivileged_s3_caikit_serving_runtime(
    admin_client: DynamicClient,
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
) -> Generator[ServingRuntime, Any, Any]:
    with ServingRuntimeFromTemplate(
        client=admin_client,
        unprivileged_client=unprivileged_client,
        name=f"{Protocols.HTTP}-{ModelInferenceRuntime.CAIKIT_TGIS_RUNTIME}",
        namespace=unprivileged_model_namespace.name,
        template_name=RuntimeTemplates.CAIKIT_TGIS_SERVING,
        multi_model=False,
        enable_http=True,
        enable_grpc=False,
    ) as model_runtime:
        yield model_runtime


@pytest.fixture(scope="class")
def unprivileged_models_endpoint_s3_secret(
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    models_s3_bucket_name: str,
    models_s3_bucket_region: str,
    models_s3_bucket_endpoint: str,
) -> Generator[Secret, Any, Any]:
    with s3_endpoint_secret(
        client=unprivileged_client,
        name="models-bucket-secret",
        namespace=unprivileged_model_namespace.name,
        aws_access_key=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_s3_region=models_s3_bucket_region,
        aws_s3_bucket=models_s3_bucket_name,
        aws_s3_endpoint=models_s3_bucket_endpoint,
    ) as secret:
        yield secret


@pytest.fixture(scope="class")
def unprivileged_s3_caikit_serverless_inference_service(
    request: FixtureRequest,
    unprivileged_client: DynamicClient,
    unprivileged_model_namespace: Namespace,
    unprivileged_s3_caikit_serving_runtime: ServingRuntime,
    unprivileged_models_endpoint_s3_secret: Secret,
) -> Generator[InferenceService, Any, Any]:
    with create_isvc(
        client=unprivileged_client,
        name=f"{Protocols.HTTP}-{ModelFormat.CAIKIT}",
        namespace=unprivileged_model_namespace.name,
        runtime=unprivileged_s3_caikit_serving_runtime.name,
        model_format=unprivileged_s3_caikit_serving_runtime.instance.spec.supportedModelFormats[0].name,
        deployment_mode=KServeDeploymentType.SERVERLESS,
        storage_key=unprivileged_models_endpoint_s3_secret.name,
        storage_path=request.param["model-dir"],
    ) as isvc:
        yield isvc


@pytest.fixture(scope="package")
def fail_if_missing_dependent_operators(admin_client: DynamicClient) -> None:
    if dependent_operators := py_config.get("dependent_operators"):
        missing_operators: list[str] = []

        for operator_name in dependent_operators.split(","):
            csvs = list(
                ClusterServiceVersion.get(
                    dyn_client=admin_client,
                    namespace=py_config["applications_namespace"],
                )
            )

            LOGGER.info(f"Verifying if {operator_name} is installed")
            for csv in csvs:
                if csv.name.startswith(operator_name):
                    if csv.status == csv.Status.SUCCEEDED:
                        break

                    else:
                        missing_operators.append(
                            f"Operator {operator_name} is installed but CSV is not in {csv.Status.SUCCEEDED} state"
                        )

            else:
                missing_operators.append(f"{operator_name} is not installed")

        if missing_operators:
            pytest.fail(str(missing_operators))

    else:
        LOGGER.info("No dependent operators to verify")
