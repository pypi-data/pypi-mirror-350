#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import os
import logging
from utils.operator.operator import run_command
import time
import importlib.resources

# Configure logging
logger = logging.getLogger(__name__)

def run_upgrade_matrix():
    """Execute the upgrade matrix shell script."""
    # Get the script path from the installed package
    try:
        # Use the current package name (rhoai_upgrade_matrix) instead of rhoshift
        script_path = importlib.resources.files('rhoai_upgrade_matrix').joinpath('scripts/run_upgrade_matrix.sh')
        if not script_path.exists():
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
    except Exception as e:
        logger.error(f"Error running upgrade matrix: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    sys.exit(run_upgrade_matrix())
