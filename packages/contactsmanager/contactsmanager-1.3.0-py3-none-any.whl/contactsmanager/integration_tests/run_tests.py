#!/usr/bin/env python
"""
Script to run integration tests for the ContactsManager SDK.

This script can be run directly or via pytest.
"""
import sys
import unittest
from pathlib import Path

# Add the parent directory to sys.path to import the package
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the test modules
from contactsmanager.integration_tests.test_api_key_validation import (
    TestApiKeyValidation,
)
from contactsmanager.integration_tests.test_server_api import (
    TestServerAPI,
)
from contactsmanager.integration_tests.env_loader import load_env_config


def run_tests():
    """Run all integration tests."""
    # Load configuration
    config = load_env_config()
    if not config:
        print(
            "WARNING: No test configuration found. Tests requiring credentials will be skipped."
        )
        print("Please set TEST_CONFIG environment variable or create test_config.json")

    # Create a test suite
    suite = unittest.TestSuite()

    # Add test cases using TestLoader
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(TestApiKeyValidation))
    suite.addTest(loader.loadTestsFromTestCase(TestServerAPI))

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
