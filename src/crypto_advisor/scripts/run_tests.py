"""
Test runner script for the Crypto Advisor project.
"""
import sys
import pytest


def run_all_tests():
    """
    Run all tests including integration tests with verbose output.
    
    This function is used as an entry point for the 'test-all' Poetry script.
    """
    sys.exit(pytest.main(["-xvs", "--run-integration"]))


if __name__ == "__main__":
    run_all_tests() 