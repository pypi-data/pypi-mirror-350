from typing import Any, Generator

import pytest
from kubernetes.dynamic import DynamicClient
from ocp_resources.inference_service import InferenceService
from ocp_resources.namespace import Namespace
from ocp_resources.role import Role
from ocp_resources.role_binding import RoleBinding
from ocp_resources.secret import Secret
from ocp_resources.service_account import ServiceAccount
from ocp_resources.serving_runtime import ServingRuntime
from simple_logger.logger import get_logger

from utilities.constants import (
    KServeDeploymentType,
    ModelAndFormat,
    ModelFormat,
    ModelStoragePath,
    ModelVersion,
    Protocols,
    RuntimeTemplates,
)
from utilities.inference_utils import create_isvc
from utilities.infra import create_inference_token, create_isvc_view_role, create_ns, s3_endpoint_secret
from utilities.serving_runtime import ServingRuntimeFromTemplate


LOGGER = get_logger(name=__name__)


@pytest.fixture(scope="session")
def model_namespace_scope_session(
    pytestconfig: pytest.Config,
    admin_client: DynamicClient,
    teardown_resources: bool,
) -> Generator[Namespace, Any, Any]:
    name = "upgrade-model-server"
    ns = Namespace(client=admin_client, name=name)

    if pytestconfig.option.post_upgrade:
        yield ns
        ns.clean_up()

    else:
        with create_ns(
            client=admin_client,
            name=name,
            model_mesh_enabled=True,
            add_dashboard_label=True,
            teardown=teardown_resources,
        ) as ns:
            yield ns


@pytest.fixture(scope="session")
def models_endpoint_s3_secret_scope_session(
    pytestconfig: pytest.Config,
    admin_client: DynamicClient,
    model_namespace_scope_session: Namespace,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    models_s3_bucket_name: str,
    models_s3_bucket_region: str,
    models_s3_bucket_endpoint: str,
    teardown_resources: bool,
) -> Generator[Secret, Any, Any]:
    secret_kwargs = {
        "client": admin_client,
        "name": "models-bucket-secret",
        "namespace": model_namespace_scope_session.name,
    }

    secret = Secret(**secret_kwargs)

    if pytestconfig.option.post_upgrade:
        yield secret
        secret.clean_up()

    else:
        with s3_endpoint_secret(
            **secret_kwargs,
            aws_access_key=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_s3_region=models_s3_bucket_region,
            aws_s3_bucket=models_s3_bucket_name,
            aws_s3_endpoint=models_s3_bucket_endpoint,
            teardown=teardown_resources,
        ) as secret:
            yield secret


@pytest.fixture(scope="session")
def ci_endpoint_s3_secret_scope_session(
    pytestconfig: pytest.Config,
    admin_client: DynamicClient,
    model_namespace_scope_session: Namespace,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    ci_s3_bucket_name: str,
    ci_s3_bucket_region: str,
    ci_s3_bucket_endpoint: str,
    teardown_resources: bool,
) -> Generator[Secret, Any, Any]:
    secret_kwargs = {
        "client": admin_client,
        "name": "ci-bucket-secret",
        "namespace": model_namespace_scope_session.name,
    }

    secret = Secret(**secret_kwargs)

    if pytestconfig.option.post_upgrade:
        yield secret
        secret.clean_up()

    else:
        with s3_endpoint_secret(
            **secret_kwargs,
            aws_access_key=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_s3_region=ci_s3_bucket_region,
            aws_s3_bucket=ci_s3_bucket_name,
            aws_s3_endpoint=ci_s3_bucket_endpoint,
            teardown=teardown_resources,
        ) as secret:
            yield secret


@pytest.fixture(scope="session")
def model_mesh_model_service_account_scope_session(
    pytestconfig: pytest.Config,
    admin_client: DynamicClient,
    ci_endpoint_s3_secret_scope_session: Secret,
    teardown_resources: bool,
) -> Generator[ServiceAccount, Any, Any]:
    sa_kwargs = {
        "client": admin_client,
        "name": "models-bucket-sa",
        "namespace": ci_endpoint_s3_secret_scope_session.namespace,
    }

    sa = ServiceAccount(**sa_kwargs)

    if pytestconfig.option.post_upgrade:
        yield sa
        sa.clean_up()

    else:
        with ServiceAccount(
            **sa_kwargs,
            secrets=[{"name": ci_endpoint_s3_secret_scope_session.name}],
            teardown=teardown_resources,
        ) as sa:
            yield sa


