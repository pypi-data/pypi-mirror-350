#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import os
import logging
from rhoshift.utils.utils import run_command

# Configure logging
logger = logging.getLogger(__name__)


def run_upgrade_matrix():
    """Execute the upgrade matrix shell script."""
    # Get the package installation directory
    if getattr(sys, 'frozen', False):
        # If running as a frozen executable
        package_dir = os.path.dirname(sys.executable)
    else:
        # If running as a Python module
        package_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Look for the script in the installed package location
    script_path = os.path.join(package_dir, "scripts", "run_upgrade_matrix.sh")
    
    # If not found in package location, try the project root
    if not os.path.exists(script_path):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        script_path = os.path.join(project_root, "run_upgrade_matrix.sh")
    
    if not os.path.exists(script_path):
        logger.error(f"Script not found at: {script_path}")
        sys.exit(1)

    # Execute script with all arguments using run_command
    args = " ".join(sys.argv[1:])
    logger.info(f"Running upgrade matrix with args: {args}")
    return_code, stdout, stderr = run_command(f"bash {script_path} {args}", live_output=True, max_retries=0)

    if return_code != 0:
        logger.error(f"Upgrade matrix failed with exit code: {return_code}")
    else:
        logger.info("Upgrade matrix completed successfully")

    return return_code


if __name__ == "__main__":
    sys.exit(run_upgrade_matrix())
