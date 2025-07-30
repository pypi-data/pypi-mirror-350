#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import os
import logging
from importlib.resources import files
from rhoshift.utils.utils import run_command

# Configure logging
logger = logging.getLogger(__name__)

def find_script():
    """Locate the run_upgrade_matrix.sh script using multiple methods."""
    try:
        # 1. First try using package resources (works for installed packages)
        script_path = files('rhoshift').joinpath('scripts/run_upgrade_matrix.sh')
        if os.path.exists(script_path):
            return script_path
        
        # 2. Try alternative package resource path
        script_path = files('rhoshift').joinpath('run_upgrade_matrix.sh')
        if os.path.exists(script_path):
            return script_path
        
        # 3. Fallback for development/frozen environments
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Check in scripts directory
        script_path = os.path.join(base_path, 'scripts', 'run_upgrade_matrix.sh')
        if os.path.exists(script_path):
            return script_path
        
        # Check in root directory
        script_path = os.path.join(base_path, 'run_upgrade_matrix.sh')
        if os.path.exists(script_path):
            return script_path
        
    except Exception as e:
        logger.debug(f"Error while locating script: {str(e)}")
    
    return None

def run_upgrade_matrix():
    """Execute the upgrade matrix shell script."""
    script_path = find_script()
    
    if not script_path or not os.path.exists(script_path):
        logger.error("Could not locate run_upgrade_matrix.sh script")
        logger.error("Searched in:")
        logger.error("1. Package resources")
        logger.error("2. scripts/ directory")
        logger.error("3. Package root directory")
        return 1

    try:
        # Make script executable
        os.chmod(script_path, 0o755)
        
        # Prepare command
        args = " ".join(sys.argv[1:])
        logger.info(f"Executing upgrade matrix with arguments: {args}")
        cmd = f"bash {script_path} {args}"
        
        # Execute command
        return_code, stdout, stderr = run_command(
            cmd,
            live_output=True,
            max_retries=0
        )

        if return_code != 0:
            logger.error(f"Script failed with exit code {return_code}")
            if stderr:
                logger.error(stderr)
        else:
            logger.info("Upgrade matrix completed successfully")
            if stdout:
                logger.info(stdout)

        return return_code

    except Exception as e:
        logger.error(f"Failed to execute upgrade matrix: {str(e)}")
        return 1


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    sys.exit(run_upgrade_matrix())