@pytest.fixture(scope="session")
def openvino_serverless_serving_runtime_scope_session(
    pytestconfig: pytest.Config,
    admin_client: DynamicClient,
    model_namespace_scope_session: Namespace,
    teardown_resources: bool,
) -> Generator[ServingRuntime, Any, Any]:
    runtime_kwargs = {
        "client": admin_client,
        "name": "onnx-serverless",
        "namespace": model_namespace_scope_session.name,
    }

    model_runtime = ServingRuntime(**runtime_kwargs)

    if pytestconfig.option.post_upgrade:
        yield model_runtime
        model_runtime.clean_up()

    else:
        with ServingRuntimeFromTemplate(
            **runtime_kwargs,
            template_name=RuntimeTemplates.OVMS_KSERVE,
            multi_model=False,
            resources={
                ModelFormat.OVMS: {
                    "requests": {"cpu": "1", "memory": "4Gi"},
                    "limits": {"cpu": "2", "memory": "8Gi"},
                }
            },
            model_format_name={ModelFormat.ONNX: ModelVersion.OPSET13},
            teardown=teardown_resources,
        ) as model_runtime:
            yield model_runtime


@pytest.fixture(scope="session")
def ovms_serverless_inference_service_scope_session(
    pytestconfig: pytest.Config,
    admin_client: DynamicClient,
    openvino_serverless_serving_runtime_scope_session: ServingRuntime,
    ci_endpoint_s3_secret_scope_session: Secret,
    teardown_resources: bool,
) -> Generator[InferenceService, Any, Any]:
    isvc_kwargs = {
        "client": admin_client,
        "name": openvino_serverless_serving_runtime_scope_session.name,
        "namespace": openvino_serverless_serving_runtime_scope_session.namespace,
    }

    isvc = InferenceService(**isvc_kwargs)

    if pytestconfig.option.post_upgrade:
        yield isvc
        isvc.clean_up()

    else:
        with create_isvc(
            runtime=openvino_serverless_serving_runtime_scope_session.name,
            storage_path="test-dir",
            storage_key=ci_endpoint_s3_secret_scope_session.name,
            model_format=ModelAndFormat.OPENVINO_IR,
            deployment_mode=KServeDeploymentType.SERVERLESS,
            model_version=ModelVersion.OPSET13,
            teardown=teardown_resources,
            **isvc_kwargs,
        ) as isvc:
            yield isvc


@pytest.fixture(scope="session")
def caikit_raw_serving_runtime_scope_session(
    pytestconfig: pytest.Config,
    admin_client: DynamicClient,
    model_namespace_scope_session: Namespace,
    teardown_resources: bool,
) -> Generator[ServingRuntime, Any, Any]:
    runtime_kwargs = {
        "client": admin_client,
        "name": "caikit-raw",
        "namespace": model_namespace_scope_session.name,
    }

    model_runtime = ServingRuntime(**runtime_kwargs)

    if pytestconfig.option.post_upgrade:
        yield model_runtime
        model_runtime.clean_up()

    else:
        with ServingRuntimeFromTemplate(
            **runtime_kwargs,
            template_name=RuntimeTemplates.CAIKIT_STANDALONE_SERVING,
            multi_model=False,
            enable_http=True,
            teardown=teardown_resources,
        ) as model_runtime:
            yield model_runtime


