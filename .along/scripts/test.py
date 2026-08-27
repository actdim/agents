#!/usr/bin/env python3
# Status: verified
"""
test.py - Automated Test Runner Hook for along repository.
Executes the comprehensive unit test suite via Python standard unittest.
"""

import sys
import os
import unittest

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    tests_dir = os.path.join(repo_root, "tests")
    
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=tests_dir, pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    sys.exit(0 if result.wasSuccessful() else 1)

if __name__ == "__main__":
    main()
