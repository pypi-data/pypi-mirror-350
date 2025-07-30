import logging
import subprocess
import time
from typing import Tuple, Optional
import sys
import threading


def run_command(
        cmd: str,
        max_retries: int = 3,
        retry_delay: float = 5.0,
        timeout: Optional[int] = None,
        cwd: Optional[str] = None,
        env: Optional[dict] = None,
        shell: bool = True,
        log_output: bool = True,
        live_output: bool = False
) -> Tuple[int, str, str]:
    """Execute a shell command with retries and proper error handling."""
    attempt = 0
    last_exception = None
    stdout = ""
    stderr = ""

    def stream_output(pipe, output_list, log_prefix, is_stderr=False):
        for line in iter(pipe.readline, ''):
            if line:
                line = line.rstrip()
                if live_output:
                    print(line, file=sys.stderr if is_stderr else sys.stdout)
                if log_output:
                    logging.debug(f"{log_prefix}: {line}")
                output_list.append(line)
        pipe.close()

    while attempt <= max_retries:
        attempt += 1
        try:
            logging.info(f"Executing command (attempt {attempt}/{max_retries}): {cmd}")

            if live_output:
                process = subprocess.Popen(
                    cmd,
                    shell=shell,
                    cwd=cwd,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1
                )

                stdout_lines = []
                stderr_lines = []

                # Start threads to capture stdout and stderr
                t_out = threading.Thread(target=stream_output, args=(process.stdout, stdout_lines, "STDOUT"))
                t_err = threading.Thread(target=stream_output, args=(process.stderr, stderr_lines, "STDERR", True))
                t_out.start()
                t_err.start()

                # Wait for completion
                t_out.join()
                t_err.join()
                process.wait(timeout=timeout)

                return_code = process.returncode
                stdout = '\n'.join(stdout_lines)
                stderr = '\n'.join(stderr_lines)

            else:
                result = subprocess.run(
                    cmd,
                    shell=shell,
                    check=False,
                    timeout=timeout,
                    cwd=cwd,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout = result.stdout
                stderr = result.stderr
                return_code = result.returncode

                if log_output:
                    if stdout:
                        logging.debug(f"STDOUT: {stdout.strip()}")
                    if stderr:
                        logging.debug(f"STDERR: {stderr.strip()}")

            if return_code == 0:
                return return_code, stdout, stderr

            last_exception = subprocess.CalledProcessError(
                return_code, cmd, stdout, stderr
            )

        except subprocess.TimeoutExpired as e:
            last_exception = e
            logging.warning(f"Command timed out: {cmd}")

        except Exception as e:
            last_exception = e
            logging.error(f"Unexpected error executing command: {e}")

        if attempt <= max_retries:
            logging.info(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    logging.error(f"Command failed after {max_retries} attempts: {cmd}")
    if last_exception:
        if isinstance(last_exception, subprocess.CalledProcessError):
            return (
                last_exception.returncode,
                last_exception.stdout,
                last_exception.stderr
            )
        else:
            return -1, "", str(last_exception)

    return -1, "", "Unknown error"


def apply_manifest(
        manifest_content: str,
        oc_binary: str = "oc",
        namespace: Optional[str] = None,
        context: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 10.0,
        timeout: Optional[int] = 300,
        log_output: bool = True,
        **kwargs
) -> Tuple[int, str, str]:
    """Apply a Kubernetes/OpenShift manifest with robust error handling.

    Args:
        manifest_content: String content of the manifest to apply
        oc_binary: Path to oc/kubectl binary (default: 'oc')
        namespace: Namespace to apply the manifest to
        context: Kubernetes context to use
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
        timeout: Timeout in seconds for the command
        log_output: Whether to log command output
        **kwargs: Additional arguments to pass to run_command

    Returns:
        Tuple of (return_code, stdout, stderr)

    Raises:
        RuntimeError: If manifest application fails after retries
    """
    try:
        # Build base command
        cmd_parts = [oc_binary, "apply", "-f", "-"]

        if namespace:
            cmd_parts.extend(["-n", namespace])
        if context:
            cmd_parts.extend(["--context", context])

        base_cmd = " ".join(cmd_parts)
        full_cmd = f"{base_cmd} <<EOF\n{manifest_content}\nEOF"

        logging.info(f"Applying manifest (size: {len(manifest_content)} bytes)")
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug(f"Manifest content:\n{manifest_content}")

        rc, stdout, stderr = run_command(
            full_cmd,
            max_retries=max_retries,
            retry_delay=retry_delay,
            timeout=timeout,
            log_output=log_output,
            **kwargs
        )

        if rc != 0:
            error_msg = f"Manifest application failed (rc={rc}): {stderr.strip()}"
            if "already exists" in stderr:
                logging.warning(error_msg)
            else:
                raise RuntimeError(error_msg)

        logging.info("Manifest applied successfully")
        return rc, stdout, stderr

    except Exception as e:
        logging.error(f"Failed to apply manifest: {str(e)}")
        raise RuntimeError(f"Manifest application failed: {str(e)}") from e


def wait_for_resource_for_specific_status(
        status: str,
        cmd: str,
        timeout: int = 300,
        interval: int = 5,
        case_sensitive: bool = False,
        max_retries: int = 3,
        retry_delay: float = 5.0,
        log_output: bool = True,
        cwd: Optional[str] = None,
        env: Optional[dict] = None,
        shell: bool = True
) -> Tuple[bool, str, str]:
    """
    Wait for a specific status to appear in command output.

    Args:
        status: Expected status string to wait for
        cmd: Command to execute repeatedly
        timeout: Maximum time to wait in seconds (default: 300)
        interval: Time between command executions in seconds (default: 5)
        case_sensitive: Whether status check should be case sensitive (default: False)
        max_retries: Maximum retry attempts for each command execution (passed to run_command)
        retry_delay: Delay between retries in seconds (passed to run_command)
        log_output: Whether to log command output (passed to run_command)
        cwd: Working directory for command (passed to run_command)
        env: Environment variables dictionary (passed to run_command)
        shell: Whether to run through shell (passed to run_command)

    Returns:
        Tuple of (success: bool, last_stdout: str, last_stderr: str)
    """
    start_time = time.time()
    end_time = start_time + timeout
    last_stdout = ""
    last_stderr = ""

    if not case_sensitive:
        status = status.lower()

    while time.time() < end_time:
        # Run the check command with explicit parameters
        rc, last_stdout, last_stderr = run_command(
            cmd,
            max_retries=max_retries,
            retry_delay=retry_delay,
            timeout=interval,  # Don't let individual commands exceed our interval
            cwd=cwd,
            env=env,
            shell=shell,
            log_output=log_output
        )

        # Check if command succeeded and contains desired status
        current_status = last_stdout if case_sensitive else last_stdout.lower()
        if rc == 0 and status == current_status.strip():
            return True, last_stdout, last_stderr

        # Log progress if we have stderr output
        if last_stderr:
            logging.info(f"Waiting for status '{status}': {last_stderr.strip()}")

        # Sleep until next check
        time.sleep(interval)

    # Timeout reached
    elapsed = time.time() - start_time
    logging.error(
        f"Timeout after {elapsed:.1f}s waiting for status '{status}'. "
        f"Last output: {last_stdout.strip()}"
    )
    return False, last_stdout, last_stderr