@pytest.fixture(scope="session")
def caikit_raw_inference_service_scope_session(
    pytestconfig: pytest.Config,
    admin_client: DynamicClient,
    caikit_raw_serving_runtime_scope_session: ServingRuntime,
    models_endpoint_s3_secret_scope_session: Secret,
    teardown_resources: bool,
) -> Generator[InferenceService, Any, Any]:
    isvc_kwargs = {
        "client": admin_client,
        "name": caikit_raw_serving_runtime_scope_session.name,
        "namespace": caikit_raw_serving_runtime_scope_session.namespace,
    }

    isvc = InferenceService(**isvc_kwargs)

    if pytestconfig.option.post_upgrade:
        yield isvc

        isvc.clean_up()

    else:
        with create_isvc(
            runtime=caikit_raw_serving_runtime_scope_session.name,
            model_format=caikit_raw_serving_runtime_scope_session.instance.spec.supportedModelFormats[0].name,
            deployment_mode=KServeDeploymentType.RAW_DEPLOYMENT,
            storage_key=models_endpoint_s3_secret_scope_session.name,
            storage_path=ModelStoragePath.EMBEDDING_MODEL,
            external_route=False,
            teardown=teardown_resources,
            **isvc_kwargs,
        ) as isvc:
            yield isvc


@pytest.fixture(scope="session")
def s3_ovms_model_mesh_serving_runtime_scope_session(
    pytestconfig: pytest.Config,
    admin_client: DynamicClient,
    model_namespace_scope_session: Namespace,
    teardown_resources: bool,
) -> Generator[ServingRuntime, Any, Any]:
    runtime_kwargs = {
        "client": admin_client,
        "name": "ovms-model-mesh",
        "namespace": model_namespace_scope_session.name,
    }

    model_runtime = ServingRuntime(**runtime_kwargs)

    if pytestconfig.option.post_upgrade:
        yield model_runtime
        model_runtime.clean_up()

    else:
        with ServingRuntimeFromTemplate(
            **runtime_kwargs,
            template_name=RuntimeTemplates.OVMS_MODEL_MESH,
            multi_model=True,
            protocol=Protocols.REST.upper(),
            resources={
                ModelFormat.OVMS: {
                    "requests": {"cpu": "1", "memory": "4Gi"},
                    "limits": {"cpu": "2", "memory": "8Gi"},
                }
            },
            teardown=teardown_resources,
        ) as model_runtime:
            yield model_runtime


@pytest.fixture(scope="session")
def openvino_model_mesh_inference_service_scope_session(
    pytestconfig: pytest.Config,
    admin_client: DynamicClient,
    s3_ovms_model_mesh_serving_runtime_scope_session: ServingRuntime,
    ci_endpoint_s3_secret_scope_session: Secret,
    model_mesh_model_service_account_scope_session: ServiceAccount,
    teardown_resources: bool,
) -> Generator[InferenceService, Any, Any]:
    isvc_kwargs = {
        "client": admin_client,
        "name": s3_ovms_model_mesh_serving_runtime_scope_session.name,
        "namespace": s3_ovms_model_mesh_serving_runtime_scope_session.namespace,
    }

    isvc = InferenceService(**isvc_kwargs)

    if pytestconfig.option.post_upgrade:
        yield isvc
        isvc.clean_up()

    else:
        with create_isvc(
            runtime=s3_ovms_model_mesh_serving_runtime_scope_session.name,
            model_service_account=model_mesh_model_service_account_scope_session.name,
            storage_key=ci_endpoint_s3_secret_scope_session.name,
            storage_path=ModelStoragePath.OPENVINO_EXAMPLE_MODEL,
            model_format=ModelAndFormat.OPENVINO_IR,
            deployment_mode=KServeDeploymentType.MODEL_MESH,
            model_version=ModelVersion.OPSET1,
            teardown=teardown_resources,
            **isvc_kwargs,
        ) as isvc:
            yield isvc


@pytest.fixture(scope="session")
def model_service_account_scope_session(
    pytestconfig: pytest.Config,
    admin_client: DynamicClient,
    ci_endpoint_s3_secret_scope_session: Secret,
    teardown_resources: bool,
) -> Generator[ServiceAccount, Any, Any]:
    sa_kwargs = {
        "client": admin_client,
        "name": "upgrade-models-bucket-sa",
        "namespace": ci_endpoint_s3_secret_scope_session.namespace,
    }

    sa = ServiceAccount(**sa_kwargs)

    if pytestconfig.option.post_upgrade:
        yield sa
        sa.clean_up()

    else:
        with ServiceAccount(
            client=admin_client,
            namespace=ci_endpoint_s3_secret_scope_session.namespace,
            name="upgrade-models-bucket-sa",
            secrets=[{"name": ci_endpoint_s3_secret_scope_session.name}],
            teardown=teardown_resources,
        ) as sa:
            yield sa


