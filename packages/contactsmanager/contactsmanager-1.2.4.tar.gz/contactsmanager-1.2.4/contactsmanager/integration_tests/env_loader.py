"""
Environment variable loader for integration tests.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


def load_env_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables or .env file.

    Returns:
        Dict containing the test configuration
    """
    # First try to load from TEST_CONFIG environment variable
    config_json = os.environ.get("TEST_CONFIG")
    if config_json:
        try:
            return json.loads(config_json)
        except json.JSONDecodeError:
            print("WARNING: TEST_CONFIG environment variable is not valid JSON")

    print("WARNING: No test configuration found")
    return {}
