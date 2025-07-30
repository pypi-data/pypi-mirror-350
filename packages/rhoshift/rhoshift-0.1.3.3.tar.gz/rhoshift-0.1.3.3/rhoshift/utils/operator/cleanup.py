import os
import importlib.resources
from utils.utils import run_command


def cleanup():
    try:
        script_path = importlib.resources.files('utils').joinpath('operator/scripts/cleanup_all.sh')
        if not script_path.exists():
            raise FileNotFoundError(f"Cleanup script not found at: {script_path}")
            
        cmd = f"sh {script_path}"
        run_command(cmd, live_output=True, max_retries=0)
    except Exception as e:
        raise RuntimeError(f"Error during cleanup: {str(e)}")