@pytest.fixture(scope="session")
def http_view_role_scope_session(
    pytestconfig: pytest.Config,
    admin_client: DynamicClient,
    ovms_authenticated_serverless_inference_service_scope_session: InferenceService,
    teardown_resources: bool,
) -> Generator[Role, Any, Any]:
    role_kwargs = {
        "client": admin_client,
        "name": f"{ovms_authenticated_serverless_inference_service_scope_session.name}-view",
    }

    role = Role(
        **role_kwargs,
        namespace=ovms_authenticated_serverless_inference_service_scope_session.namespace,
    )

    if pytestconfig.option.post_upgrade:
        yield role
        role.clean_up()

    else:
        with create_isvc_view_role(
            **role_kwargs,
            isvc=ovms_authenticated_serverless_inference_service_scope_session,
            resource_names=[ovms_authenticated_serverless_inference_service_scope_session.name],
            teardown=teardown_resources,
        ) as role:
            yield role


@pytest.fixture(scope="session")
def http_role_binding_scope_session(
    pytestconfig: pytest.Config,
    admin_client: DynamicClient,
    http_view_role_scope_session: Role,
    model_service_account_scope_session: ServiceAccount,
    ovms_authenticated_serverless_inference_service_scope_session: InferenceService,
    teardown_resources: bool,
) -> Generator[RoleBinding, Any, Any]:
    rb_kwargs = {
        "client": admin_client,
        "name": f"{model_service_account_scope_session.name}-view",
        "namespace": ovms_authenticated_serverless_inference_service_scope_session.namespace,
    }

    rb = RoleBinding(**rb_kwargs)

    if pytestconfig.option.post_upgrade:
        yield rb
        rb.clean_up()

    else:
        with RoleBinding(
            **rb_kwargs,
            role_ref_name=http_view_role_scope_session.name,
            role_ref_kind=http_view_role_scope_session.kind,
            subjects_kind=model_service_account_scope_session.kind,
            subjects_name=model_service_account_scope_session.name,
            teardown=teardown_resources,
        ) as rb:
            yield rb


@pytest.fixture(scope="session")
def http_inference_token_scope_session(
    model_service_account_scope_session: ServiceAccount, http_role_binding_scope_session: RoleBinding
) -> str:
    return create_inference_token(model_service_account=model_service_account_scope_session)


@pytest.fixture(scope="session")
def ovms_authenticated_serverless_inference_service_scope_session(
    pytestconfig: pytest.Config,
    admin_client: DynamicClient,
    openvino_serverless_serving_runtime_scope_session: ServingRuntime,
    ci_endpoint_s3_secret_scope_session: Secret,
    teardown_resources: bool,
) -> Generator[InferenceService, Any, Any]:
    isvc_kwargs = {
        "client": admin_client,
        "name": f"{openvino_serverless_serving_runtime_scope_session.name}-auth",
        "namespace": openvino_serverless_serving_runtime_scope_session.namespace,
    }

    isvc = InferenceService(**isvc_kwargs)

    if pytestconfig.option.post_upgrade:
        yield isvc
        isvc.clean_up()

    else:
        with create_isvc(
            runtime=openvino_serverless_serving_runtime_scope_session.name,
            storage_path="test-dir",
            storage_key=ci_endpoint_s3_secret_scope_session.name,
            model_format=ModelAndFormat.OPENVINO_IR,
            deployment_mode=KServeDeploymentType.SERVERLESS,
            model_version=ModelVersion.OPSET13,
            enable_auth=True,
            teardown=teardown_resources,
            **isvc_kwargs,
        ) as isvc:
            yield isvc
