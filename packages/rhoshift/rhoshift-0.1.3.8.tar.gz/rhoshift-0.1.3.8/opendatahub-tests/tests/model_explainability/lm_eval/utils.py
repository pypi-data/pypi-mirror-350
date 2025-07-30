from kubernetes.dynamic import DynamicClient
from ocp_resources.lm_eval_job import LMEvalJob
from ocp_resources.pod import Pod

from utilities.constants import Timeout
from utilities.infra import check_pod_status_in_time
from simple_logger.logger import get_logger


LOGGER = get_logger(name=__name__)


def verify_lmevaljob_running(client: DynamicClient, lmevaljob: LMEvalJob) -> None:
    """
    Verifies that an LMEvalJob Pod reaches Running state and maintains Running/Succeeded state.
    Waits for Pod to enter Running state, then checks it stays Running or Succeeded for 2 minutes.

    Args:
        client: DynamicClient instance for interacting with Kubernetes
        lmevaljob: LMEvalJob object representing the job to verify

    Raises:
        TimeoutError: If Pod doesn't reach Running state within 10 minutes
        AssertionError: If Pod doesn't stay in one of the desired states for 2 minutes
    """

    lmevaljob_pod = Pod(client=client, name=lmevaljob.name, namespace=lmevaljob.namespace, wait_for_resource=True)
    lmevaljob_pod.wait_for_status(status=lmevaljob_pod.Status.RUNNING, timeout=Timeout.TIMEOUT_20MIN)

    check_pod_status_in_time(pod=lmevaljob_pod, status={lmevaljob_pod.Status.RUNNING, lmevaljob_pod.Status.SUCCEEDED})


def get_lmevaljob_pod(client: DynamicClient, lmevaljob: LMEvalJob, timeout: int = Timeout.TIMEOUT_2MIN) -> Pod:
    """
    Gets the pod corresponding to a given LMEvalJob and waits for it to be ready.

    Args:
        client: The Kubernetes client to use
        lmevaljob: The LMEvalJob that the pod is associated with
        timeout: How long to wait for the pod, defaults to TIMEOUT_2MIN

    Returns:
        Pod resource
    """
    lmeval_pod = Pod(
        client=client,
        namespace=lmevaljob.namespace,
        name=lmevaljob.name,
    )

    lmeval_pod.wait(timeout=timeout)

    return lmeval_pod
