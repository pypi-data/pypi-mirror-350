import os
from rhoshift.utils.utils import run_command


def cleanup():
    # Get the project root directory (3 levels up from this file)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    script_path = os.path.join(project_root, "scripts", "cleanup", "cleanup_all.sh")
    cmd = f"sh {script_path}"
    run_command(cmd, live_output=True, max_retries=0)
