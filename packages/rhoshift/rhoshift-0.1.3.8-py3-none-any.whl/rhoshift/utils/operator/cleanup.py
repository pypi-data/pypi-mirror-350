import os
import sys
from rhoshift.utils.utils import run_command


def cleanup():
    # Get the package installation directory
    if getattr(sys, 'frozen', False):
        # If running as a frozen executable
        package_dir = os.path.dirname(sys.executable)
    else:
        # If running as a Python module
        package_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Look for the script in the installed package location
    script_path = os.path.join(package_dir, "scripts", "cleanup", "cleanup_all.sh")
    
    # If not found in package location, try the project root
    if not os.path.exists(script_path):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        script_path = os.path.join(project_root, "scripts", "cleanup", "cleanup_all.sh")
    
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Cleanup script not found at {script_path}")
    
    cmd = f"sh {script_path}"
    run_command(cmd, live_output=True, max_retries=0)
